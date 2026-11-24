# Journal des versions

Les identifiants (`id`) ne dépendent pas du texte. Toute version qui les déplace le dit ici,
avec sa table de correspondance.

## 2.1.0, 24 novembre 2026

**6 081 passages** (+1 317), dont 5 712 portant les paroles de David Lisnard. Aucun passage retiré, **aucun identifiant
déplacé** : les 4 764 passages de la 2.0.1 sont tous retrouvés sous le même `id`. Un seul ancien
passage change de contenu, celui qui est requalifié dans la section Attribution.

### Ajouts

- **473 passages d'interview** : BFMTV (« 100 % Mabrouk », « Le Grand Oral » avec Le Figaro), Europe 1,
  RMC, LCI, RTL, Nice-Matin et Var-matin, Maires de France, TF1, « Et si l'économie sauvait l'écologie ? »,
  et le DLive. Pour ces vidéos, le locuteur est établi sur preuve de texte et chaque passage a passé un
  contrôle de contamination, voir le README.
- **9 passages de discours** : Cannes, hôtel de ville, 19 octobre 2026.
- **835 publications** des comptes de campagne, dont **508 publications X de 2010 à 2025**. Le corpus
  remonte désormais à février 2010.

### Attribution

- **26 publications sont passées de `david-lisnard` à `equipe`** après relecture, dont une déjà publiée
  dans la 2.0.1 : questions « vrai ou faux », phrases « mythe ou réalité », titres d'articles repris,
  retweet, texte d'un tiers. Les décisions et leur motif sont dans
  [`data/revision-voix-posts.csv`](data/revision-voix-posts.csv).
- `equipe` passe de 96 à 162 passages.

### Nouveau champ

- **`texte_prolonge_automatiquement`** : vrai pour 608 interviews dont la fin a été prolongée
  automatiquement jusqu'à une fin de phrase. Sur un échantillon de 60, environ 18 % de ces prolongements
  recollaient une relance de l'intervieweur. Le champ permet de les écarter. Ils n'ont pas été retraités.
- Le schéma est mis à jour.

## 2.0.1 — 15 octobre 2026

Correction d'un défaut de la 2.0.0, trouvé en relisant ce qu'elle publiait.

- `citation_dl` est renommé **`citations_entre_guillemets`**, parce que son nom promettait plus
  que son contenu. L'extraction attrapait les titres d'émission (« 8h30 franceinfo »), les noms
  de campus (« Laissez-nous faire ») et les mots mis en relief (« résistance »), tous présentés
  comme des paroles de David Lisnard. Seules les suites de **huit mots ou plus** sont retenues,
  et le champ est désormais documenté comme un **candidat à vérifier**, pas une citation
  certifiée. 14 passages en portent une, contre 23 avant.
- Les onze décisions relues à la main tranchent maintenant aussi sur la citation, colonne
  `citation` de [`data/revision-voix-posts.csv`](data/revision-voix-posts.csv). Sans elle,
  l'extraction automatique publiait les « mythes » réfutés comme ses positions, et la phrase de
  Boualem Sansal à son sujet comme une citation de lui.

Aucun passage ajouté ni retiré, aucun identifiant déplacé.

## 2.0.0 — 15 octobre 2026

**4 764 passages**, dont 4 461 portant les paroles de David Lisnard.

### Attribution de l'écrit social

Jusqu'ici, toute publication des comptes de campagne portait `locuteur: David Lisnard`. C'était
faux pour une partie d'entre elles : descriptifs de vidéo rédigés par l'équipe, comptes rendus
de déplacement, communication municipale, citations d'autres intervenants.

- Deux champs nouveaux, **`voix`** et **`paroles_de_dl`**, sur tous les passages. Filtrez sur
  `paroles_de_dl` pour n'avoir que ses mots.
- **96 passages** sont désormais étiquetés `voix: equipe`. Ils restent dans le corpus parce
  qu'ils documentent la communication de campagne, mais ils ne lui sont plus attribués.
- Quand un passage d'équipe porte une phrase entre guillemets, elle ressort dans
  **`citation_dl`** (renommé `citations_entre_guillemets` en 2.0.1).
- Le crédit ajouté sous ses mots (« @davidlisnard hier soir à Benfeld ») sort de `texte` et passe
  dans **`cadre_editorial`**. 122 passages sont concernés.
- **`compte_source`** et **`compte_proprietaire`** donnent le compte de publication et son
  titulaire, rattachés par l'adresse de la publication à la table des comptes de la collecte.
  Ils ne sont pas déduits du texte. Les 1 213 publications sont toutes rattachées.
- La règle est publiée dans [`scripts/lib_voix_post.py`](scripts/lib_voix_post.py), ses cas de
  test dans [`scripts/test_voix_post.py`](scripts/test_voix_post.py), et les décisions relues à
  la main dans [`data/revision-voix-posts.csv`](data/revision-voix-posts.csv).

### Identifiants stables

- `id` valait `sha1(type|source|texte[:200])`. Il changeait donc à chaque correction de texte,
  ce qui rendait impossible de construire dessus.
- `id` vaut maintenant `sha1(type|source|rang dans la source)`, tronqué à 16 caractères.
  **Le texte n'entre plus dans le calcul.**
- La correspondance complète entre les deux est dans
  [`data/ids-v1-vers-v2.csv`](data/ids-v1-vers-v2.csv).
- **`cle_source`** porte la même information en clair : `type:source#rang`.

### Effets de bord

- 16 passages en moins. Ce sont des doublons que la version 1 ne voyait pas : une fois le cadre
  éditorial retiré, la même citation publiée sur deux réseaux devient identique et n'est plus
  comptée qu'une fois.
- `locuteur` accepte une quatrième valeur, `Nouvelle Énergie (équipe)`.
- Le schéma exige désormais `cle_source`, `voix` et `paroles_de_dl`.

## 1.1.0 — 15 octobre 2026

- Le recueil *Ainsi va la France* (2025) est découpé en **78 tribunes de presse** datées et
  créditées, lues dans la table des matières de l'ouvrage. 277 passages passent de
  `book_tribune` à `tribune` et reçoivent média, date et cosignataires.
- Inventaire des 78 tribunes dans [`data/tribunes.json`](data/tribunes.json).
- Les 64 textes de liaison, écrits pour le recueil et parus nulle part ailleurs, restent typés
  `book_tribune`.

## 1.0.0 — 15 octobre 2026

Première publication. 4 780 passages, 25 mars 2014 au 11 octobre 2026.
