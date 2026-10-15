#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recherche sémantique : calcule les vecteurs une fois, les met en cache, puis interroge.

Le corpus entier coûte moins de deux centimes à vectoriser avec text-embedding-3-small.
Les vecteurs ne sont PAS versionnés dans ce dépôt : ils dépendent du modèle choisi et
pèseraient 27 Mo à chaque régénération.

    pip install numpy openai
    export OPENAI_API_KEY=sk-...
    python3 exemples/recherche_semantique.py "comment financer la retraite par capitalisation"
"""
import argparse, json, os, sys
import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(RACINE, "data", "corpus.jsonl")
CACHE = os.path.join(RACINE, "data", "vecteurs.npy")
MODELE = "text-embedding-3-small"
DIMS = 1536

def charger():
    with open(CORPUS, encoding="utf-8") as f:
        return [json.loads(l) for l in f]

def vectoriser(textes, client):
    out = []
    for i in range(0, len(textes), 256):
        lot = textes[i:i + 256]
        r = client.embeddings.create(model=MODELE, input=lot, dimensions=DIMS)
        out += [d.embedding for d in r.data]
        print(f"  {min(i + 256, len(textes))}/{len(textes)}", file=sys.stderr)
    return np.array(out, dtype=np.float32)

def index(corpus, client):
    if os.path.exists(CACHE):
        V = np.load(CACHE)
        if V.shape[0] == len(corpus): return V
        print("corpus modifié, recalcul des vecteurs", file=sys.stderr)
    V = vectoriser([e["texte"] for e in corpus], client)
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    np.save(CACHE, V)
    return V

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("question"); ap.add_argument("-k", type=int, default=5)
    ap.add_argument("--type", help="interview, discours, post, programme, fiche_2027")
    a = ap.parse_args()
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("pip install openai numpy")
    client = OpenAI()
    corpus = charger()
    V = index(corpus, client)
    q = np.array(client.embeddings.create(model=MODELE, input=[a.question],
                                          dimensions=DIMS).data[0].embedding, dtype=np.float32)
    q /= np.linalg.norm(q)
    score = V @ q
    ordre = np.argsort(-score)
    montres = 0
    for i in ordre:
        e = corpus[int(i)]
        if a.type and e["type_source"] != a.type: continue
        print(f"\n[{score[i]:.3f}] {e['date'] or 'sans date'} · {e['media'] or e['type_source']}")
        print(f"  {e['texte'][:400]}")
        print(f"  → {e['url_source'] or e.get('reference_papier') or 'sans lien'}")
        montres += 1
        if montres >= a.k: break
