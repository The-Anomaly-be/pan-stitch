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
