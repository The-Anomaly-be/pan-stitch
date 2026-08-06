#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pan-Stitch-Video : empile une serie d'images en un panoramique continu.

Le panoramique glisse le long des images empilees. Quatre directions sont
possibles : haut (up), bas (down), gauche (left), droite (right).
Une tranche peut etre remplacee par une VIDEO (k.mp4) qui joue en BOUCLE
pendant son passage a l'ecran, SANS arret de la camera. Aucune IA : la
continuite entre images est obtenue par un fondu de couture fin et net.

Voir LISEZMOI.md (FR) / README.md (EN) pour l'utilisation.
"""
import os
import sys
import shutil
import subprocess
import argparse
import tempfile
import datetime
import numpy as np
from PIL import Image, ImageFilter

# ----------------------------------------------------------------------------
# CONFIGURATION PAR DEFAUT (peut etre override via la ligne de commande)
# ----------------------------------------------------------------------------
SRC_DIR   = "O:/flats"                       # dossier des images source (1.png..N.png)
CACHE_DIR = "C:/Users/jacof/flats_cache"    # copie locale des sources (resilience reseau)
OUT_LOCAL = "C:/Users/jacof/flats_render"   # sortie locale sure
COPY_TARGETS = ["O:/flats/out"]             # copie finale si le lecteur reseau repond

FFMPEG    = r"C:/FFmpeg/bin/ffmpeg.exe"

DIRECTION   = "up"        # "up" | "down" | "left" | "right"
FIRST_IDX   = 1           # numerotation des fichiers 1.png .. N.png
IMAGE_W     = 1536
IMAGE_H     = 2752

FPS          = 30
PX_PER_FRAME = 3         # vitesse pan (px/frame). 3 ~= 13x plus lent que 40.
FEATHER      = 110       # largeur (px) du fondu de couture. Plus bas = couture plus fine.
BAND_BLUR    = 0.0       # flou gaussien (px) du bandeau de couture. 0 = net.
PAUSE_FRAMES = 0         # frames de pause sur chaque image (0 = pan continu).
CRF          = 19
PRESET       = "medium"
OUTPUT_NAME  = "pan_{mode}.mp4"
# ----------------------------------------------------------------------------

os.makedirs(OUT_LOCAL, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)


class ImageItem:
    is_video = False

    def __init__(self, arr):
        self.static = arr
        self.cur = None


class VideoClip:
    is_video = True

    def __init__(self, path, W, H, fps, ffmpeg):
        self.W = W
        self.H = H
        self.fps = fps          # framerate de sortie (pan)
        # Decode TOUTES les frames source (aucune perdue, pas de drop CFR).
        # La lecture se fait en boucle 1:1 stricte (next), sans remapping par
        # framerate : on a deja 100% des frames, donc aucune ne saute. La video
        # defile alors a 30 fps en montrant ses frames dans l'ordre -> fluide.
        tmp = tempfile.mkdtemp(prefix="panvid_")
        pat = os.path.join(tmp, "f%05d.png")
        proc = subprocess.Popen(
            [ffmpeg, "-loglevel", "error", "-i", path,
             "-vf", f"scale={W}:{H}", "-vsync", "0", pat],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        pngs = sorted(os.path.join(tmp, f) for f in os.listdir(tmp) if f.endswith(".png"))
        self.frames = []
        for p in pngs:
            im = Image.open(p).convert("RGB")
            self.frames.append(np.asarray(im))
            try:
                os.remove(p)
            except Exception:
                pass
        try:
            shutil.rmtree(tmp)
        except Exception:
            pass
        if not self.frames:
            sys.exit(f"Video vide ou illisible: {path}")
        self.N = len(self.frames)
        self.idx = 0
        self.static = self.frames[0].copy()
        self.cur = self.frames[0].copy()

    def next(self):
        """Boucle 1:1 stricte sur les frames deja decodees (100% des frames
        source, aucune perdue). Aucun remapping par framerate -> zero saut."""
        self.idx = (self.idx + 1) % self.N
        self.cur = self.frames[self.idx]
        return self.cur


def get_items(src_dir, cache_dir, first_idx, image_w, image_h, ffmpeg):
    def find_image(idx):
        for ext in (".png", ".jpg", ".jpeg"):
            p = os.path.join(src_dir, f"{idx}{ext}")
            if os.path.exists(p):
                return p
        return None
    fnums = []
    idx = first_idx
    while True:
        has_img = find_image(idx) is not None
        has_mp4 = os.path.exists(os.path.join(src_dir, f"{idx}.mp4"))
        if not has_img and not has_mp4:
            break
        fnums.append(idx)
        idx += 1
    if not fnums:
        sys.exit("Aucune image/video trouvee (source inaccessible et rien en cache).")
    N = fnums[-1] - first_idx + 1
    print(f"[*] {N} fichiers detectes ({first_idx}..{N})")

    items = []
    for fnum in range(N, first_idx - 1, -1):      # bande du haut/gauche vers le bas/droite
        img_path = find_image(fnum)
        vid_path = os.path.join(src_dir, f"{fnum}.mp4")
        cached_img = os.path.join(cache_dir, f"{fnum}.png")
        cached_vid = os.path.join(cache_dir, f"{fnum}.mp4")
        if os.path.exists(vid_path):
            if not os.path.exists(cached_vid):
                try:
                    shutil.copyfile(vid_path, cached_vid)
                except Exception:
                    pass
            vpath = cached_vid if os.path.exists(cached_vid) else vid_path
            items.append(VideoClip(vpath, image_w, image_h, FPS, ffmpeg))
            print(f"    tranche fichier {fnum} = VIDEO (loop dans le pan)")
        else:
            if not os.path.exists(cached_img):
                if img_path is None:
                    sys.exit(f"Image manquante pour l'index {fnum}")
                shutil.copyfile(img_path, cached_img)
            im = Image.open(cached_img)
            if im.mode == "RGBA":
                bg = Image.new("RGB", im.size, (255, 255, 255))
                bg.paste(im, mask=im.split()[3])
                im = bg
            else:
                im = im.convert("RGB")
            items.append(ImageItem(np.asarray(im)))
    nvid = sum(1 for it in items if it.is_video)
    print(f"[*] {len(items)} tranches chargees "
          f"({items[0].static.shape[1]}x{items[0].static.shape[0]}), dont {nvid} video(s)")
    return items, N


def compute_band(a, b, mode, V):
    """Bandeau de couture entre l'image a (haut/gauche) et b (bas/droite)."""
    if mode == "vertical":
        Hh, Ww = a.shape[0], a.shape[1]
        c = V // 2
        band = np.empty((V, Ww, 3), dtype=np.uint8)
        top_rows = np.clip(Hh - 1 - c + np.arange(V), 0, Hh - 1)
        bot_rows = np.clip(np.arange(V) - c, 0, Hh - 1)
        r = np.arange(V)
        band[r < c - FEATHER // 2] = a[top_rows[r < c - FEATHER // 2]]
        band[r > c + FEATHER // 2] = b[bot_rows[r > c + FEATHER // 2]]
        m = (r >= c - FEATHER // 2) & (r <= c + FEATHER // 2)
        rr = r[m]
        alpha = (rr - (c - FEATHER // 2)) / FEATHER
        top = a[top_rows[m]].astype(np.float32)
        bot = b[bot_rows[m]].astype(np.float32)
        band[m] = (top * (1 - alpha[:, None, None]) + bot * alpha[:, None, None]).astype(np.uint8)
    else:
        Hh, Ww = a.shape[0], a.shape[1]
        c = V // 2
        band = np.empty((Hh, V, 3), dtype=np.uint8)
        top_cols = np.clip(Ww - 1 - c + np.arange(V), 0, Ww - 1)
        bot_cols = np.clip(np.arange(V) - c, 0, Ww - 1)
        r = np.arange(V)
        band[:, r < c - FEATHER // 2] = a[:, top_cols[r < c - FEATHER // 2]]
        band[:, r > c + FEATHER // 2] = b[:, bot_cols[r > c + FEATHER // 2]]
        m = (r >= c - FEATHER // 2) & (r <= c + FEATHER // 2)
        rr = r[m]
        alpha = (rr - (c - FEATHER // 2)) / FEATHER
        top = a[:, top_cols[m]].astype(np.float32)
        bot = b[:, bot_cols[m]].astype(np.float32)
        band[:, m] = (top * (1 - alpha)[None, :, None] + bot * alpha[None, :, None]).astype(np.uint8)
    if BAND_BLUR > 0:
        band = np.asarray(Image.fromarray(band).filter(ImageFilter.GaussianBlur(BAND_BLUR)))
    return band


def build_frame(p0, items, bands_static, V, unit, mode):
    """Construit une frame pour une position p0 le long de la bande.

    p0 est l'offset (en px) du haut/gauche du viewport par rapport au debut
    de la bande empilee. Gere un nombre arbitraire de tranches dans le viewport.
    """
    N = len(items)

    def arr(k):
        it = items[k]
        return it.cur if (it.is_video and it.cur is not None) else it.static

    if mode == "vertical":
        Ww = items[0].static.shape[1]
        frame = np.empty((V, Ww, 3), dtype=np.uint8)
        rows = p0 + np.arange(V)
        k = np.minimum(rows // unit, N - 1)
        ch = np.flatnonzero(np.diff(k)) + 1
        segs = np.concatenate(([0], ch, [V]))
        for s in range(len(segs) - 1):
            r0, r1 = int(segs[s]), int(segs[s + 1])
            kk = int(k[r0])
            local = np.clip(rows[r0:r1] - kk * unit, 0, unit - 1)
            frame[r0:r1] = arr(kk)[local]
        for bi in range(N - 1):
            if items[bi].is_video or items[bi + 1].is_video:
                bnd = compute_band(arr(bi), arr(bi + 1), mode, V)
            else:
                bnd = bands_static[bi]
            seam = (bi + 1) * unit
            b0 = seam - V // 2
            lo = max(p0, b0)
            hi = min(p0 + V, b0 + V)
            if lo < hi:
                frame[lo - p0:hi - p0] = bnd[lo - b0:hi - b0]
    else:
        Hh = items[0].static.shape[0]
        frame = np.empty((Hh, V, 3), dtype=np.uint8)
        cols = p0 + np.arange(V)
        k = np.minimum(cols // unit, N - 1)
        ch = np.flatnonzero(np.diff(k)) + 1
        segs = np.concatenate(([0], ch, [V]))
        for s in range(len(segs) - 1):
            c0, c1 = int(segs[s]), int(segs[s + 1])
            kk = int(k[c0])
            local = np.clip(cols[c0:c1] - kk * unit, 0, unit - 1)
            frame[:, c0:c1] = arr(kk)[:, local]
        for bi in range(N - 1):
            if items[bi].is_video or items[bi + 1].is_video:
                bnd = compute_band(arr(bi), arr(bi + 1), mode, V)
            else:
                bnd = bands_static[bi]
            seam = (bi + 1) * unit
            b0 = seam - V // 2
            lo = max(p0, b0)
            hi = min(p0 + V, b0 + V)
            if lo < hi:
                frame[:, lo - p0:hi - p0] = bnd[:, lo - b0:hi - b0]
    return frame


def render(items, N, mode, direction, out_name):
    if mode == "vertical":
        Ww, Hh = IMAGE_W, IMAGE_H
        V = round(Ww * 9 / 16)
        LONG = N * Hh
        out_W, out_H = Ww, V
        unit = Hh
    else:
        Ww, Hh = IMAGE_W, IMAGE_H
        V = round(Hh * 16 / 9)
        LONG = N * Ww
        out_W, out_H = V, Hh
        unit = Ww
    if V % 2 == 1:                           # ffmpeg yuv420p exige dimensions paires
        V += 1
    out_W, out_H = (Ww, V) if mode == "vertical" else (V, Hh)
    c = V // 2

    bands_static = [compute_band(items[k].static, items[k + 1].static, mode, V)
                    for k in range(N - 1)]
    print(f"[*] {len(bands_static)} bandeaux de couture calcules (viewport {out_W}x{out_H})")

    # Sequence des positions le long de la bande.
    # Ascendant (p0 croissant) = on part du haut (vertical) / gauche (horizontal)
    # et on avance vers le bas / droite.
    p0s = list(range(0, LONG - V + 1, PX_PER_FRAME))
    if p0s[-1] != LONG - V:
        p0s.append(LONG - V)
    if PAUSE_FRAMES:
        extra = []
        for k in range(N):
            target = int((k + 0.5) * unit) - c
            best = min(range(len(p0s)), key=lambda i: abs(p0s[i] - target))
            extra.extend([p0s[best]] * PAUSE_FRAMES)
        p0s = p0s + extra
        p0s.sort()
    # Direction : "up" et "left" partent de la fin (bas/droite) et remontent.
    if direction in ("up", "left"):
        p0s = p0s[::-1]

    sens = {"up": "haut (img1->imgN)", "down": "bas (imgN->img1)",
            "left": "gauche (imgN->img1)", "right": "droite (img1->imgN)"}[direction]
    print(f"[*] {len(p0s)} frames a generer (~{len(p0s)/FPS:.1f}s a {FPS}fps, sens={sens})")

    local_mp4 = os.path.join(OUT_LOCAL, out_name)
    proc = subprocess.Popen(
        [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{out_W}x{out_H}", "-framerate", str(FPS), "-i", "-",
         "-an", "-c:v", "libx264", "-preset", PRESET, "-crf", str(CRF),
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", local_mp4],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for fi, p0 in enumerate(p0s):
        for it in items:
            if it.is_video:
                it.next()                     # avance la video (loop) 1 frame/output
        frame = build_frame(p0, items, bands_static, V, unit, mode)
        proc.stdin.write(np.ascontiguousarray(frame, dtype=np.uint8).tobytes())
        if (fi + 1) % 1000 == 0:
            print(f"    frames {fi+1}/{len(p0s)}")

    proc.stdin.close()
    out, err = proc.communicate()
    if proc.returncode != 0:
        print("[!] ERREUR ffmpeg:\n", err.decode(errors="ignore")[-2000:])
        sys.exit(1)
    print(f"[+] Video ecrite (local) : {local_mp4}")
    return local_mp4, bands_static


def save_band_preview(items, mode, bands, max_show=6):
    show = bands[:max_show]
    if mode == "vertical":
        c = bands[0].shape[0] // 2
        thumbs = [Image.fromarray(b[c - 120:c + 120]) for b in show]
        w = max(t.width for t in thumbs)
        h = sum(t.height for t in thumbs)
        sheet = Image.new("RGB", (w, h), (0, 0, 0))
        y = 0
        for t in thumbs:
            sheet.paste(t, (0, y))
            y += t.height
    else:
        c = bands[0].shape[1] // 2
        thumbs = [Image.fromarray(b[:, c - 120:c + 120]) for b in show]
        w = sum(t.width for t in thumbs)
        h = max(t.height for t in thumbs)
        sheet = Image.new("RGB", (w, h), (0, 0, 0))
        x = 0
        for t in thumbs:
            sheet.paste(t, (x, 0))
            x += t.width
    p = os.path.join(OUT_LOCAL, f"bands_preview_{mode}.png")
    sheet.save(p)
    print(f"[+] Apercu des coutures : {p}")
    return p


def deposit(local_path, rel_name):
    for tgt in COPY_TARGETS:
        try:
            os.makedirs(tgt, exist_ok=True)
            shutil.copy2(local_path, os.path.join(tgt, rel_name))
            print(f"[+] Copie -> {tgt}/{rel_name}")
        except OSError as e:
            print(f"[!] Copie vers {tgt} impossible ({e}); fichier conserve localement.")


def probe(local_mp4):
    try:
        r = subprocess.run([FFMPEG.replace("ffmpeg.exe", "ffprobe.exe"), "-v", "error",
                            "-show_entries", "format=duration",
                            "-show_entries", "stream=width,height,r_frame_rate",
                            "-of", "default=noprint_wrappers=1", local_mp4],
                           capture_output=True, text=True, timeout=30)
        print("[*] Infos ffmpeg :\n" + r.stdout.strip())
    except Exception as e:
        print("[!] probe ignoree :", e)


def parse_args():
    p = argparse.ArgumentParser(
        description="Panoramique continu a partir d'images empilees (avec videos loop).")
    p.add_argument("--direction", choices=["up", "down", "left", "right"],
                   default=DIRECTION, help="Sens du pan (defaut: %(default)s).")
    p.add_argument("--src", default=SRC_DIR, help="Dossier des images source (1.png..N.png).")
    p.add_argument("--out-dir", default=OUT_LOCAL, help="Dossier de sortie local.")
    p.add_argument("--cache", default=CACHE_DIR, help="Dossier de cache local des sources.")
    p.add_argument("--copy-to", default=None, action="append",
                   help="Copie finale supplementaire (ex: O:/flats/out). Repetable.")
    p.add_argument("--first-idx", type=int, default=FIRST_IDX, help="Premier index (defaut: 1).")
    p.add_argument("--image-w", type=int, default=IMAGE_W, help="Largeur images source.")
    p.add_argument("--image-h", type=int, default=IMAGE_H, help="Hauteur images source.")
    p.add_argument("--fps", type=int, default=FPS)
    p.add_argument("--px", type=int, default=PX_PER_FRAME,
                   help="Vitesse pan en px/frame (plus bas = plus lent).")
    p.add_argument("--feather", type=int, default=FEATHER,
                   help="Largeur du fondu de couture (plus bas = couture plus fine).")
    p.add_argument("--band-blur", type=float, default=BAND_BLUR)
    p.add_argument("--pause-frames", type=int, default=PAUSE_FRAMES)
    p.add_argument("--crf", type=int, default=CRF)
    p.add_argument("--preset", default=PRESET)
    p.add_argument("--output", default=OUTPUT_NAME,
                   help="Nom du fichier de sortie (peut contenir {mode}).")
    p.add_argument("--extract", type=int, default=0, metavar="N",
                   help="Mode test: extrait les N premieres secondes de chaque tranche "
                        "video (loop) dans un clip dedie, sans rendre tout le pan "
                        "(permet de juger la fluidite rapidement).")
    return p.parse_args()


def extract_video_clips(items, N, mode, direction, seconds, out_name):
    """Mode test: pour chaque tranche video, produit un clip court (loop) a la
    resolution du viewport, pour juger la fluidite sans rendre tout le pan."""
    if mode == "vertical":
        Ww, Hh = IMAGE_W, IMAGE_H
        V = round(Ww * 9 / 16)
        out_W, out_H = Ww, V
    else:
        Ww, Hh = IMAGE_W, IMAGE_H
        V = round(Hh * 16 / 9)
        out_W, out_H = V, Hh
    if V % 2 == 1:
        V += 1
    out_W, out_H = (Ww, V) if mode == "vertical" else (V, Hh)

    vids = [it for it in items if it.is_video]
    if not vids:
        print("[!] Aucune tranche video a extraire.")
        return
    print(f"[*] Extraction test: {len(vids)} video(s), {seconds}s chacun "
          f"({out_W}x{out_H}, {FPS}fps)")

    nframes = int(seconds * FPS)
    stamp = datetime.datetime.now().strftime("%H%M%S")
    for vi, it in enumerate(vids, 1):
        # remet l'index a 0 pour un loop propre
        it.idx = 0
        out = os.path.join(OUT_LOCAL,
                           f"extract_{direction}_v{vi}_{seconds}s.mp4")
        proc = subprocess.Popen(
            [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
             "-s", f"{out_W}x{out_H}", "-framerate", str(FPS), "-i", "-",
             "-an", "-c:v", "libx264", "-preset", PRESET, "-crf", str(CRF),
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", out],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for _ in range(nframes):
            fr = it.next() if it.is_video else it.static
            # recadre la frame video au viewport (centre)
            a = fr
            if mode == "vertical":
                sh = a.shape[0]
                s0 = (sh - V) // 2
                a = a[s0:s0 + V]
            else:
                sw = a.shape[1]
                s0 = (sw - V) // 2
                a = a[:, s0:s0 + V]
            proc.stdin.write(np.ascontiguousarray(a, dtype=np.uint8).tobytes())
        proc.stdin.close()
        proc.communicate()
        print(f"  -> {out}")
    print(f"[+] Extraction terminee (test). Local: {OUT_LOCAL}")


def main():
    global SRC_DIR, CACHE_DIR, OUT_LOCAL, COPY_TARGETS, FIRST_IDX
    global IMAGE_W, IMAGE_H, FPS, PX_PER_FRAME, FEATHER, BAND_BLUR
    global PAUSE_FRAMES, CRF, PRESET, OUTPUT_NAME

    args = parse_args()
    SRC_DIR = args.src
    CACHE_DIR = args.cache
    OUT_LOCAL = args.out_dir
    if args.copy_to:
        COPY_TARGETS = args.copy_to
    FIRST_IDX = args.first_idx
    IMAGE_W = args.image_w
    IMAGE_H = args.image_h
    FPS = args.fps
    PX_PER_FRAME = args.px
    FEATHER = args.feather
    BAND_BLUR = args.band_blur
    PAUSE_FRAMES = args.pause_frames
    CRF = args.crf
    PRESET = args.preset
    OUTPUT_NAME = args.output

    os.makedirs(OUT_LOCAL, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)

    direction = args.direction
    mode = "vertical" if direction in ("up", "down") else "horizontal"
    out_name = OUTPUT_NAME.format(mode=mode, direction=direction)

    items, N = get_items(SRC_DIR, CACHE_DIR, FIRST_IDX, IMAGE_W, IMAGE_H, FFMPEG)

    if args.extract and args.extract > 0:
        # Mode test rapide : extrait chaque tranche video (loop) dans un clip
        # court a la place qu'elle occupe dans le pan, pour juger la fluidite.
        extract_video_clips(items, N, mode, direction, args.extract, out_name)
        return

    local_mp4, bands = render(items, N, mode, direction, out_name)
    preview = save_band_preview(items, mode, bands)
    probe(local_mp4)
    deposit(local_mp4, os.path.basename(local_mp4))
    deposit(preview, os.path.basename(preview))
    print("[*] Termine. Local :", OUT_LOCAL)


if __name__ == "__main__":
    main()
