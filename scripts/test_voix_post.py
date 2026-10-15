#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cas de test de la regle d'attribution de l'ecrit social.

    python3 scripts/test_voix_post.py

Chaque cas est une publication reelle du corpus. Si vous modifiez lib_voix_post.py,
ces cas disent ce que la regle est censee faire.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_voix_post import voix_du_post

CAS = [
 # --- ses mots, suivis d'un simple credit : le texte reste de lui ---
 ("Ces jeunes ont besoin de discipline. Si on remet en place des etablissements "
  "disciplinaires pour les voyous, on va sauver des gamins et proteger la societe. "
  "@davidlisnard",
  "david-lisnard", "le credit en fin de legende ne retire pas la parole"),

 ("« Les ecologistes d'extreme gauche aiment la nature, mais ils detestent la nature "
  "humaine » @davidlisnard hier soir a Benfeld.",
  "david-lisnard", "citation creditee : « ... » puis le lieu et la date"),

 ("« Le pouvoir peut rendre fou et con »  @davidlisnard",
  "david-lisnard", "une citation courte reste de lui"),

 # --- du texte sur lui : ce n'est pas sa parole ---
 ("Bocca Cabana : @davidlisnard detaille la 5eme phase du projet emblematique de "
  "renovation du littoral boccassien !",
  "equipe", "il est le sujet de la phrase, pas son auteur"),

 # descriptif de video, texte reel du corpus : l'enonce sur lui encadre le contenu
 ("David Lisnard sur franceinfo : « A chaque crise, on se rend compte que la France "
  "devient faible »\n\n"
  "David Lisnard etait l'invite du 7h30 de franceinfo, interroge par Alix Bouilhaguet.\n\n"
  "Flambee des prix des carburants, mobilisation des pecheurs, depenses publiques, "
  "bureaucratie, retraites, collectivites locales et election presidentielle de 2027 : "
  "le president de Nouvelle Energie expose ses propositions pour sortir la France de la "
  "spirale de la depense et retrouver un Etat plus efficace.\n\n"
  "« A chaque crise, on va se rendre compte que la France devient faible. »\n\n"
  "David Lisnard defend notamment un",
  "equipe", "descriptif de video : l'enonce sur lui encadre le contenu"),

 ("Pour un capitalisme POPULAIRE. @davidlisnard souhaite que tous les Francais "
  "deviennent coproprietaires des grandes entreprises francaises.",
  "equipe", "un slogan de quatre mots ne fait pas un propos"),

 # --- garde-fous ---
 ("Voici le lien vers mon interview integrale de ce matin : "
  "https://www.cannesradio.com/interview-exclusive-de-david-lisnard-sur-cannes-radio",
  "david-lisnard", "son nom dans l'adresse du lien ne compte pas"),
]

def main():
    rates = 0
    for texte, attendu, pourquoi in CAS:
        voix, methode, tdl, citations, cadre = voix_du_post(texte, "David Lisnard")
        ok = voix == attendu
        rates += not ok
        print(f"{'ok  ' if ok else 'RATE'} {attendu:14s} {pourquoi}")
        if not ok:
            print(f"       obtenu : {voix} ({methode})")
    # la citation d'un passage d'equipe doit etre conservee
    _, _, _, cit, _ = voix_du_post(CAS[4][0], "David Lisnard")
    if not cit:
        rates += 1; print("RATE citation_dl       la citation du passage d'equipe est perdue")
    else:
        print(f"ok   citation_dl       conservee : « {cit[0][:48]}... »")
    # le cadre editorial doit sortir du texte
    _, _, tdl, _, cadre = voix_du_post(CAS[1][0], "David Lisnard")
    if cadre and "Benfeld" in cadre and "Benfeld" not in (tdl or ""):
        print(f"ok   cadre_editorial   retire de texte : « {cadre} »")
    else:
        rates += 1; print(f"RATE cadre_editorial   texte={tdl!r} cadre={cadre!r}")
    print(f"\n{len(CAS) + 2 - rates}/{len(CAS) + 2} cas passent")
    return 1 if rates else 0

if __name__ == "__main__":
    sys.exit(main())
