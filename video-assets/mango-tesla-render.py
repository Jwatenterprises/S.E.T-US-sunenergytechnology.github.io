"""
S.E.T. Solar — Mango Power E vs Tesla Powerwall 3 TikTok Ad
Local ffmpeg render — 7 shots, price-shock hook, stacking angle
Real product images, AriaNeural voiceover, 9:16 vertical
"""
import os
import subprocess
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
VO_DIR = os.path.join(BASE, "mango-tesla-vo")
IMG_DIR = os.path.join(os.path.dirname(BASE), "images", "mango-power")
TEMP_DIR = os.path.join(BASE, "mango-tesla-temp")
OUT_DIR = os.path.expanduser("~/OneDrive/video-assets/exports")
LOGO = os.path.join(os.path.dirname(BASE), "set-logo.jpg")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

FONT_BOLD = "/Windows/Fonts/arialbd.ttf"
FONT_REG = "/Windows/Fonts/arial.ttf"

def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True
    )
    return float(r.stdout.strip())

# --- Shot definitions ---
shots = [
    {
        # Scene 1: HOOK — price shock
        "line": "line1.mp3",
        "text": "$13,000 vs $1,299",
        "sub": "HOME BATTERY BACKUP",
        "img": None,
        "bg": "0x0a1020",
        "type": "hook",
    },
    {
        # Scene 2: THE PROBLEM
        "line": "line2.mp3",
        "text": "NO BATTERY = NO BACKUP",
        "sub": "Solar panels shut off during outages",
        "img": None,
        "bg": "0x0f1825",
        "type": "text",
    },
    {
        # Scene 3: TESLA REALITY
        "line": "line3.mp3",
        "text": "TESLA POWERWALL 3",
        "sub": "$8,400 + $4,000 Install + 6 Month Wait",
        "img": None,
        "bg": "0x1a0505",
        "type": "tesla",
    },
    {
        # Scene 4: THE REVEAL — Mango Power E
        "line": "line4.mp3",
        "text": "MANGO POWER E",
        "sub": "Ships to your door — $1,299",
        "img": "mango-power-e-main.jpg",
        "bg": "0x0d1826",
        "type": "product",
    },
    {
        # Scene 5: THE SPECS
        "line": "line5.mp3",
        "text": "3,500 Wh \\u2192 14,000 Wh",
        "sub": "CATL LFP \\u00b7 10-Yr Warranty \\u00b7 6,000 Cycles",
        "img": "mango-power-e-specs.jpg",
        "bg": "0x0d1826",
        "type": "product",
    },
    {
        # Scene 6: STACKING
        "line": "line6.mp3",
        "text": "STACK TO SCALE",
        "sub": "3 Units = 10,500 Wh — $3,897",
        "img": "mango-power-e-14kwh.jpg",
        "bg": "0x0a1628",
        "type": "stack",
    },
    {
        # Scene 7: CTA
        "line": "line7.mp3",
        "text": "S.E.T. Solar",
        "sub": "Link in bio \\u2193",
        "img": None,
        "bg": "0x0d1826",
        "type": "endcard",
    },
]

# --- Get durations ---
PAD = 0.5
for s in shots:
    vo_path = os.path.join(VO_DIR, s["line"])
    s["dur"] = get_duration(vo_path)
    s["total"] = s["dur"] + PAD
    print(f"  {s['line']}: {s['dur']:.2f}s (padded: {s['total']:.2f}s)")

total_dur = sum(s["total"] for s in shots)
print(f"\nTotal video duration: {total_dur:.1f}s")

# --- Render each shot ---
clip_files = []

for i, s in enumerate(shots):
    print(f"\nRendering shot {i+1}/{len(shots)}: {s.get('text', '')[:40]}...")
    clip_path = os.path.join(TEMP_DIR, f"shot{i:02d}.mp4")
    vo_path = os.path.join(VO_DIR, s["line"])
    dur = f"{s['total']:.3f}"

    if s["type"] == "hook":
        # Big price shock — gold numbers, dark bg
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c={s['bg']}:s=1080x1920:d={dur}:r=30",
            "-i", vo_path,
            "-filter_complex",
            f"[0:v]drawtext=text='$13,000':"
            f"fontsize=100:fontcolor=0xcc0000:x=(w-text_w)/2:y=(h/2)-180:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='vs':"
            f"fontsize=40:fontcolor=0x808080:x=(w-text_w)/2:y=(h/2)-60:"
            f"fontfile={FONT_REG},"
            f"drawtext=text='$1,299':"
            f"fontsize=120:fontcolor=0xd4940a:x=(w-text_w)/2:y=(h/2)+10:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='HOME BATTERY BACKUP':"
            f"fontsize=28:fontcolor=0xa0a0a0:x=(w-text_w)/2:y=(h/2)+180:"
            f"fontfile={FONT_REG}"
            f"[out]",
            "-map", "[out]", "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p", "-t", dur,
            clip_path
        ]

    elif s["type"] == "tesla":
        # Tesla cost breakdown — red accent
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c={s['bg']}:s=1080x1920:d={dur}:r=30",
            "-i", vo_path,
            "-filter_complex",
            f"[0:v]drawtext=text='{s['text']}':"
            f"fontsize=60:fontcolor=0xcc0000:x=(w-text_w)/2:y=(h/2)-120:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='$8,400 Unit':"
            f"fontsize=42:fontcolor=white:x=(w-text_w)/2:y=(h/2):"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='+ $4,000 Installation':"
            f"fontsize=42:fontcolor=white:x=(w-text_w)/2:y=(h/2)+60:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='+ 6 Month Waitlist':"
            f"fontsize=42:fontcolor=0xfc8181:x=(w-text_w)/2:y=(h/2)+120:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='= $13,000+ INSTALLED':"
            f"fontsize=36:fontcolor=0xcc0000:x=(w-text_w)/2:y=(h/2)+220:"
            f"fontfile={FONT_BOLD}"
            f"[out]",
            "-map", "[out]", "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p", "-t", dur,
            clip_path
        ]

    elif s["type"] == "product" and s["img"]:
        # Product shot with image
        img_path = os.path.join(IMG_DIR, s["img"])
        esc_text = s["text"].encode("unicode_escape").decode("ascii")
        esc_sub = s["sub"].encode("unicode_escape").decode("ascii")
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c={s['bg']}:s=1080x1920:d={dur}:r=30",
            "-i", img_path,
            "-i", vo_path,
            "-filter_complex",
            f"[1:v]scale=900:-1:force_original_aspect_ratio=decrease,scale='min(900,iw)':'min(900,ih)':force_original_aspect_ratio=decrease[prod];"
            f"[0:v][prod]overlay=(W-w)/2:(H/2-h)/2+40[bg];"
            f"[bg]drawtext=text='{esc_text}':"
            f"fontsize=52:fontcolor=0xd4940a:x=(w-text_w)/2:y=h-350:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='{esc_sub}':"
            f"fontsize=28:fontcolor=0x00d4aa:x=(w-text_w)/2:y=h-280:"
            f"fontfile={FONT_REG}"
            f"[out]",
            "-map", "[out]", "-map", "2:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p", "-t", dur,
            clip_path
        ]

    elif s["type"] == "stack":
        # Stacking shot with image
        img_path = os.path.join(IMG_DIR, s["img"])
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c={s['bg']}:s=1080x1920:d={dur}:r=30",
            "-i", img_path,
            "-i", vo_path,
            "-filter_complex",
            f"[1:v]scale=800:-1:force_original_aspect_ratio=decrease[prod];"
            f"[0:v][prod]overlay=(W-w)/2:180[bg];"
            f"[bg]drawtext=text='STACK TO SCALE':"
            f"fontsize=60:fontcolor=0xd4940a:x=(w-text_w)/2:y=h-440:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='1x = 3,500 Wh   $1,299':"
            f"fontsize=32:fontcolor=white:x=(w-text_w)/2:y=h-360:"
            f"fontfile={FONT_REG},"
            f"drawtext=text='2x = 7,000 Wh   $2,598':"
            f"fontsize=32:fontcolor=white:x=(w-text_w)/2:y=h-310:"
            f"fontfile={FONT_REG},"
            f"drawtext=text='3x = 10,500 Wh  $3,897':"
            f"fontsize=36:fontcolor=0x00d4aa:x=(w-text_w)/2:y=h-250:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='vs 1 Powerwall = $13,000+':"
            f"fontsize=28:fontcolor=0xfc8181:x=(w-text_w)/2:y=h-180:"
            f"fontfile={FONT_REG}"
            f"[out]",
            "-map", "[out]", "-map", "2:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p", "-t", dur,
            clip_path
        ]

    elif s["type"] == "endcard":
        # End card with logo
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c={s['bg']}:s=1080x1920:d={dur}:r=30",
            "-i", LOGO,
            "-i", vo_path,
            "-filter_complex",
            f"[1:v]scale=300:-1[logo];"
            f"[0:v][logo]overlay=(W-w)/2:(H-h)/2-200[bg];"
            f"[bg]drawtext=text='S.E.T. Solar':"
            f"fontsize=56:fontcolor=white:x=(w-text_w)/2:y=(h/2)+40:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='MANGO POWER E — $1,299':"
            f"fontsize=34:fontcolor=0xd4940a:x=(w-text_w)/2:y=(h/2)+110:"
            f"fontfile={FONT_BOLD},"
            f"drawtext=text='Link in bio':"
            f"fontsize=30:fontcolor=0x00d4aa:x=(w-text_w)/2:y=(h/2)+160:"
            f"fontfile={FONT_REG},"
            f"drawtext=text='sunenergytechnology.com':"
            f"fontsize=24:fontcolor=0xe0e0e0:x=(w-text_w)/2:y=(h/2)+210:"
            f"fontfile={FONT_REG}"
            f"[out]",
            "-map", "[out]", "-map", "2:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p", "-t", dur,
            clip_path
        ]

    else:
        # Text-only
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c={s['bg']}:s=1080x1920:d={dur}:r=30",
            "-i", vo_path,
            "-filter_complex",
            f"[0:v]drawtext=text='{s['text']}':"
            f"fontsize=56:fontcolor=white:x=(w-text_w)/2:y=(h/2)-40:"
            f"fontfile={FONT_BOLD}:line_spacing=20,"
            f"drawtext=text='{s['sub']}':"
            f"fontsize=30:fontcolor=0x00d4aa:x=(w-text_w)/2:y=(h/2)+80:"
            f"fontfile={FONT_REG}"
            f"[out]",
            "-map", "[out]", "-map", "1:a",
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
    print(f"\nWARNING: Only {len(clip_files)}/{len(shots)} shots rendered!")

# --- Concatenate all shots ---
print(f"\nConcatenating {len(clip_files)} shots...")
concat_list = os.path.join(TEMP_DIR, "concat.txt")
with open(concat_list, "w") as f:
    for c in clip_files:
        f.write(f"file '{c}'\n")

out_path = os.path.join(OUT_DIR, "tiktok-mango-vs-tesla-powerwall.mp4")
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
    print(f"CONCAT FAILED: {result.stderr[-500:]}")
else:
    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print(f"\n✅ DONE: {out_path}")
    print(f"   Size: {size_mb:.1f} MB")
    print(f"   Duration: {total_dur:.1f}s")
    print(f"   Format: 1080x1920 (9:16 vertical)")

# Also copy to local exports
local_out = os.path.join(os.path.dirname(BASE), "video-assets", "exports", "tiktok-mango-vs-tesla-powerwall.mp4")
shutil.copy2(out_path, local_out)
print(f"   Local copy: {local_out}")
