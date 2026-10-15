# Méthode

Comment ce corpus est construit, et ce que chaque garantie vaut exactement.

## 1. Les sources

| Source | Origine | Traitement |
|---|---|---|
| Discours | vidéos officielles sur YouTube | transcription professionnelle, séparation des locuteurs |
| Interviews | plateaux télé et radio | transcription, puis extraction des seules réponses de David Lisnard |
| Publications | ses comptes Instagram, Facebook, X, LinkedIn, TikTok, YouTube | texte intégral de la publication |
| Programme | `unenouvelleenergie.fr/notre-programme/` | lecture de l'API du site, découpage sur les sections |
| Imprimé | *Ainsi va la France* (2025) | texte intégral, découpé selon la pagination |
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
