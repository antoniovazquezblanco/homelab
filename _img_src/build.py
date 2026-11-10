"""
Regenerate the labelled images used in the docs from the source photos and TOML label files.

Layout:
    _img_src/orig/     source photos, never modified
    _img_src/labels/   one TOML file per generated image

Usage:
    python _img_src/build.py                     regenerate every image described in labels/
    python _img_src/build.py <file.toml>...      regenerate only those
    python _img_src/build.py <file.toml> --grid  write a coordinate grid preview to the temp folder

Needs Python 3.11+ and Pillow (pip install pillow).
Paths in a TOML file are relative to that file. All coordinates are pixels of the source photo,
so the --grid preview can be used to read them off.

TOML format:
    base = "../orig/photo.jpg"           # source photo
    output = "../../chassis/photo.jpg"   # generated image (.jpg or .png), next to the doc that uses it
    crop = [x0, y0, x1, y1]           # optional
    rotate = 90                       # optional, degrees counter-clockwise: 0, 90, 180 or 270
    width = 1600                      # optional output width (after rotating), default: crop size
    quality = 85                      # optional JPEG quality

    [[label]]
    text = ["Title", "detail line"]   # first line is bold and coloured
    box = [x0, y0, x1, y1]            # outline around the part
    at = [x, y]                       # where the label's top-left corner goes
    color = "#ffd400"

Coordinates stay in source photo pixels when the image is rotated; labels are always drawn upright.
"""
import argparse
import tempfile
import tomllib
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
FONTS = {
    "bold": ["C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "/System/Library/Fonts/Supplemental/Arial Bold.ttf"],
    "regular": ["C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/System/Library/Fonts/Supplemental/Arial.ttf"],
}


def font(kind, size):
    for path in FONTS[kind]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


ROTATIONS = {90: Image.Transpose.ROTATE_90, 180: Image.Transpose.ROTATE_180, 270: Image.Transpose.ROTATE_270}


class Canvas:
    """The cropped, rotated and resized source photo, with a mapping from photo pixels to image pixels."""

    def __init__(self, spec, toml_path):
        base = ImageOps.exif_transpose(Image.open(toml_path.parent / spec["base"])).convert("RGB")
        self.crop = tuple(spec.get("crop", (0, 0, base.width, base.height)))
        self.rotate = spec.get("rotate", 0) % 360
        if self.rotate not in (0, *ROTATIONS):
            raise ValueError(f"rotate must be 0, 90, 180 or 270, not {spec['rotate']}")
        image = base.crop(self.crop)
        across = image.width if self.rotate in (0, 180) else image.height  # becomes the output width
        self.scale = spec.get("width", across) / across
        image = image.resize((round(image.width * self.scale), round(image.height * self.scale)), Image.LANCZOS)
        self.w, self.h = image.size  # before rotating
        self.image = image.transpose(ROTATIONS[self.rotate]) if self.rotate else image

    def at(self, x, y):
        cx, cy = (x - self.crop[0]) * self.scale, (y - self.crop[1]) * self.scale
        if self.rotate == 90:
            return cy, self.w - cx
        if self.rotate == 180:
            return self.w - cx, self.h - cy
        if self.rotate == 270:
            return self.h - cy, cx
        return cx, cy

    def box(self, x0, y0, x1, y1):
        (ax, ay), (bx, by) = self.at(x0, y0), self.at(x1, y1)
        return min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)


def draw_labels(spec, canvas):
    image = canvas.image
    unit = image.width / 1600  # sizes below are tuned for a 1600 px wide image
    bold, regular = font("bold", round(26 * unit)), font("regular", round(22 * unit))
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    placed = []
    for label in spec.get("label", []):
        colour = ImageColor.getrgb(label["color"])
        lines = label["text"]
        fonts = [bold] + [regular] * (len(lines) - 1)
        heights = [f.size + round(6 * unit) for f in fonts]
        x, y = canvas.at(*label["at"])
        w = max(od.textlength(t, font=f) for t, f in zip(lines, fonts)) + 24 * unit
        h = sum(heights) + 16 * unit
        od.rounded_rectangle([x, y, x + w, y + h], radius=8 * unit, fill=(0, 0, 0, 200),
                             outline=colour + (255,), width=max(2, round(3 * unit)))
        placed.append((colour, label["box"], (x, y, x + w, y + h), lines, fonts, heights))
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")

    draw = ImageDraw.Draw(image)
    for colour, box, (lx0, ly0, lx1, ly1), lines, fonts, heights in placed:
        bx0, by0, bx1, by1 = canvas.box(*box)
        draw.rectangle([bx0, by0, bx1, by1], outline=colour, width=max(2, round(4 * unit)))
        # leader from the nearest label edge to the nearest point of the part outline
        cx, cy = (lx0 + lx1) / 2, (ly0 + ly1) / 2
        px, py = min(max(cx, bx0), bx1), min(max(cy, by0), by1)
        if not (lx0 <= px <= lx1 and ly0 <= py <= ly1):
            sx = lx1 if px > lx1 else lx0 if px < lx0 else cx
            sy = ly1 if py > ly1 else ly0 if py < ly0 else cy
            draw.line([(sx, sy), (px, py)], fill=colour, width=max(2, round(3 * unit)))
            r = 5 * unit
            draw.ellipse([px - r, py - r, px + r, py + r], fill=colour)
        ty = ly0 + 8 * unit
        for i, (text, f, lh) in enumerate(zip(lines, fonts, heights)):
            draw.text((lx0 + 12 * unit, ty), text, font=f, fill=colour if i == 0 else (255, 255, 255))
            ty += lh
    return image


def draw_grid(image, canvas):
    """Grid lines in source photo coordinates, labelled x... and y... so they read the same when rotated."""
    x0, y0, x1, y1 = canvas.crop
    step = 100 if max(x1 - x0, y1 - y0) <= 2000 else 250
    draw = ImageDraw.Draw(image)
    f = font("regular", 14)
    lines = [(f"x{x}", (x, y0), (x, y1)) for x in range((x0 // step + 1) * step, x1, step)]
    lines += [(f"y{y}", (x0, y), (x1, y)) for y in range((y0 // step + 1) * step, y1, step)]
    for text, start, end in lines:
        (ax, ay), (bx, by) = canvas.at(*start), canvas.at(*end)
        draw.line([(ax, ay), (bx, by)], fill=(255, 0, 255))
        draw.text((min(ax, bx) + 2, min(ay, by) + 2), text, font=f, fill=(255, 0, 255))
    return image


def build(toml_path, grid=False):
    spec = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    canvas = Canvas(spec, toml_path)
    image = draw_labels(spec, canvas)
    if grid:
        out = Path(tempfile.gettempdir()) / (Path(spec["output"]).stem + ".grid.jpg")
        image = draw_grid(image, canvas)
    else:
        out = (toml_path.parent / spec["output"]).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
    # no exif is passed, so camera metadata never reaches the output
    image.save(out, quality=spec.get("quality", 85), optimize=True, progressive=True)
    print(f"{toml_path.name} -> {out} ({image.width}x{image.height})")


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("labels", type=Path, nargs="*", help="TOML files (default: all in labels/)")
    parser.add_argument("--grid", action="store_true", help="write coordinate grid previews instead")
    args = parser.parse_args()
    for toml_path in args.labels or sorted((HERE / "labels").glob("*.toml")):
        build(toml_path, args.grid)


if __name__ == "__main__":
    main()
