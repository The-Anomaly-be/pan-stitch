# Pan-Stitch-Video

Experimental way of generating long videos with a low amount of material (videos and images).
Perfect to create local and ecologically responsible AI videos.

OBO has been working incredibly hard for the past week, almost 24 hours a day. It is simultaneously an image creator, screenwriter/director, post-production and VFX supervisor, sound engineer, and developer. It’s simply incredible to think that a relatively old computer can handle so many different tasks at the same time.

He also helps me find creative solutions to problems. One of the biggest challenges at the moment is that, if I want AI that is environmentally responsible, I remain fairly limited in terms of resources. Generating large quantities of video at home is not the same as doing it through a data center running at full capacity while destroying spaces that should be green…

We discussed several possible approaches. The first was to reduce the quality, which I obviously didn’t want to do. The second was to make videos using less footage. That was an idea, but how could I apply it? Slowing things down wasn’t an option: the pace had to remain dynamic and watchable. That’s when I had an idea, and OBO helped me implement it in less than an hour.

Imagine an endless image, with the camera panning from left to right, from right to left… Or, as in my first example, from bottom to top. The idea of infinite apartments is not new, but I didn’t have the technical skills to apply it in an animated format. AI not only allowed me to bring the idea to life, but also to take it a little further…

So we designed a script that stitches the images together. It can create an infinite vertical tower of images, or assemble them horizontally. Then, using a virtual camera, it travels through this composition from bottom to top, top to bottom, right to left, left to right… There are no limitations in terms of quality or resolution, and there is no need to generate long videos in order to reach a certain duration. My first test was conclusive: 38 images for a 20-minute video!

That was already great, but I was missing one small detail to make it perfect. It’s all very well to watch a landscape go by, but all the people in it are completely static… What if we could bring them to life?

After imagining the concept, I had another discussion with the AI. Instead of inserting a still image between two others, what would happen if I inserted a video? A kind of loop in which my animated characters, rather than remaining frozen, would move within their static frames?

I explained the idea as best I could. After initially misunderstanding me, the AI realized that the movement needed to remain continuous and maintain a consistent rhythm. However, it should not use a still image for this section; instead, it needed to play every frame of a video one after another, then loop back to the beginning. The result: the people in my video move as the camera passes their level. It was absolutely extraordinary—exactly what I had imagined. I therefore converted several images into videos locally, and here is the final result.

The script used to create this assembly is extremely simple. You provide it with a folder containing your images and/or videos, specify the direction—horizontal or vertical—and it creates your panning sequence. I took advantage of the length of this video to feature a small, calm playlist of beautiful tracks that OBO created locally a few days ago.

My workflow
To generate the code, I used Hermes and a local Qwen3.6-35B Q2_K_P model, which works very well in an agentic setup on my RTX 4080 graphics card.

Generate images based on a theme that will provide a certain degree of continuity when assembled. I used ComfyUI with the Z-Image Turbo image model. For a 16:9 vertical panning video, I generated my images in 9:16. Here is an example of an image prompt. I asked Hermes for several variations using many different styles mixed together for the buildings, such as Art Deco, Brutalism, Russian Constructivism, Neo-Moorish architecture, and so on:

An ultra-detailed urban photograph captured at night in warm mist, tightly framed on a composite façade completely occupied by buildings, with no opening toward the sky. The wall is an architectural collage in which four styles blend together: Streamline Moderne with horizontal lines and porthole windows, Neo-Mudéjar architecture with brickwork and horseshoe arches, Korean minimalism with clean surfaces, and cyber-gothic architecture with metal and neon lights. The mist settles between the façades, around the balconies, and in front of certain windows, creating halos around the light sources.

At the bottom of the frame, a band of mixed façades stretches across the image. On the left, a Streamline Moderne building features a white façade with horizontal lines, ribbon windows, and rounded balconies with chrome railings. On one balcony, a person is standing in silhouette, hands resting on the railing, face turned outward. Pale yellow interior light spreads across the smooth surfaces and facial features, revealing the eyes, the curve of the nose, and the line of the lips in an attentive expression.

In the lower center, a Neo-Mudéjar section appears: a red-brick façade with horseshoe arches, geometric friezes, and balconies with wrought-iron railings forming star-shaped patterns. On one balcony, a person is sitting on a chair, legs crossed, hands holding a glass, face turned toward another balcony. The light from an outdoor wall lamp casts reflections across the brickwork and the face, emphasizing the features, eyes, and lips.

On the lower right, a Korean minimalist block dominates the scene: a smooth concrete façade, regular windows, and simple balconies with glass railings. On one balcony, a person is leaning forward, hands resting on the railing, face turned downward. Light from an interior lamp creates soft contrasts across the face, with defined features, narrowed eyes, and a closed mouth expressing intensity. Beside it, a cyber-gothic façade emerges, made of dark metal surfaces with integrated colored neon lights and metal-grid railings. On one balcony, a person is sitting on a bench, hands resting on their knees, eyes half-closed, wearing a calm expression. Neon light spreads across the metal surfaces and the face, creating a smooth transition between light and shadow.

As the image rises, the styles continue to intersect. Streamline Moderne floors, with their horizontal lines, appear above Neo-Mudéjar sections; Korean minimalist volumes stand beside cyber-gothic façades. The balconies multiply, each with its own signature: chrome for Streamline Moderne, wrought iron for Neo-Mudéjar, glass for minimalism, and metal for cyber-gothic architecture. On some of them, people are engaged in various activities: a Streamline Moderne silhouette closes shutters; someone on a Mudéjar balcony adjusts a lamp; someone on a minimalist balcony leans over to look toward a lower floor; on a cyber-gothic balcony, someone walks slowly from one side to the other with their hands behind their back.

The nighttime light in the mist creates a warm and enveloping atmosphere. Interior sources in the Streamline Moderne and Mudéjar façades are often more decorative, with golden tones; in the minimalist and cyber-gothic blocks, some lights are more functional, whiter, or slightly greenish. The mist blends these colors, creating softly blurred halos around the windows and outdoor lamps. The Streamline Moderne surfaces take on white tones; the Mudéjar patterns reflect golden glows; the minimalist volumes remain cooler, although their angles are softened; the cyber-gothic façades display subtle gradients.

The tight framing, with no sky, gives the composite wall an overwhelming yet fascinating presence. The depth of field is extensive; the fine textures of the Streamline Moderne lines, Mudéjar brickwork, minimalist concrete, and cyber-gothic metal are all clearly visible. The faces and bodies on the balconies and behind the windows remain large enough for their micro-expressions to be perceptible, while still being integrated into a larger composition in which each person is a note in an architectural visual score.

I didn’t want the images in any particular order, so I used a small Python script to rename all my files 1.png, 2.png, and so on, in a completely random order.

Generate videos from some of the images. I used Wan, although I would now recommend Minimax H3 instead for better quality. In my example, one image out of every six is animated, resulting in six videos. Replace the PNG files with MP4 files. My prompt for each video was:
video of people living in their flats and balconies, walking, moving, no talking, totally fixed camera, no camera movement at all

Use an upscaler for both the images and the videos to improve quality and standardize the resolution. I used a resolution of 2160 × 3840, with my own upscaler that adds details, but you can use other upscalers in ComfyUI or local upscaling applications such as Topaz Video AI.

A few minutes later, the video was already ready!

A quick pass in DaVinci Resolve to add the soundtrack, and that was it!

If you use this script
It would make me happy for two reasons:

I will have given you an opportunity to generate AI videos for your long-form content in a more responsible and environmentally respectful way, while also being kinder to your wallet.

I’ll get to see beautiful new projects from genuine AI technicians, who will probably come up with even more creative ways to use this infinite-panning system.

Share your creations with me, and I’ll share them on my social media!

Turn a stack of images into a continuous **panning video** (the camera glides
along the stacked images). Four directions are supported: **up, down, left,
right**. Any slice can be replaced by a **looping video** (`k.mp4`) that plays
in place of the still image while it is on screen — **without stopping the
camera**. No AI is involved in this process: continuity between images is achieved with a thin,
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
