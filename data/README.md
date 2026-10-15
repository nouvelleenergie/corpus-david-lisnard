# Fichiers de données

| Fichier | Contenu |
|---|---|
| `corpus.jsonl` | le corpus complet, un objet JSON par ligne. **C'est le fichier de référence.** |
| `corpus.csv` | les mêmes données en tableau ; la colonne `themes` est une liste séparée par des barres verticales |
| `themes/*.jsonl` | le corpus réparti par thème principal |
| `tribunes.json` | inventaire des 78 tribunes : titre, média, date, cosignataires, volume |
| `stats.json` | compteurs et date de génération |

Les vecteurs d'embedding ne sont pas versionnés : ils dépendent du modèle choisi et pèseraient
27 Mo à chaque régénération. `exemples/recherche_semantique.py` les calcule et les met en cache
en une commande, pour moins de deux centimes.
