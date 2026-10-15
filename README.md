# Corpus David Lisnard

Corpus textuel des prises de parole publiques de **David Lisnard** et des publications de **Nouvelle Énergie**, sourcé, daté et horodaté, destiné à la recherche, au RAG et à la vérification de citations.

| | |
|---|---|
| Passages | **4 780** |
| Mots | **470 449** |
| Période couverte | **25 mars 2014 → 11 octobre 2026** |
| Dont 2026 | 2 582 passages |
| Passages horodatés à la seconde | 3 003 |
| Dernière génération | **15 octobre 2026** |
| Format | JSONL, CSV, découpage par thème |

La date de génération fait foi dans [`data/stats.json`](data/stats.json).

## Composition

| `type_source` | Passages | Contenu |
|---|---:|---|
| `interview` | 2 612 | réponses en plateau et en radio, 25 médias |
| `post` | 1 229 | publications sur ses comptes |
| `discours` | 391 | six prises de parole publiques, transcrites intégralement |
| `book_tribune` | 341 | *Ainsi va la France* (2025) |
| `programme` | 157 | programme officiel du site et documents PDF associés |
| `fiche_2027` | 50 | questions-réponses du site de campagne |

### Discours

| Date | Lieu | Passages | Mots |
|---|---|---:|---:|
| 20/01/2026 | Maison de la Mutualité, Paris | 73 | 14 294 |
| 22/04/2026 | « En finir avec la bureaucratie » | 56 | 10 617 |
| 17/06/2026 | Bayeux, sur les institutions | 31 | 5 708 |
| 03/07/2026 | Saint-Raphaël | 79 | 15 204 |
| 29/08/2026 | Campus de La Gagne, Cannes | 85 | 16 748 |
| 25/09/2026 | Benfeld, Alsace | 67 | 13 194 |

### Médias et plateformes

Interviews : Europe 1 (449), Sud Radio (410), BFMTV (200), franceinfo (180), RMC (176), Public Sénat (162), Le Figaro (129), LCI (113), Le Crayon (85), Grand Angle (83), TF1 (79), CNews (63), et 13 autres.

Publications : X (394), Instagram (384), Facebook (200), YouTube (146), TikTok (61), LinkedIn (44).

## Comment il est constitué

**1. Collecte.** Vidéos depuis les chaînes officielles et les médias. Publications depuis les six comptes de David Lisnard. Programme et fiches depuis l'API Payload du site `unenouvelleenergie.fr`.

**2. Transcription.** ElevenLabs Scribe v1 avec diarisation et horodatage au mot. Pour les documents PDF à deux colonnes, extraction en mode flux (`pdftotext` sans `-layout`, qui autrement entrelace les colonnes). Un livret au format image est passé en reconnaissance optique (`pdftoppm -r 300` puis `tesseract -l fra`).

**3. Attribution du locuteur.** Établie avant tout découpage, sur trois signaux textuels concordants : la concentration des points d'interrogation, qui nomme qui par son nom, et la répartition du temps de parole. Les trois doivent concorder, sinon la source est écartée. **Seules les paroles de David Lisnard entrent ; la parole des journalistes et des autres intervenants est exclue.**

**4. Découpage.** Un passage ne franchit jamais une prise de parole, et les coupes tombent sur des fins de phrase. Les montages d'extraits en ouverture de vidéo et les chants de clôture de meeting sont écartés. Les bornes `t_debut_s` et `t_fin_s` sont calculées sur les horodatages au mot.

**5. Dédoublonnage.** À texte identique, une seule version est conservée, celle qui a obtenu le plus d'engagement d'après les compteurs bruts de la plateforme.

**6. Thèmes.** Dérivés par lexique sur le texte, 18 thèmes, sans modèle de langage. Méthode détaillée dans [`docs/METHODE.md`](docs/METHODE.md).

## Schéma

Un objet JSON par ligne dans [`data/corpus.jsonl`](data/corpus.jsonl). Schéma formel : [`schema/corpus.schema.json`](schema/corpus.schema.json).

| Champ | Type | Description |
|---|---|---|
| `id` | chaîne | identifiant stable dérivé du contenu |
| `texte` | chaîne | le passage |
| `locuteur` | chaîne | `David Lisnard`, ou Nouvelle Énergie pour les textes officiels |
| `attribution` | chaîne | méthode d'établissement du locuteur |
| `type_source` | chaîne | voir le tableau de composition |
| `titre_source` | chaîne | émission, partie ou section |
| `media` | chaîne | média, lieu ou ouvrage |
| `url_source` | chaîne | lien vers l'original, horodaté pour l'oral ; `null` pour un imprimé |
| `reference_papier` | chaîne | référence paginée, pour les sources imprimées |
| `date` | chaîne | `AAAA-MM-JJ`, date de l'intervention et non de la mise en ligne |
| `precision_date` | chaîne | `jour`, ou `null` |
| `lieu`, `plateforme` | chaîne | contexte |
| `t_debut_s`, `t_fin_s`, `duree_s` | entier | position et durée dans la vidéo, en secondes |
| `video_id` | chaîne | identifiant YouTube |
| `themes` | liste | jusqu'à trois thèmes |
| `nb_mots` | entier | longueur du passage |
| `extrait_complet` | booléen | le passage se termine sur une ponctuation |
| `transcription_verifiee` | booléen | transcription professionnelle avec séparation des locuteurs |

## Démarrer

```python
import json
corpus = [json.loads(l) for l in open("data/corpus.jsonl", encoding="utf-8")]
```

Recherche par mots, sans dépendance :

```bash
python3 exemples/recherche_simple.py "retraite capitalisation" --depuis 2026-01-01
```

Recherche sémantique, vecteurs calculés une fois et mis en cache :

```bash
pip install numpy openai && export OPENAI_API_KEY=sk-...
python3 exemples/recherche_semantique.py "financer la retraite par capitalisation"
```

Les vecteurs ne sont pas versionnés : ils dépendent du modèle et pèsent 27 Mo. Les recalculer coûte moins de deux centimes.

## Limites

- **3 003 passages sur 4 780 portent un timecode.** Pour ceux-là, `url_source` ouvre la vidéo à la seconde exacte. Vérifiez à l'écoute avant toute citation publique.
- **708 passages ont une transcription professionnelle vérifiée.** Les autres viennent d'une extraction antérieure, fiable sur le fond, moins sur la ponctuation.
- **2 350 passages sur 4 780 se terminent sur une ponctuation.** Filtrez sur `extrait_complet` pour citer mot à mot.
- **1 013 passages restent en thème « divers »**, pour l'essentiel des fragments de moins de 25 mots. Les thèmes sont une aide au tri, pas une classification de référence.
- **548 passages n'ont pas de date** : textes mis à jour en continu ou sources imprimées.
- Les positions évoluent. Datez toujours une citation.

## Licence

Code d'exemple sous licence MIT. Les textes restent la propriété de leurs auteurs et sont fournis sourcés et liés à leur original. Voir [`LICENCE.md`](LICENCE.md).

Une erreur d'attribution, une citation tronquée, une date fausse ? Ouvrez une issue, la correction sera faite à la source.
