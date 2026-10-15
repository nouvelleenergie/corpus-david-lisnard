# Corpus David Lisnard

Corpus textuel des prises de parole publiques de **David Lisnard** et des publications de **Nouvelle Énergie**, sourcé, daté et horodaté, destiné à la recherche, au RAG et à la vérification de citations.

| | |
|---|---|
| Version | **2.0.1** |
| Passages | **4 764** |
| Dont paroles de David Lisnard | **4 461** (`paroles_de_dl`) |
| Mots | **468 688**, dont 409 871 de lui |
| Période couverte | **25 mars 2014 → 11 octobre 2026** |
| Dont 2026 | 2 566 passages |
| Passages horodatés à la seconde | 3 003 |
| Dernière génération | **15 octobre 2026** |
| Format | JSONL, CSV, découpage par thème |

La version et la date de génération font foi dans [`data/stats.json`](data/stats.json). Les changements d'une version à l'autre sont dans [`CHANGELOG.md`](CHANGELOG.md).

> **Filtrez sur `paroles_de_dl`** pour ne travailler que sur ses propres mots. 96 passages sont du texte écrit par la campagne à son sujet : ils restent dans le corpus, étiquetés, parce qu'ils documentent la communication, mais ce ne sont pas ses paroles. Voir [Qui parle](#qui-parle).

## Composition

| `type_source` | Passages | Contenu |
|---|---:|---|
| `interview` | 2 612 | réponses en plateau et en radio, 25 médias |
| `post` | 1 213 | publications des comptes de campagne, dont 96 écrites par l'équipe |
| `discours` | 391 | six prises de parole publiques, transcrites intégralement |
| `tribune` | 277 | 78 tribunes de presse, 14 médias, 2014 à 2024 |
| `book_tribune` | 64 | textes de liaison du recueil *Ainsi va la France* (2025) |
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

### Tribunes de presse

78 tribunes signées ou cosignées par David Lisnard, parues entre 2014 et 2024 : L'Opinion (123 passages), Le Figaro (78), Atlantico (23), Le Journal du dimanche (10), Les Échos (9), Le Monde, Le Point, Marianne, Valeurs actuelles, La Tribune, Nice-matin, Le HuffPost, La Revue politique et parlementaire, 25 millions de propriétaires.

L'inventaire complet des 78 tribunes, avec média, date, cosignataires et volume, est dans [`data/tribunes.json`](data/tribunes.json). 18 d'entre elles sont cosignées ; le champ `cosignataires` les nomme. Ces tribunes sont des imprimés : `url_source` vaut `null` et `reference_papier` porte le crédit de parution, par exemple `L'Opinion, 21 novembre 2024`.

### Médias et plateformes

Interviews : Europe 1 (449), Sud Radio (410), BFMTV (200), franceinfo (180), RMC (176), Public Sénat (162), Le Figaro (129), LCI (113), Le Crayon (85), Grand Angle (83), TF1 (79), CNews (63), et 13 autres.

Publications : X (388), Instagram (381), Facebook (199), YouTube (140), TikTok (60), LinkedIn (45). Le champ `compte_source` donne le compte exact, et `compte_proprietaire` son titulaire, repris de la table des comptes et non devinés du texte.

## Qui parle

Pour l'oral, la séparation des locuteurs répond à la question : ce qui n'est pas de lui est exclu avant le découpage.

Pour l'écrit social, non. Un compte de campagne publie trois choses mélangées, et une seule est de sa main :

| | Exemple | `voix` |
|---|---|---|
| ses mots | « Ces jeunes ont besoin de discipline. » | `david-lisnard` |
| ses mots, plus un crédit | « ... » @davidlisnard hier soir à Benfeld. | `david-lisnard`, crédit déplacé dans `cadre_editorial` |
| du texte sur lui | « @davidlisnard détaille la 5ᵉ phase du projet. » | `equipe` |

Chaque passage porte donc `voix` et le booléen `paroles_de_dl`. Quand un passage est de l'équipe, ce qui s'y trouve entre guillemets ressort dans `citations_entre_guillemets` : rien n'est perdu, mais rien n'est attribué à tort.

Ce champ est un **candidat, pas une citation certifiée**. L'extraction ne retient que les suites de huit mots et plus, pour écarter les titres d'émission et les mots mis en relief, mais elle ne garantit pas que la phrase soit de lui : vérifiez à la source. 14 passages en portent une.

La règle est lexicale, publiée, et tient en un fichier : [`scripts/lib_voix_post.py`](https://github.com/nouvelleenergie/corpus-david-lisnard/blob/main/scripts/lib_voix_post.py). Elle sert à **présélectionner**, pas à décider seule. Les cas qu'un motif ne peut pas trancher, parce qu'ils demandent de lire le sens, ont été relus un par un et chaque décision est publiée avec son motif dans [`data/revision-voix-posts.csv`](data/revision-voix-posts.csv). Exemple de ce que la règle ne voit pas : les publications au format « mythe ou réalité », où les phrases entre guillemets sont les idées reçues qu'il réfute, et non ses positions.

Le détail du compte de chaque méthode est dans `par_methode_voix`, dans [`data/stats.json`](data/stats.json).

## Comment il est constitué

**1. Collecte.** Vidéos depuis les chaînes officielles et les médias. Publications depuis les six comptes de David Lisnard. Programme et fiches depuis l'API Payload du site `unenouvelleenergie.fr`.

**2. Transcription.** ElevenLabs Scribe v1 avec diarisation et horodatage au mot. Pour les documents PDF à deux colonnes, extraction en mode flux (`pdftotext` sans `-layout`, qui autrement entrelace les colonnes). Un livret au format image est passé en reconnaissance optique (`pdftoppm -r 300` puis `tesseract -l fra`).

**3. Attribution du locuteur.** Établie avant tout découpage, sur trois signaux textuels concordants : la concentration des points d'interrogation, qui nomme qui par son nom, et la répartition du temps de parole. Les trois doivent concorder, sinon la source est écartée. **Seules les paroles de David Lisnard entrent ; la parole des journalistes et des autres intervenants est exclue.**

**4. Découpage.** Un passage ne franchit jamais une prise de parole, et les coupes tombent sur des fins de phrase. Les montages d'extraits en ouverture de vidéo et les chants de clôture de meeting sont écartés. Les bornes `t_debut_s` et `t_fin_s` sont calculées sur les horodatages au mot.

**5. Dédoublonnage.** À texte identique, une seule version est conservée, celle qui a obtenu le plus d'engagement d'après les compteurs bruts de la plateforme.

**6. Tribunes.** Les tribunes proviennent du recueil *Ainsi va la France* (2025), qui porte lui-même leur attribution dans sa table des matières, sous la forme `Titre (cosigné avec X, Le Figaro, 12 septembre 2022)`. Cette table est lue, les 78 entrées en sont extraites avec média, date et cosignataires, et chaque passage est rattaché à sa tribune par sa pagination. Les textes de liaison écrits pour le recueil, qui ne sont parus nulle part ailleurs, restent typés `book_tribune`.

**7. Thèmes.** Dérivés par lexique sur le texte, 18 thèmes, sans modèle de langage. Méthode détaillée dans [`docs/METHODE.md`](docs/METHODE.md).

## Schéma

Un objet JSON par ligne dans [`data/corpus.jsonl`](data/corpus.jsonl). Schéma formel : [`schema/corpus.schema.json`](schema/corpus.schema.json).

| Champ | Type | Description |
|---|---|---|
| `id` | chaîne | `sha1(type|source|rang)[:16]`. **Ne dépend pas du texte** : corriger une transcription ne le change pas |
| `cle_source` | chaîne | la même information en clair, `type:source#rang` |
| `voix` | chaîne | `david-lisnard`, `equipe`, `nouvelle-energie`, `nouvelle-energie-site` |
| `paroles_de_dl` | booléen | vrai si `texte` porte ses propres mots. **Le champ sur lequel filtrer** |
| `methode_voix` | chaîne | la règle qui a établi `voix` |
| `citations_entre_guillemets` | liste | quand `voix` vaut `equipe`, ce qui est entre guillemets dans ce passage. Candidat à vérifier, pas une citation certifiée |
| `cadre_editorial` | chaîne | crédit ou appel à l'action retiré de `texte` parce qu'il n'est pas de lui |
| `compte_source` | chaîne | compte de publication, `plateforme/identifiant` |
| `compte_proprietaire` | chaîne | titulaire de ce compte |
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
| `cosignataires` | chaîne | pour une tribune cosignée |
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

- **96 passages sont du texte de campagne sur lui**, pas de lui : descriptifs de vidéo, comptes rendus de déplacement, communication municipale. Ils sont étiquetés `voix: equipe` et `paroles_de_dl: false`. Filtrez.
- **La règle d'attribution de l'écrit social est lexicale.** Elle ne lit pas le sens. Elle manque le compte tiers qui raconte un événement sans jamais prendre David Lisnard pour sujet. Les cas repérés sont corrigés dans `data/revision-voix-posts.csv` ; il en reste probablement.
- **3 003 passages sur 4 764 portent un timecode.** Pour ceux-là, `url_source` ouvre la vidéo à la seconde exacte. Vérifiez à l'écoute avant toute citation publique.
- **708 passages ont une transcription professionnelle vérifiée.** Les autres viennent d'une extraction antérieure, fiable sur le fond, moins sur la ponctuation.
- **2 470 passages sur 4 764 se terminent sur une ponctuation.** Filtrez sur `extrait_complet` pour citer mot à mot.
- **1 012 passages restent en thème « divers »**, pour l'essentiel des fragments de moins de 25 mots. Les thèmes sont une aide au tri, pas une classification de référence.
- **271 passages n'ont pas de date** : textes mis à jour en continu ou sources imprimées.
- Les positions évoluent. Datez toujours une citation.

## Licence

Code d'exemple sous licence MIT. Les textes restent la propriété de leurs auteurs et sont fournis sourcés et liés à leur original. Voir [`LICENCE.md`](LICENCE.md).

Une erreur d'attribution, une citation tronquée, une date fausse ? Ouvrez une issue, la correction sera faite à la source. Les identifiants ne bougeront pas pour autant : ils ne dépendent pas du texte.
