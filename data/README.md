# Fichiers de données

| Fichier | Contenu |
|---|---|
| `corpus.jsonl` | le corpus complet, un objet JSON par ligne. **C'est le fichier de référence.** |
| `corpus.csv` | les mêmes données en tableau ; la colonne `themes` est une liste séparée par des barres verticales |
| `themes/*.jsonl` | le corpus réparti par thème principal |
| `tribunes.json` | inventaire des 78 tribunes : titre, média, date, cosignataires, volume |
| `stats.json` | version, compteurs et date de génération |
| `revision-voix-posts.csv` | les décisions d'attribution relues à la main, avec leur motif |
| `ids-v1-vers-v2.csv` | correspondance des identifiants entre la version 1 et la version 2 |

Les vecteurs d'embedding ne sont pas versionnés : ils dépendent du modèle choisi et pèseraient
27 Mo à chaque régénération. `exemples/recherche_semantique.py` les calcule et les met en cache
en une commande, pour moins de deux centimes.

## Le champ sur lequel filtrer

`paroles_de_dl` dit si `texte` porte les mots de David Lisnard. 96 passages valent `false` :
ce sont des textes écrits par la campagne à son sujet, conservés parce qu'ils documentent la
communication, mais qui ne lui sont pas attribués. Quand l'un d'eux le cite entre guillemets,
la citation est dans `citation_dl`.

```python
import json
corpus = [json.loads(l) for l in open("data/corpus.jsonl", encoding="utf-8")]
lui = [e for e in corpus if e["paroles_de_dl"]]      # 4 461 passages
```

## Les identifiants

`id` vaut `sha1(type_source|source|rang dans la source)[:16]`. **Le texte n'entre pas dans le
calcul** : une correction de transcription ne déplace pas l'identifiant. Voir
[`../CHANGELOG.md`](../CHANGELOG.md).
