# Méthode

Comment ce corpus est construit, et ce que chaque garantie vaut exactement.

## 1. Les sources

| Source | Origine | Traitement |
|---|---|---|
| Discours | vidéos officielles sur YouTube | transcription professionnelle, séparation des locuteurs |
| Interviews | plateaux télé et radio | transcription, puis extraction des seules réponses de David Lisnard |
| Publications | ses comptes Instagram, Facebook, X, LinkedIn, TikTok, YouTube | texte intégral de la publication |
| Programme | `unenouvelleenergie.fr/notre-programme/` | lecture de l'API du site, découpage sur les sections |
| Tribunes | presse, 2014 à 2024 | 78 tribunes, attribution lue dans la table des matières du recueil |
| Recueil | *Ainsi va la France* (2025) | textes de liaison seuls, le reste étant typé en tribunes |
| Fiches 2027 | site de campagne | questions-réponses officielles |

## 2. Établir qui parle

C'est l'étape qui conditionne tout le reste. Une transcription automatique rend un texte continu où la question du journaliste et la réponse de l'invité se suivent sans marque. Reprendre ce texte tel quel et l'attribuer à l'invité produit de fausses citations.

La séparation automatique des voix ne suffit pas non plus : elle se trompe de locuteur, et elle n'est pas déterministe d'un passage à l'autre sur un même fichier.

Nous établissons donc le locuteur sur **trois signaux textuels concordants**, avant tout découpage :

1. **Qui pose les questions.** Le journaliste concentre les points d'interrogation, dans un rapport typique de trois à dix contre un.
2. **Qui nomme qui.** Le journaliste dit « David Lisnard » ; David Lisnard ne se nomme jamais lui-même. Ce signal est le plus discriminant.
3. **Le temps de parole.** Dans un entretien, l'invité occupe très majoritairement l'antenne. Un déséquilibre inverse signale une erreur d'attribution.

Les trois doivent concorder. Si l'un diverge, la vidéo n'entre pas dans le corpus.

Le champ `attribution` conserve la méthode appliquée à chaque passage.

## 2 bis. Qui parle dans une publication de réseau social

Les trois signaux ci-dessus valent pour l'oral. Ils ne valent pas pour l'écrit : une publication n'a pas de tour de parole, et un compte de campagne publie trois choses mélangées.

| | Exemple | `voix` |
|---|---|---|
| ses mots | « Ces jeunes ont besoin de discipline. » | `david-lisnard` |
| ses mots, plus un crédit | « ... » @davidlisnard hier soir à Benfeld. | `david-lisnard` |
| du texte sur lui | « @davidlisnard détaille la 5ᵉ phase du projet. » | `equipe` |

**La provenance d'abord, et elle ne se devine pas.** Chaque publication est rattachée à son compte par son adresse, et le compte à son titulaire par la table des comptes de la collecte. `compte_source` et `compte_proprietaire` sortent de là, pas d'une lecture du texte. 96 passages viennent de comptes qui ne sont pas les siens, ou portent du texte écrit sur lui.

**Ensuite le texte.** Le passage est découpé en segments, les citations étant masquées d'abord pour ne pas être coupées. Chaque segment qui le désigne est pesé :

- au-delà de six mots utiles autour de la mention, ce n'est plus un crédit, c'est un **énoncé sur lui** ;
- un énoncé placé **avant ou entre** les segments de contenu fait basculer le passage du côté de l'équipe. C'est le cas des descriptifs de vidéo (« David Lisnard était l'invité du 7h30 de franceinfo, interrogé par Alix Bouilhaguet ») et des comptes rendus de déplacement ;
- un énoncé placé **après tout le contenu** est un cadre éditorial, crédit ou appel à l'action ajouté sous ses mots. Le texte reste de lui, le cadre part dans `cadre_editorial` et sort de `texte`.

Les passages entre guillemets restent toujours de lui. Quand le passage est classé `equipe`, ils ressortent dans `citation_dl` : rien n'est perdu, mais rien n'est attribué à tort.

**Deux garde-fous.** Les liens sont retirés avant toute détection, parce qu'une adresse porte souvent son nom (`/interview-exclusive-de-david-lisnard-sur-cannes-radio`). Et si la séparation du cadre fait perdre plus de 40 % des mots du passage, elle est abandonnée et le texte entier est publié tel quel : mieux vaut un crédit résiduel qu'une citation tronquée.

**Ce que la règle ne sait pas faire.** Elle est lexicale, elle ne lit pas le sens. Elle ne voit pas le compte tiers qui raconte un événement sans jamais le prendre pour sujet, ni les publications au format « mythe ou réalité », où les phrases entre guillemets sont les idées reçues qu'il réfute et non ses positions. La règle sert donc à **présélectionner**. Les cas qu'un motif ne peut pas trancher ont été relus un par un, et chaque décision est publiée avec son motif dans [`../data/revision-voix-posts.csv`](../data/revision-voix-posts.csv). Le code de la règle est dans [`../scripts/lib_voix_post.py`](../scripts/lib_voix_post.py).

## 2 ter. Les identifiants

`id` vaut `sha1(type_source|source|rang dans la source)` tronqué à seize caractères. **Le texte n'entre pas dans le calcul.** Corriger une transcription, retirer un crédit, réparer une ponctuation : l'identifiant ne bouge pas. C'est ce qui permet de construire dessus.

Il ne change que si une source est réextraite et que le rang des passages s'en trouve modifié. Ce cas est annoncé dans [`../CHANGELOG.md`](../CHANGELOG.md), avec la table de correspondance entre l'ancien et le nouvel identifiant. La version 1 calculait l'identifiant sur le texte : la correspondance avec la version 2 est dans [`../data/ids-v1-vers-v2.csv`](../data/ids-v1-vers-v2.csv).

`cle_source` porte la même information en clair, sous la forme `type:source#rang`.

## 3. Découper sans fabriquer de fausses citations

Deux règles.

**Un passage ne franchit jamais une prise de parole.** Sans cette règle, les répliques successives d'un même locuteur, séparées de plusieurs minutes, se recollent en un verbatim continu qu'il n'a jamais prononcé d'un trait. Une courte relance du journaliste, du type « oui, bien sûr », ne coupe pas la réponse en deux ; une vraie question, si.

**Les coupes tombent sur des fins de phrase**, et de préférence sur une respiration réelle de l'orateur. Le champ `extrait_complet` indique si le passage se termine effectivement sur une ponctuation.

Pour les discours et les entretiens récents, les bornes sont calculées au mot près à partir des horodatages de la transcription : `t_debut_s` et `t_fin_s` sont les secondes réelles, et `url_source` ouvre la vidéo à cet instant.

## 4. Les montages d'ouverture

Beaucoup de vidéos s'ouvrent sur un montage d'extraits pris plus loin dans l'entretien. Les inclure produirait des citations assemblées au montage, avec des timecodes faux. Ces ouvertures sont systématiquement écartées, après vérification que leur contenu se retrouve bien dans le corps de l'entretien.

De la même façon, les meetings se terminent souvent par un chant ou des slogans du public, captés sous la voix de l'orateur. Ils sont écartés : ce ne sont pas ses mots.

## 4 bis. Les documents PDF

Les pages du programme portent des livrets au format PDF, plus détaillés que le texte des pages
elles-mêmes. Ils sont inclus en texte intégral : *Les Carnets — Agriculture*, *Les Carnets —
Santé*, et *Le Livre noir — En finir avec la bureaucratie*.

Deux pièges, notés ici parce qu'ils produisent un texte faux sans prévenir :

**Les livrets sont composés sur deux colonnes.** Une extraction qui respecte la mise en page lit
ligne à ligne en travers des colonnes et entrelace deux phrases différentes, ce qui donne un
texte grammaticalement plausible et factuellement absurde. Il faut au contraire suivre l'ordre
du document, qui rend chaque colonne entière.

**Le carnet Agriculture est un PDF composé d'images**, sans couche de texte. Son contenu provient
d'une reconnaissance optique de caractères. Le corps du document est propre, mais des coquilles
sont possibles, en particulier sur les chiffres et les noms propres. Le champ `ocr` de la
classification le signale en interne.

## 4 ter bis. Du recueil aux tribunes

*Ainsi va la France* (2025) est un recueil : des tribunes déjà parues dans la presse, reliées par
des textes écrits pour l'ouvrage. Le livre porte son attribution dans sa propre table des matières :

    Peut-on arrêter la décivilisation ? (cosigné avec Naïma M'Faddel et Maurice Berger,
    Le Figaro, 12 septembre 2022) ........................ 360

Cette table est analysée, et chaque passage est rattaché à sa tribune par la pagination. Le
résultat est vérifiable : **78 tribunes, qui reçoivent toutes du texte, 0 passage non rattaché**.
277 passages sur 341 tombent dans une tribune, soit 81 % du recueil ; les 64 autres sont les
textes de liaison, qui ne sont parus nulle part ailleurs et restent typés `book_tribune`.

L'attribution vient donc de l'éditeur lui-même, pas d'une reconstitution de notre part. Nous
n'avons en revanche **pas vérifié article par article en ligne** : la plupart de ces tribunes
sont derrière un péage et mal indexées.

## 4 ter. Les sources imprimées

Une source imprimée n'a pas d'URL : `url_source` vaut `null` et `reference_papier` porte la
référence paginée. Le découpage suit la pagination, ce qui explique qu'un passage puisse
commencer en milieu de phrase ; `extrait_complet` le signale.

## 5. Les dates

`date` est la date de l'intervention, pas celle de la mise en ligne de la vidéo. Les deux diffèrent souvent de plusieurs jours, parfois de plusieurs semaines.

Quand aucune date ne peut être établie avec certitude, c'est la date de publication qui est retenue, et c'est signalé. Les textes du programme, mis à jour en continu, n'ont pas de date : `precision_date` vaut alors
`null`. Les sources imprimées non plus : seule l'année de parution est connue, elle figure
dans `reference_papier`.

## 6. Les thèmes

Les thèmes sont dérivés **par lexique**, sur le texte du passage : une liste de mots-clés par thème, appliquée après normalisation des accents, les trois thèmes les mieux servis étant retenus. La méthode est volontairement simple et reproductible, sans modèle de langage, donc sans risque d'invention.

Sa limite est connue et mesurée : les passages de moins de vingt-cinq mots n'offrent pas assez de prise et retombent en « divers », soit un peu moins d'un quart du corpus. **Les thèmes sont une aide au tri, pas une classification de référence.** Pour un travail sérieux sur un sujet, préférez une recherche sémantique sur le texte.

Le lexique complet est lisible dans le script d'export : il tient en dix-huit lignes.

## 7. Dédoublonnage

Le même texte publié sur plusieurs réseaux n'apparaît qu'une fois. À contenu identique, la version retenue est celle qui a obtenu le plus d'engagement, mesuré sur les compteurs bruts de la plateforme.

## 8. Ce que nous ne garantissons pas

- Que chaque mot soit transcrit exactement. Une transcription automatique se trompe sur les noms propres et les chiffres. **Vérifiez à l'écoute avant toute citation publique**, le timecode est là pour ça.
- Que le corpus soit exhaustif. Il couvre les prises de parole repérées par notre veille, pas la totalité des interventions.
- Que les positions soient à jour. Elles évoluent ; datez toujours.
