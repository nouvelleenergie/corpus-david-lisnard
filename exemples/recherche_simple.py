#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recherche par mots dans le corpus, sans aucune dépendance.

    python3 exemples/recherche_simple.py "retraite capitalisation"
    python3 exemples/recherche_simple.py "école" --theme education --depuis 2026-01-01
"""
import argparse, json, os, re, sys, unicodedata

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "corpus.jsonl")

def sans_accents(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def charger(chemin=BASE):
    with open(chemin, encoding="utf-8") as f:
        return [json.loads(l) for l in f]

def chercher(corpus, question, k=5, theme=None, depuis=None, complet_seulement=False):
    mots = [m for m in re.findall(r"\w+", sans_accents(question)) if len(m) > 2]
    if not mots: return []
    out = []
    for e in corpus:
        if theme and theme not in e["themes"]: continue
        if depuis and (not e["date"] or e["date"] < depuis): continue
        if complet_seulement and not e["extrait_complet"]: continue
        t = sans_accents(e["texte"])
        n = sum(t.count(m) for m in mots)
        if not n: continue
        couverture = sum(1 for m in mots if m in t) / len(mots)
        # on favorise les passages qui contiennent TOUS les mots, puis les plus récents
        out.append((couverture * 10 + min(n, 5), e["date"] or "", e))
    out.sort(key=lambda x: (-x[0], x[1] < "", x[1]), reverse=False)
    out.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [e for _, _, e in out[:k]]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("question"); ap.add_argument("-k", type=int, default=5)
    ap.add_argument("--theme"); ap.add_argument("--depuis")
    ap.add_argument("--complet", action="store_true", help="seulement les passages finissant sur une ponctuation")
    a = ap.parse_args()
    corpus = charger()
    res = chercher(corpus, a.question, a.k, a.theme, a.depuis, a.complet)
    if not res: sys.exit("Aucun résultat.")
    for e in res:
        print(f"\n[{e['date'] or 'sans date'}] {e['media'] or e['type_source']}"
              f"{' · ' + e['titre_source'] if e['titre_source'] else ''}")
        print(f"  {e['texte'][:400]}")
        print(f"  → {e['url_source'] or e.get('reference_papier') or 'sans lien'}")
