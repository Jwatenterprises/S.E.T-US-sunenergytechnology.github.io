"""
S.E.T. Store — Segway vs Razor Go-Karts Comparison (Video #30)
TikTok format: 9:16, price-shock hook, ~40-45s
Products: Segway GoKart Pro 2, Razor Crazy Cart, Razor Ground Force
"""
import os
import subprocess
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
VO_DIR = os.path.join(BASE, "gokart-vs-vo")
IMG_DIR = os.path.join(BASE, "gokart-images")
TEMP_DIR = os.path.join(BASE, "gokart-vs-temp")
OUT_DIR = os.path.expanduser("~/OneDrive/video-assets/exports")
LOGO = os.path.join(os.path.dirname(BASE), "set-logo.jpg")

os.makedirs(VO_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

FONT_BOLD = "/Windows/Fonts/arialbd.ttf"
FONT_REG = "/Windows/Fonts/arial.ttf"

# ============================================================
# STEP 1: Generate voiceover with edge-tts
# ============================================================
LINES = [
    ("line1.mp3", "Would you pay fifteen hundred dollars for a go-kart?"),
    ("line2.mp3", "The Segway GoKart Pro Two hits twenty-seven miles per hour. It transforms into a scooter, a mecha kit, and a go-kart. Premium build. Ages fourteen and up."),
    ("line3.mp3", "The Razor Crazy Cart? Four sixty-three. Twelve miles per hour with a drift bar that lets you spin three-sixty while driving. Pure fun. Ages nine and up."),
    ("line4.mp3", "Or the Razor Ground Force at just one seventy-five. Twelve miles per hour, steel frame, forty-minute runtime. Best starter kart for kids eight and up."),
    ("line5.mp3", "Want speed? Segway. Want to drift? Crazy Cart. Want value? Ground Force. All three ship from Amazon."),
    ("line6.mp3", "Links in bio. S.E.T. Store."),
]

print("🎤 Generating voiceover...")
for fname, text in LINES:
    out_path = os.path.join(VO_DIR, fname)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"  {fname} — exists, skipping")
        continue
    cmd = f'edge-tts --voice en-US-AriaNeural --rate=+5% --text "{text}" --write-media "{out_path}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        print(f"  {fname} — OK ({os.path.getsize(out_path)//1024} KB)")
    else:
        print(f"  {fname} — FAILED: {result.stderr[:200]}")
        exit(1)

# ============================================================
# STEP 2: Get durations
# ============================================================
def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True
    )
    return float(r.stdout.strip())

PAD = 0.5
shots = [
    {
        "line": "line1.mp3",
        "type": "hook",
        "text_main": "$1,499 vs $175",
        "text_sub": "ELECTRIC GO-KARTS",
    },
    {
        "line": "line2.mp3",
        "type": "product",
        "img": "segway_pro2.jpg",
        "text_main": "SEGWAY GOKART PRO 2",
        "text_sub": "$1,499 | 26.7 MPH | 3-in-1",
        "badge": "PREMIUM PICK",
        "accent": "0x00b4d8",
    },
    {
        "line": "line3.mp3",
        "type": "product",
        "img": "razor_crazy_xl.jpg",
        "text_main": "RAZOR CRAZY CART",
        "text_sub": "$463 | 12 MPH | 360° Drift Bar",
        "badge": "BEST DRIFTER",
        "accent": "0xe63946",
    },
    {
        "line": "line4.mp3",
        "type": "product",
        "img": "razor_gf_one.png",
        "text_main": "RAZOR GROUND FORCE",
        "text_sub": "$175 | 12 MPH | Ages 8+",
        "badge": "BEST VALUE",
        "accent": "0x2ec46d",
    },
    {
        "line": "line5.mp3",
        "type": "compare",
        "text_main": "WHICH ONE IS RIGHT?",
    },
    {
        "line": "line6.mp3",
        "type": "endcard",
        "text_main": "S.E.T. Store",
        "text_sub": "Links in bio",
    },
]

print("\n⏱ Shot durations:")
for s in shots:
    vo_path = os.path.join(VO_DIR, s["line"])
    s["dur"] = get_duration(vo_path)
    s["total"] = s["dur"] + PAD
    print(f"  {s['line']}: {s['dur']:.2f}s (padded: {s['total']:.2f}s)")

total_dur = sum(s["total"] for s in shots)
print(f"\nTotal video: {total_dur:.1f}s")

# ============================================================
# STEP 3: Render each shot
# ============================================================
clip_files = []

for i, s in enumerate(shots):
    print(f"\nRendering shot {i+1}/{len(shots)}: {s.get('text_main', '')[:30]}...")
    clip_path = os.path.join(TEMP_DIR, f"shot{i:02d}.mp4")
    vo_path = os.path.join(VO_DIR, s["line"])
    dur = f"{s['total']:.3f}"

    if s["type"] == "hook":
        # Big price shock
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=0x0a1020:s=1080x1920:d={dur}:r=30",
            "-i", vo_path,
            "-filter_complex",
            f"[0:v]drawtext=text='$1,499':"
            f"fontsize=90:fontcolor=0x00b4d8:x=(w-text_w)/2:y=(h/2)-180:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='vs':"
            f"fontsize=40:fontcolor=0x808080:x=(w-text_w)/2:y=(h/2)-60:"
            f"fontfile={FONT_REG},"
            f"drawtext=text='$175':"
            f"fontsize=120:fontcolor=0x2ec46d:x=(w-text_w)/2:y=(h/2)+10:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='ELECTRIC GO-KARTS':"
            f"fontsize=32:fontcolor=0xa0a0a0:x=(w-text_w)/2:y=(h/2)+180:"
            f"fontfile={FONT_REG},"
            f"drawtext=text='Which one is worth it?':"
            f"fontsize=28:fontcolor=0xe63946:x=(w-text_w)/2:y=(h/2)+230:"
            f"fontfile={FONT_REG}"
            f"[out]",
            "-map", "[out]", "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p", "-t", dur,
            clip_path
        ]

    elif s["type"] == "product":
        img_path = os.path.join(IMG_DIR, s["img"])
        accent = s.get("accent", "0x00d4aa")
        badge = s.get("badge", "")
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=0x0d1826:s=1080x1920:d={dur}:r=30",
            "-i", img_path,
            "-i", vo_path,
            "-filter_complex",
            f"[1:v]scale=900:-1:force_original_aspect_ratio=decrease,"
            f"scale='min(900,iw)':'min(900,ih)':force_original_aspect_ratio=decrease[prod];"
            f"[0:v][prod]overlay=(W-w)/2:(H/2-h)/2+40[bg];"
            f"[bg]drawtext=text='{badge}':"
            f"fontsize=24:fontcolor={accent}:x=(w-text_w)/2:y=h-420:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='{s['text_main']}':"
            f"fontsize=52:fontcolor=white:x=(w-text_w)/2:y=h-370:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='{s['text_sub']}':"
            f"fontsize=28:fontcolor={accent}:x=(w-text_w)/2:y=h-300:"
            f"fontfile={FONT_REG}"
            f"[out]",
            "-map", "[out]", "-map", "2:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p", "-t", dur,
            clip_path
        ]

    elif s["type"] == "compare":
        # Side-by-side comparison text
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=0x0a1628:s=1080x1920:d={dur}:r=30",
            "-i", vo_path,
            "-filter_complex",
            f"[0:v]drawtext=text='WHICH ONE IS RIGHT?':"
            f"fontsize=52:fontcolor=white:x=(w-text_w)/2:y=(h/2)-260:"
            f"fontfile={FONT_BOLD},"
            # Segway row
            f"drawtext=text='SPEED':"
            f"fontsize=28:fontcolor=0x808080:x=80:y=(h/2)-160:"
            f"fontfile={FONT_REG},"
            f"drawtext=text='Segway Pro 2':"
            f"fontsize=34:fontcolor=0x00b4d8:x=80:y=(h/2)-120:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='$1,499':"
            f"fontsize=28:fontcolor=white:x=w-200:y=(h/2)-120:"
            f"fontfile={FONT_BOLD},"
            # Razor Crazy Cart row
            f"drawtext=text='DRIFT':"
            f"fontsize=28:fontcolor=0x808080:x=80:y=(h/2)-40:"
            f"fontfile={FONT_REG},"
            f"drawtext=text='Crazy Cart':"
            f"fontsize=34:fontcolor=0xe63946:x=80:y=(h/2):"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='$463':"
            f"fontsize=28:fontcolor=white:x=w-200:y=(h/2):"
            f"fontfile={FONT_BOLD},"
            # Ground Force row
            f"drawtext=text='VALUE':"
            f"fontsize=28:fontcolor=0x808080:x=80:y=(h/2)+80:"
            f"fontfile={FONT_REG},"
            f"drawtext=text='Ground Force':"
            f"fontsize=34:fontcolor=0x2ec46d:x=80:y=(h/2)+120:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='$175':"
            f"fontsize=28:fontcolor=white:x=w-200:y=(h/2)+120:"
            f"fontfile={FONT_BOLD},"
            # All ship note
            f"drawtext=text='All 3 ship from Amazon':"
            f"fontsize=26:fontcolor=0xd4940a:x=(w-text_w)/2:y=(h/2)+220:"
            f"fontfile={FONT_REG}"
            f"[out]",
            "-map", "[out]", "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p", "-t", dur,
            clip_path
        ]

    elif s["type"] == "endcard":
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=0x0d1826:s=1080x1920:d={dur}:r=30",
            "-i", LOGO,
            "-i", vo_path,
            "-filter_complex",
            f"[1:v]scale=300:-1[logo];"
            f"[0:v][logo]overlay=(W-w)/2:(H-h)/2-200[bg];"
            f"[bg]drawtext=text='S.E.T. Store':"
            f"fontsize=56:fontcolor=white:x=(w-text_w)/2:y=(h/2)+40:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='Segway \\u00b7 Razor \\u00b7 Electric Go-Karts':"
            f"fontsize=28:fontcolor=0xd4940a:x=(w-text_w)/2:y=(h/2)+110:"
            f"fontfile={FONT_REG},"
            f"drawtext=text='Links in bio':"
            f"fontsize=30:fontcolor=0x00d4aa:x=(w-text_w)/2:y=(h/2)+160:"
            f"fontfile={FONT_REG},"
            f"drawtext=text='sunenergytechnology.com/store':"
            f"fontsize=24:fontcolor=0xe0e0e0:x=(w-text_w)/2:y=(h/2)+210:"
            f"fontfile={FONT_REG}"
            f"[out]",
            "-map", "[out]", "-map", "2:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p", "-t", dur,
            clip_path
        ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print(f"  FAILED: {result.stderr[-500:]}")
        continue
    else:
        size_mb = os.path.getsize(clip_path) / 1024 / 1024
        print(f"  OK — {size_mb:.1f} MB")
        clip_files.append(clip_path)

if len(clip_files) != len(shots):
    print(f"\n⚠️  Only {len(clip_files)}/{len(shots)} shots rendered!")

# ============================================================
# STEP 4: Concatenate
# ============================================================
print(f"\nConcatenating {len(clip_files)} shots...")
concat_list = os.path.join(TEMP_DIR, "concat.txt")
with open(concat_list, "w") as f:
    for c in clip_files:
        f.write(f"file '{c}'\n")

out_path = os.path.join(OUT_DIR, "video30-segway-vs-razor-gokarts.mp4")
concat_cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", concat_list,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k",
    "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    out_path
]

result = subprocess.run(concat_cmd, capture_output=True, text=True, timeout=120)
if result.returncode != 0:
    print(f"\n❌ CONCAT FAILED: {result.stderr[-500:]}")
else:
    size_mb = os.path.getsize(out_path) / 1024 / 1024
    final_dur = get_duration(out_path)
    print(f"\n✅ DONE: {out_path}")
    print(f"   Size: {size_mb:.1f} MB")
    print(f"   Duration: {final_dur:.1f}s")
    print(f"   Format: 1080x1920 (9:16)")

# Debug screenshot at t=7s (should show Segway product)
debug = os.path.join(TEMP_DIR, "debug-frame.jpg")
subprocess.run([
    "ffmpeg", "-y", "-ss", "7", "-i", out_path,
    "-frames:v", "1", "-q:v", "2", debug
], capture_output=True, timeout=30)
print(f"   Debug frame: {debug}")
