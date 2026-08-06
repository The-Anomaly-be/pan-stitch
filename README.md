# Pan-Stitch-Video

Turn a stack of images into a continuous **panning video** (the camera glides
along the stacked images). Four directions are supported: **up, down, left,
right**. Any slice can be replaced by a **looping video** (`k.mp4`) that plays
in place of the still image while it is on screen — **without stopping the
camera**. No AI is involved: continuity between images is achieved with a thin,
sharp seam cross-fade.

## Features

- **4 pan directions**: up, down, left, right (configurable, plus CLI flags).
- **Looping video slices**: drop `k.mp4` next to `k.png` (or instead of it);
  the slice plays on loop during its time on screen while the camera keeps
  moving. The video provides character motion; the scenery scrolls like a still.
- **Thin, sharp seams**: adjustable cross-fade width (`--feather`) and no blur
  by default.
- **Network resilience**: sources are cached locally; output is written locally
  first, then copied to the network target only if it is reachable.
- Pure Python + ffmpeg. No ML dependencies.

## Requirements

- Python 3.8+
- `numpy` and `Pillow`
- `ffmpeg` (and `ffprobe`, for the optional info probe) on `PATH` or set `FFMPEG`

```bash
pip install -r requirements.txt
```

## Usage

1. Put the source images in a folder as `1.png`, `2.png`, `3.png`, … (contiguous;
   the pan stops if indices are missing).
2. (Optional) Replace a slice by a looping video: drop `k.mp4` in the same folder
   and remove (or keep) `k.png`. `.mp4` slices are detected automatically.
3. Run:

   ```bash
   python build_pan.py --direction up --src /path/to/images
   ```

4. Output:
   - Local video: `./pan_<mode>.mp4` (or your `--out-dir`)
   - Seam preview: `bands_preview_<mode>.png`

### Command-line options

| Option         | Default          | Description                                   |
|----------------|------------------|-----------------------------------------------|
| `--direction`  | `up`             | `up`, `down`, `left`, `right`                 |
| `--src`        | `O:/flats`       | Source folder with `1.png` … `N.png`          |
| `--out-dir`    | `C:/.../flats_render` | Local output folder                      |
| `--cache`      | `C:/.../flats_cache`  | Local cache of sources (network resilience)|
| `--copy-to`    | (none)           | Extra copy destination(s); repeatable         |
| `--first-idx`  | `1`              | First image index                             |
| `--image-w`    | `1536`           | Source image width                            |
| `--image-h`    | `2752`           | Source image height                           |
| `--fps`        | `30`             | Output frames per second                      |
| `--px`         | `3`              | Pan speed in px/frame (lower = slower)        |
| `--feather`    | `110`            | Seam cross-fade width in px (lower = thinner) |
| `--band-blur`  | `0.0`            | Seam blur in px (0 = sharp)                   |
| `--pause-frames` | `0`            | Frames to pause on each image (0 = continuous)|
| `--crf`        | `19`             | x264 quality (lower = better)                 |
| `--preset`     | `medium`         | x264 preset                                   |
| `--output`     | `pan_{mode}.mp4` | Output filename (`{mode}`/`{direction}` allowed) |

## How looping video slices work

- The slide `k` becomes a video. The camera **keeps moving** (no freeze): the
  scenery behaves like a still (it scrolls down if the camera moves up).
- While the slice is on screen, the `.mp4` frames are played **on loop**
  (frame1 → frame2 → … → last → frame1 → …) instead of the fixed image.
- The video provides the motion of characters; the scenery follows the pan.
- When the slice leaves the screen, the pan resumes on the next image.
- Recommended video resolution: same as the images (e.g. 1536×2752); otherwise
  it is resized.

## How it works

- Videos are decoded by ffmpeg into temporary PNG frames, loaded into RAM, then
  played back via a modulo index (loop).
- The viewport is 16:9, full width (vertical) or full height (horizontal).
- Seam bands are computed once (static) except for video slices, recomputed
  each frame to follow the current video frame.

## License

MIT — see [LICENSE](LICENSE).
