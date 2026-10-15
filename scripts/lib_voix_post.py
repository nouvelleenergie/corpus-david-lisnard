# -*- coding: utf-8 -*-
"""Qui parle dans une publication de reseau social ?

Le corpus affirme que chaque passage porte un locuteur verifie. Pour l'oral, la
diarisation le garantit. Pour l'ecrit social, non : un compte de campagne publie
trois choses melangees, et seule la premiere est de la main de David Lisnard.

  1. ses propres mots      « Ces jeunes ont besoin de discipline. »
  2. ses mots + un credit  « ... » @davidlisnard hier soir a Benfeld.
  3. du texte sur lui      « @davidlisnard detaille la 5e phase du projet. »

METHODE. Le texte est decoupe en segments (phrases et retours a la ligne), les
passages entre guillemets etant masques d'abord pour ne pas etre coupes. Chaque
segment qui designe David Lisnard est pese : au-dela de MOTS_CREDIT_MAX mots
utiles autour de la mention, ce n'est plus un credit, c'est un ENONCE SUR LUI.

  • un enonce sur lui place AVANT ou ENTRE les segments de contenu => equipe.
    C'est le cas des descriptions YouTube (« David Lisnard etait l'invite du
    7h30 de franceinfo, interroge par Alix Bouilhaguet ») et des comptes rendus
    de deplacement.
  • un enonce place APRES tout le contenu est un cadre editorial : un credit ou
    un appel a l'action ajoute sous ses mots. Le texte reste de lui, le cadre
    part dans `cadre_editorial`.

Les passages entre guillemets sont toujours de lui : quand le passage est classe
`equipe`, ils ressortent dans `citation_dl` pour ne rien perdre.

Limite assumee : la regle est lexicale, elle ne lit pas le sens. Elle manque le
compte tiers qui raconte un evenement sans jamais le prendre pour sujet. La
precision mesuree sur relecture integrale des cas signales est publiee avec le
corpus, et `compte_source` permet a chacun de filtrer plus durement.
"""
import re, unicodedata

# Referents que David Lisnard n'emploie pas pour se designer lui-meme.
REF_EXCLUSIF = (r"@\s?david[\s._]?lisnard|@david_lisnard"
                r"|\bnotre maire\b|\ble maire de cannes\b|\bm\. lisnard\b|\bd\. lisnard\b"
                r"|\ble president de nouvelle energie\b")
# Toute facon de le designer.
REF_TOUT = re.compile(r"\bdavid lisnard\b|\blisnard\b|" + REF_EXCLUSIF, re.I)
REF_EXCLUSIF = re.compile(REF_EXCLUSIF, re.I)
PREMIERE = re.compile(r"\b(?:je|j'|me|m'|moi|mon|ma|mes|nous|notre|nos)\b", re.I)
# « ... » ne peut pas s'imbriquer. “ ... ” si : on prend alors le plus large sur la ligne.
GUILLEMETS = re.compile(r"«\s*([^«»]{12,}?)\s*»|[“\"]\s*([^\n“]{12,})\s*[”\"]")
BRUIT = re.compile(r"https?://\S+|\S+\.(?:fr|com|org|net)/\S*|#\w+|[^\w\s'’.,;:!?()-]", re.U)
# Les liens portent souvent son nom dans leur adresse : on les retire avant toute detection.
LIENS = re.compile(r"https?://\S+|\b\S+\.(?:fr|com|org|net|io)/\S*", re.I)

MOTS_CREDIT_MAX = 6   # au-dela, le segment ne credite plus : il raconte
MOTS_CORPS_MIN = 12   # en-dessous, le propos non cite est un slogan, pas un contenu
MOTS_CITATION_MIN = 5 # une citation courte reste de lui : « Le pouvoir peut rendre fou et con »

def _anorm(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def _cite(m):
    return (m.group(1) or m.group(2) or "").strip()

def _segments(txt):
    """Segments du texte, citations masquees pendant le decoupage puis restaurees."""
    cits = []
    def _pose(m):
        cits.append(m.group(0)); return f"\x00{len(cits)-1}\x00"
    masq = GUILLEMETS.sub(_pose, txt)
    out = []
    for s in re.split(r"(?<=[.!?…])\s+|\n+", masq):
        if not s.strip(): continue
        idx = [int(i) for i in re.findall(r"\x00(\d+)\x00", s)]
        out.append((re.sub(r"\x00(\d+)\x00", lambda m: cits[int(m.group(1))], s), idx))
    return out

def _mots(s, hors_citation=True):
    """Mots utiles : sans les citations, sans les mentions de David Lisnard, sans le bruit."""
    if hors_citation: s = GUILLEMETS.sub(" ", s)
    s = BRUIT.sub(" ", REF_TOUT.sub(" ", _anorm(s)))
    return len([w for w in re.findall(r"[a-z0-9'’-]+", s) if len(w) > 1])

def _recompose(parts):
    """Recolle les morceaux gardes : sans lien nu, sans doublon, sans espace en trop.

    Les titres YouTube reprennent souvent la premiere phrase de la description :
    le dedoublonnage se fait sur la forme normalisee, pas sur la chaine brute.
    """
    out, vus = [], set()
    for p in parts:
        p = re.sub(r"\s+", " ", LIENS.sub(" ", p or "")).strip(" \t·-—:|")
        if not p: continue
        k = re.sub(r"[^a-z0-9]", "", _anorm(p))
        if not k or k in vus: continue
        vus.add(k); out.append(p)
    return " ".join(out).strip() or None

def _perte(origine, garde):
    """Part des mots de l'origine (hors cadre) absents du texte recompose."""
    mo = set(re.findall(r"[a-z0-9'’-]{3,}", _anorm(origine)))
    mg = set(re.findall(r"[a-z0-9'’-]{3,}", _anorm(garde or "")))
    return 1.0 if not mo else len(mo - mg) / len(mo)

def voix_du_post(texte, compte_proprietaire=None):
    """(voix, methode, texte_dl, citations, cadre_editorial) pour une publication.

    voix      'david-lisnard' si le passage porte ses mots, 'equipe' sinon
    texte_dl  ses mots, debarrasses du cadre editorial ; None si voix='equipe'
    citations ses paroles entre guillemets, quand le passage est de l'equipe
    """
    t = texte or ""
    citations = [_cite(m) for m in GUILLEMETS.finditer(t)]
    mots_cites = sum(len(c.split()) for c in citations)
    segs = _segments(t)

    roles = []
    for seg, idx in segs:
        net = LIENS.sub(" ", seg)
        if REF_TOUT.search(_anorm(net)):
            roles.append(("enonce" if _mots(net) > MOTS_CREDIT_MAX else "credit", seg))
        elif _mots(net) or idx:
            roles.append(("corps", seg))
        else:
            roles.append(("bruit", seg))   # lien seul, emoji seul : ni contenu ni cadre
    enonces = [i for i, (r, _) in enumerate(roles) if r == "enonce"]
    corps = [i for i, (r, _) in enumerate(roles) if r == "corps"]
    mots_dl = sum(_mots(roles[i][1]) for i in corps) + mots_cites
    assez = mots_dl >= MOTS_CORPS_MIN or mots_cites >= MOTS_CITATION_MIN

    if enonces:
        apres_tout = not corps or min(enonces) > max(corps)
        if apres_tout and assez:
            garde, cadre = [], []
            for i, (r, seg) in enumerate(roles):
                if i < min(enonces) or r == "bruit":
                    garde.append(seg); continue
                # la citation reste de lui meme quand elle partage le segment du credit
                for m in GUILLEMETS.finditer(seg): garde.append(m.group(0))
                c = GUILLEMETS.sub(" ", seg).strip()
                if c: cadre.append(c)
            tdl, cad = _recompose(garde), " ".join(cadre).strip() or None
            if _perte(" ".join(roles[i][1] for i in range(min(enonces))) or t, tdl) > 0.4:
                return "david-lisnard", "texte-entier-cadre-non-separable", _recompose([t]), [], None
            return "david-lisnard", "corps-puis-cadre-editorial", tdl, [], cad
        return "equipe", "enonce-sur-lui", None, citations, None
    if REF_EXCLUSIF.search(_anorm(t)):
        # Un credit seul, sans propos ni citation : il ne reste rien de lui.
        if not assez:
            return "equipe", "credit-sans-contenu", None, citations, None
        garde, cadre = [], []
        for r, seg in roles:
            if r == "credit":
                for m in GUILLEMETS.finditer(seg): garde.append(m.group(0))
                c = GUILLEMETS.sub(" ", seg).strip()
                if c: cadre.append(c)
            else: garde.append(seg)
        tdl, cad = _recompose(garde), " ".join(cadre).strip() or None
        if _perte(" ".join(seg for r, seg in roles if r != "credit") or t, tdl) > 0.4:
            return "david-lisnard", "texte-entier-cadre-non-separable", _recompose([t]), [], None
        return "david-lisnard", "citation-creditee", tdl, [], cad
    if compte_proprietaire and compte_proprietaire != "David Lisnard" \
       and not assez and not PREMIERE.search(_anorm(t)):
        return "equipe", "compte-de-l-organisation", None, citations, None
    return "david-lisnard", "compte-officiel", _recompose([t]), [], None
