"""S.E.T. Solar comparison-hook TikToks (9:16), 2026-09-28.
  allpowers: "Same 256Wh. RIVER 2 $209 vs VOLIX P300 $139." (prices checked live 9/28/26)
  bluetti:   "1kWh weigh-in: DELTA 3 Plus 30 lbs vs Elite 100 Mini 23.6 lbs." (manufacturer specs)
Official product photos from the manufacturers' stores, in video-assets/comparison-img/.
Formula: ~/.kiyomimax/memory/tiktok-content-strategy.md (full hook on frame 1, 30-40s, AriaNeural).
Usage: python tiktok-comparisons.py [allpowers|bluetti]
"""
import asyncio, os, subprocess, sys
from pathlib import Path
import edge_tts
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
W, H, FPS = 1080, 1920, 30
D = Path(__file__).parent
IMG = D / "comparison-img"
EXPORTS = Path(os.environ["USERPROFILE"]) / "OneDrive" / "video-assets" / "exports"
VOICE, GAP = "en-US-AriaNeural", 0.4
CHAR, CHAR2 = (30, 30, 46), (22, 34, 60)
BLUE, GREEN, GOLD, RED = (0, 102, 255), (0, 200, 150), (245, 166, 35), (235, 87, 87)
WHITE, MUTED, INK = (255, 255, 255), (180, 190, 205), (45, 55, 72)


def font(size, bold=True):
    return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf", size)


def make_bg():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(CHAR[i] + (CHAR2[i] - CHAR[i]) * k) for i in range(3)))
    logo = Image.open(D.parent / "set-logo.jpg").convert("RGB")
    logo.thumbnail((300, 150))
    d.rounded_rectangle([(W - logo.width) // 2 - 16, 80, (W + logo.width) // 2 + 16, 96 + logo.height + 16], 18, fill=WHITE)
    img.paste(logo, ((W - logo.width) // 2, 96))
    d.text((W // 2, H - 110), "sunenergytechnology.com", font=font(34, False), fill=MUTED, anchor="mm")
    return img


BG = make_bg()


def text(d, y, s, size, fill=WHITE, bold=True):
    f = font(size, bold)
    d.text((W // 2 + 3, y + 3), s, font=f, fill=(0, 0, 0), anchor="mm")
    d.text((W // 2, y), s, font=f, fill=fill, anchor="mm")


def pill(d, y, s, fill=GOLD, fg=CHAR, size=54):
    f = font(size)
    w = d.textlength(s, font=f) + 90
    d.rounded_rectangle([(W - w) / 2, y - 55, (W + w) / 2, y + 55], 55, fill=fill)
    d.text((W // 2, y), s, font=f, fill=fg, anchor="mm")


def product(name, box):
    im = Image.open(IMG / f"{name}.png").convert("RGBA")
    im.thumbnail(box)
    return im


def card(img, d, box, head, prod, big, sub, color):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 30, fill=WHITE)
    d.rounded_rectangle([x0, y0, x1, y0 + 100], 30, fill=color)
    d.rectangle([x0, y0 + 70, x1, y0 + 100], fill=color)
    cx = (x0 + x1) // 2
    d.text((cx, y0 + 50), head, font=font(40), fill=WHITE, anchor="mm")
    p = product(prod, (x1 - x0 - 70, 300))
    img.paste(p, (cx - p.width // 2, y0 + 120 + (300 - p.height) // 2), p)
    d.text((cx, y0 + 490), big, font=font(100), fill=color, anchor="mm")
    d.text((cx, y0 + 580), sub, font=font(36, False), fill=INK, anchor="mm")


def table(d, y0, head, rows, win_col):
    cols = [80, 400, 640, 870]
    d.rounded_rectangle([50, y0 - 60, 1030, y0 + 60], 18, fill=BLUE)
    for c, h in zip(cols[1:], head):
        d.text((c + 5, y0), h, font=font(36), fill=WHITE, anchor="mm")
    for i, row in enumerate(rows):
        y = y0 + 150 + i * 140
        d.rounded_rectangle([50, y - 58, 1030, y + 58], 18, fill=WHITE)
        d.text((cols[0], y), row[0], font=font(38), fill=CHAR, anchor="lm")
        for j, v in enumerate(row[1:]):
            win = j == win_col[i]
            d.text((cols[j + 1] + 5, y), v, font=font(40 if win else 38, win), fill=(0, 150, 110) if win else INK, anchor="mm")


# ---------- ALLPOWERS: same 256Wh, $70 less ----------
def a_hook(d, p, img):
    text(d, 400, "SAME 256Wh.", 96)
    text(d, 510, "SAME LiFePO4.", 96, GOLD)
    card(img, d, [60, 610, 525, 1230], "EcoFlow RIVER 2", "river2", "$209", "RIVER 2 (240)", RED)
    card(img, d, [555, 610, 1020, 1230], "ALLPOWERS", "volix", "$139", "VOLIX P300", GREEN)
    text(d, 1340, "Why pay $70 more?", 70, GOLD)
    text(d, 1430, "Prices checked Sep 28, 2026", 34, MUTED, False)


def a_specs(d, p, img):
    text(d, 400, "VOLIX P300", 100, GOLD)
    im = product("volix", (620, 480))
    img.paste(im, ((W - im.width) // 2, 480), im)
    rows = ["256Wh LiFePO4 battery", "300W output", "2,500+ cycles to 80%", "About $0.54 per Wh"]
    for i, s in enumerate(rows):
        if p > i * .15:
            y = 1080 + i * 120
            d.ellipse([140, y - 16, 172, y + 16], fill=GREEN)
            d.text((205, y), s, font=font(58), fill=WHITE, anchor="lm")


def a_use(d, p, img):
    text(d, 420, "GOOD FOR", 100, GOLD)
    rows = ["Phones, laptops, tablets", "Camp lights and fans", "Short power outages", "Tailgates and road trips"]
    for i, s in enumerate(rows):
        if p > i * .15:
            y = 620 + i * 150
            d.rounded_rectangle([110, y - 60, 970, y + 60], 18, fill=WHITE)
            d.text((150, y), s, font=font(54), fill=CHAR, anchor="lm")
    text(d, 1280, "Not for fridges or AC units:", 46, MUTED, False)
    text(d, 1350, "300W is small-device power.", 46, MUTED, False)


def a_cta(d, p, img):
    text(d, 400, "$139 TODAY", 110, GREEN)
    text(d, 510, "Regular $249 \u2022 price can change", 44, MUTED, False)
    im = product("volix", (640, 520))
    img.paste(im, ((W - im.width) // 2, 590), im)
    pill(d, 1250, "Full review \u2192 link in bio", size=56)


ALLPOWERS = dict(
    key="allpowers", slug="set-allpowers-p300-vs-river2",
    segments=[
        "Same two hundred fifty six watt hours. Same LiFePO4 battery. EcoFlow's RIVER 2 is two hundred nine dollars. "
        "The ALLPOWERS VOLIX P300 is one thirty nine.",
        "You get three hundred watts of output, over twenty five hundred charge cycles, "
        "and about fifty four cents per watt hour.",
        "It's made for phones, laptops, lights, fans, and short outages. Not fridges or air conditioners.",
        "One thirty nine as of today, down from two forty nine. Prices change, so check the full review at the link in bio.",
    ],
    funcs=[a_hook, a_specs, a_use, a_cta],
)


# ---------- BLUETTI: 1kWh weigh-in ----------
def b_hook(d, p, img):
    text(d, 400, "1kWh WEIGH-IN", 96)
    text(d, 505, "Same class. Different weight.", 56, GOLD)
    card(img, d, [60, 610, 525, 1230], "EcoFlow DELTA 3 Plus", "delta3plus", "30 lbs", "1,024Wh", RED)
    card(img, d, [555, 610, 1020, 1230], "BLUETTI", "elite", "23.6 lbs", "Elite 100 Mini \u2022 1,004.8Wh", GREEN)
    text(d, 1340, "6.4 lbs lighter.", 76, GOLD)
    text(d, 1430, "Manufacturer specs", 34, MUTED, False)


def b_table(d, p, img):
    text(d, 400, "THE TRADE-OFFS", 84, GOLD)
    for i, n in enumerate(["elite", "delta3plus", "jackery1000"]):
        cx = [405, 645, 875][i]
        d.rounded_rectangle([cx - 100, 480, cx + 100, 680], 18, fill=WHITE)
        im = product(n, (170, 170))
        img.paste(im, (cx - im.width // 2, 580 - im.height // 2), im)
    table(d, 760, ["BLUETTI", "EcoFlow", "Jackery"],
          [("Weight", "23.6 lb", "30 lb", "24.2 lb"),
           ("Capacity", "1,005Wh", "1,024Wh", "1,070Wh"),
           ("Output", "1,000W", "1,800W", "1,000W"),
           ("AC charge", "80% 45m", "100% 56m", "80% 60m")],
          win_col=[0, 2, 1, 0])
    text(d, 1440, "Elite 100 Mini • DELTA 3 Plus • Explorer 1000 v2", 36, MUTED, False)


def b_who(d, p, img):
    text(d, 420, "PICK THE MINI IF", 90, GOLD)
    rows = ["You carry it often", "Camping, RV, tailgates", "Phones, laptops, lights, fans", "You want 1,000W, not 1,800W"]
    for i, s in enumerate(rows):
        if p > i * .15:
            y = 620 + i * 150
            d.rounded_rectangle([90, y - 60, 990, y + 60], 18, fill=WHITE)
            d.text((130, y), s, font=font(50), fill=CHAR, anchor="lm")
    text(d, 1280, "Need to run bigger appliances?", 46, MUTED, False)
    text(d, 1350, "The DELTA 3 Plus has more output.", 46, MUTED, False)


def b_cta(d, p, img):
    text(d, 400, "BLUETTI ELITE 100 MINI", 76, GREEN)
    text(d, 500, "From $479 with carry bag \u2022 Sep 28, 2026", 42, MUTED, False)
    im = product("elite", (560, 600))
    img.paste(im, ((W - im.width) // 2, 580), im)
    pill(d, 1300, "Full review \u2192 link in bio", size=56)


BLUETTI = dict(
    key="bluetti", slug="set-bluetti-elite100mini-weigh-in",
    segments=[
        "Two one kilowatt hour power stations. EcoFlow's DELTA 3 Plus weighs thirty pounds. "
        "BLUETTI's Elite 100 Mini weighs twenty three point six. That's six pounds lighter.",
        "The trade off: the DELTA 3 Plus has more output, eighteen hundred watts versus one thousand. "
        "The Mini charges to eighty percent in about forty five minutes.",
        "Pick the Mini if you carry it a lot. Camping, RVs, tailgates, phones and laptops.",
        "It starts at four seventy nine with a carry bag as of today. Full review at the link in bio.",
    ],
    funcs=[b_hook, b_table, b_who, b_cta],
)


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


async def voiceover(cfg):
    seg = D / f"{cfg['slug']}-vo"
    seg.mkdir(exist_ok=True)
    slides, parts, t = [], [], 0.3
    for i, s in enumerate(cfg["segments"]):
        mp3 = seg / f"seg{i + 1}.mp3"
        await edge_tts.Communicate(s, VOICE, rate="+10%").save(str(mp3))
        d = dur(mp3)
        slides.append([0.0 if i == 0 else round(t, 2), round(t + d + GAP, 2)])
        parts.append((mp3, t))
        t += d + GAP
    slides[-1][1] = round(t + 1.5, 2)
    total = slides[-1][1]
    wav = seg / "voiceover.wav"
    inputs, filt = [], []
    for i, (mp3, start) in enumerate(parts):
        inputs += ["-i", str(mp3)]
        ms = int(start * 1000)
        filt.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    filt.append("".join(f"[a{i}]" for i in range(len(parts))) +
                f"amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{total}[out]")
    subprocess.run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]",
                    "-ar", "44100", "-c:a", "pcm_s16le", str(wav)], check=True, capture_output=True)
    return slides, total, wav


def render(cfg):
    slides, total, wav = asyncio.run(voiceover(cfg))

    def frame(t):
        for i, ((a, b), fn) in enumerate(zip(slides, cfg["funcs"])):
            if a <= t < b or (i == len(slides) - 1 and t >= a):
                img = BG.copy()
                fn(ImageDraw.Draw(img), (t - a) / (b - a), img)
                fade = 1 if i == 0 else min(1, (t - a) / 0.25)
                return Image.blend(BG, img, fade) if fade < 1 else img
        return BG

    out = D / f"{cfg['slug']}.mp4"
    cmd = ["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", str(wav), "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for i in range(int(total * FPS)):
        ff.stdin.write(frame(i / FPS).tobytes())
    ff.stdin.close()
    ff.wait()
    for i, (a, b) in enumerate(slides):
        frame(a + (b - a) * 0.95).save(D / f"{cfg['slug']}-slide{i + 1}.png")
    EXPORTS.mkdir(parents=True, exist_ok=True)
    (EXPORTS / out.name).write_bytes(out.read_bytes())
    print(f"{cfg['key']}: {total:.1f}s -> {out.name} (+ OneDrive export)")


if __name__ == "__main__":
    want = sys.argv[1:] or ["allpowers", "bluetti"]
    for cfg in (ALLPOWERS, BLUETTI):
        if cfg["key"] in want:
            render(cfg)
