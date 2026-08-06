OBO travaille beaucoup depuis une semaine, quasiment 24h sur 24. Il est à la fois créateur d’images, scénariste/metteur en scène, responsable de la postproduction et des VFX, ingé son, développeur. C’est juste incroyable de se dire qu’un simple ordinateur qui a déjà quelques années est capable de faire autant de choses en même temps.
Il m’aide aussi à trouver des solutions créatives à des problèmes: Un des plus importants actuellement est que, si je veux de l’IA respectable au point de vue énergétique, je reste assez limité en ressources, les créations de vidéos en grande quantité chez soi, ce n’est pas comme via un datacenter qui fonctionne à plein tube en détruisant des espaces qui devraient être verts…

On a discuté de plusieurs pistes: La première était de diminuer la qualité, je n’en voulais évidemment pas. La deuxième piste était de faire de la vidéo avec moins de temps de vidéos, c’est une idée mais comment l’appliquer? Diminuer la vitesse n’était pas une option, le rythme doit être soutenu et regardable, et c’est là que j’ai eu l’idée, et que OBO m’a aidé à la mettre en place en moins d’une heure: Imaginez une image sans fin, un panning de la caméra de gauche à droite, de droite à gauche… Ou dans mon premier exemple de bas en haut. Cette idée d’appartements infinis, elle ne date pas d’hier, mais je n’avais pas les compétences techniques pour l’appliquer de manière animée, l’IA m’a permis non seulement de la mettre en oeuvre mais aussi d’aller un peu plus loin…
Nous avons donc conçu un script qui assemble les images entres elles, il peut fabriquer une tour d’images infinie comme il peut les assembler horizontalement, puis, avec une caméra virtuelle, elle parcourt cet assemblage de bas en haut, de haut en bas, de droite à gauche, de gauche à droite,... Pas de limites de qualité ni de résolution, pas besoin de générer de longues vidéos pour arriver à une certaine durée, mon premier essai était sans appel: 38 images pour une vidéo de 20 minutes!

C’était déjà bien mais il me manquait le petit détail pour rendre ça parfait. C’est bien beau de voir défiler un paysage, mais toutes ces personnes dessus sont bien statiques… Et si on était capable de leur insuffler la vie? J’ai donc eu une nouvelle discussion avec l’IA après avoir imaginé le concept: Au lieu d’intégrer une image entre 2 autres, que se passerait-il si j’intégrais une vidéo? Une sorte de loop où mes personnages animés plutôt que figés évolueraient dans leur cadre statique? C’est ce que j’ai demandé comme j’ai pu. Après m’avoir compris une fois de travers, l’IA a compris qu’il fallait assurer la continuité et le rythme du mouvement, mais ne pas utiliser d’image fixe pour cette partie, plutôt chaque frame d’une vidéo l’une après l’autre, et reboucler à la fin. Résultat: Les personnes sur ma vidéo bougent pendant que la caméra passe à leur niveau, c’était juste extraordinaire, ce que j’avais imaginé. J’ai donc converti quelques images en vidéo, localement et voici le résultat final.

Le script pour réaliser cet accolage est super simple, vous lui indiquez un dossier avec vos images et/ou vidéos, la direction (horizontale ou verticale) et il vous réalise votre panning. J’ai profité de la longueur de cette vidéo pour vous mettre en avant une petite playlist calme de quelques beaux morceaux qu’OBO a créé en local il y a quelques jours.
Mon workflow:
- Pour générer le code, j’ai utilisé Hermes et un modèle local Qwen3.6-35B Q2_K_P qui fonctionne très bien en agentique sur ma carte graphique RTX4080.
- Générer des images selon un thème, qui assureraient une certaine continuité si elles étaient assemblées (comfyui, modèle d’image z-image turbo). Pour du 16:9 panning vertical, j’ai généré mes images en 9:16. Exemple de prompt pour les images (j’ai demandé plusieurs variantes via Hermes avec de nombreux styles mélangés pour les buildings comme art déco, brutalisme, constructivisme russe, néo‑mauresque, etc…):
Photographie urbaine ultra détaillée capturée de nuit dans une brume chaude, cadrée serrée sur une façade composite occupée entièrement par des buildings, sans aucune ouverture vers le ciel. La paroi est un collage architectural où quatre styles se mélangent : style paquebot avec lignes horizontales et hublots, néo‑mudéjar avec briques et arcs outrepassés, minimalisme coréen avec surfaces épurées, et cyber‑gothique avec métal et néons. La brume se loge entre les façades, autour des balcons, devant certaines fenêtres, créant des halos autour des sources lumineuses. Au bas du cadre, une bande de façades mixtes s’étend. À gauche, un immeuble style paquebot présente une façade blanche avec des lignes horizontales, des fenêtres en bandeaux, des balcons arrondis avec garde‑corps chromés. Sur un balcon, une personne est debout, silhouette découpée, mains posées sur la rambarde, visage tourné vers l’extérieur. La lumière intérieure, jaune pâle, se répand sur les surfaces lisses et sur les traits du visage, révélant les yeux, la courbe du nez, la ligne des lèvres dans une expression attentive. Au centre en bas, une portion néo‑mudéjar se manifeste : façade en brique rouge, avec des arcs outrepassés, des frises géométriques, des balcons avec garde‑corps en fer forgé formant des motifs étoilés. Sur un balcon, une personne est assise sur une chaise, jambes croisées, mains tenant un verre, visage tourné vers un autre balcon. La lumière d’une applique extérieure projette des reflets sur la brique et sur le visage, accentuant les traits, les yeux, les lèvres. À droite du bas, un bloc minimaliste coréen domine : façade en béton lisse, fenêtres régulières, balcons simples avec garde‑corps en verre. Sur un balcon, une personne est penchée, mains posées sur un garde‑corps, visage tourné vers le bas. La lumière vient d’une lampe intérieure, dessinant des contrastes doux sur le visage, les traits nets, les yeux plissés, la bouche fermée dans une expression intense. À côté, une façade cyber‑gothique apparaît : surfaces en métal sombre, néons colorés intégrés, garde‑corps en grille métallique. Sur un balcon, une personne est assise sur un banc, mains posées sur les genoux, yeux mi‑clos, expression calme. La lumière des néons se diffuse sur les surfaces métalliques et sur le visage, créant une transition régulière entre lumière et ombre. En montant dans l’image, les styles continuent de se croiser. Des étages paquebot, avec leurs lignes horizontales, surgissent au‑dessus de plateaux néo‑mudéjar; des volumes minimalistes coréens se trouvent à côté de façades cyber‑gothiques. Les balcons se multiplient, chacun avec sa signature : chromé paquebot, fer forgé mudéjar, verre minimaliste, métal cyber‑gothique. Sur certains, des personnes sont en action : une silhouette paquebot ferme des volets; une personne sur un balcon mudéjar ajuste une lampe; quelqu’un sur un balcon minimaliste se penche pour regarder vers un étage inférieur; sur un balcon cyber‑gothique, quelqu’un marche lentement d’un côté à l’autre, mains derrière le dos. La lumière nocturne dans la brume crée une ambiance chaude et enveloppante. Les sources intérieures, dans les façades paquebot et mudéjar, sont souvent des lumières plus décoratives, avec des teintes dorées; dans les blocs minimalistes et cyber‑gothiques, certains éclairages sont plus fonctionnels, plus blancs ou légèrement verdâtres. La brume mélange ces teintes, créant des halos aux contours flous autour des fenêtres et des lampes extérieures. Les surfaces paquebot prennent des teintes blanches; les motifs mudéjar reflètent des lueurs dorées; les volumes minimalistes restent plus froids, mais les angles sont adoucis; les façades cyber‑gothiques montrent des dégradés subtiles. Le cadrage serré, sans ciel, donne à la paroi composite une présence écrasante mais fascinante. La profondeur de champ est grande; les textures fines des lignes paquebot, des briques mudéjar, du béton minimaliste, du métal cyber‑gothique sont toutes lisibles. Les visages et corps aux balcons et fenêtres restent à une échelle où leurs micro‑expressions sont perceptibles, mais intégrés dans un ensemble où chaque personne est une note dans une partition visuelle architecturale.
- Je ne voulais pas d’ordre particulier donc j’ai utilisé un petit script python qui renomme tous mes fichiers 1.png, 2.png, … Dans un ordre totalement aléatoire
- Générer des vidéos à partir de certaines images (J’ai utilisé Wan mais maintenant je recommanderais plutôt Minimax H3 pour plus de qualité), pour mon exemple, 1 image sur 6 est animée. Ce qui fait 6 vidéos. Remplacer les png par des mp4. Mon prompt pour chaque vidéo: video of people living in their flats and balconies, walking, moving, no talking, totally fixed camera, no camera movement at all
- Utiliser un upscaler pour les images et les vidéos, pour améliorer la qualité et standardiser la résolution (j’ai utilisé une résolution de 2160x3840, avec mon propre upscaler qui ajoute des détails mais on peut utiliser d’autres upscaler sur comfyui ou encore des applications qui upscalent en local comme Topaz Video AI)
- Une fois que tout est rassemblé dans le même dossier, j’ai utilisé mon script disponible ici: XXXXXXXXXXXXXXXXXXXXXXXXX
- Quelques minutes après, la vidéo était déjà prête!
- Un petit coup de Davinci Resolve pour intégrer la bande son et voilà!

Si vous utilisez ce script, ça me fera à la fois plaisir:
De vous avoir donné une occasion de générer des vidéos avec l’IA pour votre contenu long d’une manière plus responsable et respectueuse de l’environnement (et de votre portefeuille).
De pouvoir voir de nouveaux projets magnifiques de la part de vrais techniciens IA, qui vont probablement trouver des solutions encore plus créatives à l’utilisation de ce système de panning infini. (Partagez-moi vos créations, que je vous partage sur mes réseaux!)

# Pan-Stitch-Video

Transforme une pile d'images en une **vidéo de panoramique continu** (la caméra
glisse le long des images empilées). Quatre directions sont supportées :
**haut, bas, gauche, droite**. N'importe quelle tranche peut être remplacée par
une **vidéo en boucle** (`k.mp4`) qui se joue à la place de l'image fixe
pendant son passage à l'écran — **sans arrêter la caméra**. Aucune IA :
la continuité entre images est obtenue par un fondu de couture fin et net.

## Fonctionnalités

- **4 directions de panoramique** : haut, bas, gauche, droite (configurable,
  avec options en ligne de commande).
- **Tranches vidéo en boucle** : déposez `k.mp4` à côté de `k.png` (ou à sa
  place) ; la tranche joue en boucle pendant son temps à l'écran tandis que la
  caméra continue de se déplacer. La vidéo fournit le mouvement des personnages ;
  le décor défile comme une image fixe.
- **Coutures fines et nettes** : largeur de fondu réglable (`--feather`),
  aucun flou par défaut.
- **Robustesse réseau** : les sources sont mises en cache localement ; la sortie
  est écrite en local d'abord, puis copiée vers la cible réseau seulement si
  elle est accessible.
- Python pur + ffmpeg. Aucune dépendance d'IA.

## Prérequis

- Python 3.8+
- `numpy` et `Pillow`
- `ffmpeg` (et `ffprobe`, pour l'info optionnelle) dans le `PATH` ou via `FFMPEG`

```bash
pip install -r requirements.txt
```

## Utilisation

1. Déposez les images source dans un dossier : `1.png`, `2.png`, `3.png`, …
   (contiguës ; le pan s'arrête si des indices manquent).
2. (Optionnel) Remplacez une tranche par une vidéo en boucle : déposez `k.mp4`
   dans le même dossier et supprimez (ou gardez) `k.png`. Les tranches `.mp4`
   sont détectées automatiquement.
3. Lancez :

   ```bash
   python build_pan.py --direction up --src /chemin/vers/images
   ```

4. Résultat :
   - Vidéo locale : `./pan_<mode>.mp4` (ou votre `--out-dir`)
   - Aperçu des coutures : `bands_preview_<mode>.png`

### Options en ligne de commande

| Option         | Défaut           | Description                                    |
|----------------|------------------|------------------------------------------------|
| `--direction`  | `up`             | `up`, `down`, `left`, `right`                  |
| `--src`        | `O:/flats`       | Dossier source (`1.png` … `N.png`)             |
| `--out-dir`    | `C:/.../flats_render` | Dossier de sortie local                     |
| `--cache`      | `C:/.../flats_cache`  | Cache local des sources (résilience réseau) |
| `--copy-to`    | (aucun)          | Copie finale supplémentaire (répétable)        |
| `--first-idx`  | `1`              | Premier index d'image                          |
| `--image-w`    | `1536`           | Largeur des images source                      |
| `--image-h`    | `2752`           | Hauteur des images source                      |
| `--fps`        | `30`             | Images par seconde                             |
| `--px`         | `3`              | Vitesse du pan en px/frame (plus bas = plus lent)|
| `--feather`    | `110`            | Largeur du fondu de couture en px (plus bas = plus fin)|
| `--band-blur`  | `0.0`            | Flou de couture en px (0 = net)                |
| `--pause-frames` | `0`            | Frames de pause sur chaque image (0 = continu) |
| `--crf`        | `19`             | Qualité x264 (plus bas = meilleur)             |
| `--preset`     | `medium`         | Préréglage x264                                |
| `--output`     | `pan_{mode}.mp4` | Nom du fichier (`{mode}`/`{direction}` autorisés)|

## Fonctionnement des vidéos en boucle

- La tranche `k` devient une vidéo. La caméra **continue de se déplacer** (pas
  de gel) : le décor se comporte comme une image fixe (il défile vers le bas si
  la caméra monte).
- Pendant que la tranche est à l'écran, les frames du `.mp4` sont jouées **en
  boucle** (frame1 → frame2 → … → dernière → frame1 → …) à la place de l'image
  fixe.
- La vidéo fournit le mouvement des personnages ; le décor suit le panoramique.
- Quand la tranche quitte l'écran, le pan reprend sur l'image suivante.
- Résolution conseillée de la vidéo : identique aux images (ex. 1536×2752) ;
  sinon elle est redimensionnée.

## Détails techniques

- Les vidéos sont décodées par ffmpeg en images PNG temporaires, chargées en
  RAM, puis jouées via un index modulo (boucle).
- Le viewport est 16:9, pleine largeur (vertical) ou pleine hauteur (horizontal).
- Les bandes de couture sont calculées une fois (statiques) sauf pour les
  tranches vidéo, recalculées à chaque frame pour suivre la frame courante.

## Licence

MIT — voir [LICENSE](LICENSE).
