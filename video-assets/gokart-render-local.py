"""
S.E.T. Store — Electric Go-Kart Promo Video (Video #28)
Local ffmpeg render — no Shotstack credits needed.
Products: Segway GoKart Pro 2, Razor Crazy Cart XL, Ground Force Elite, Ground Force One
Real product images, AriaNeural voiceover
"""
import os
import subprocess
import urllib.request
import shutil
import json

BASE = os.path.dirname(os.path.abspath(__file__))
VO_DIR = os.path.join(BASE, "gokart-voiceover")
IMG_DIR = os.path.join(BASE, "gokart-images")
TEMP_DIR = os.path.join(BASE, "gokart-temp")
OUT_DIR = os.path.expanduser("~/OneDrive/video-assets/exports")
LOGO = os.path.join(os.path.dirname(BASE), "set-logo.jpg")

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# --- Product images to download ---
IMAGES = {
    "segway_pro2.jpg": "https://images.techeblog.com/wp-content/uploads/2025/07/23133944/segway-gokart-pro-2.jpg",
    "razor_crazy_xl.jpg": "https://razor.com/wp-content/uploads/2025/04/Crazy_Cart_XL_Product_photo_001.jpg",
    "razor_gf_elite.png": "https://razor.com/wp-content/uploads/2025/04/GroundForceElite_Product_001.png",
    "razor_gf_one.png": "https://razor.com/wp-content/uploads/2025/04/GroundForce_SL_Product.png",
}

# --- Download product images ---
print("Downloading product images...")
for fname, url in IMAGES.items():
    dest = os.path.join(IMG_DIR, fname)
    if os.path.exists(dest):
        print(f"  {fname} — already exists")
        continue
    print(f"  {fname} — downloading...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp, open(dest, "wb") as f:
            f.write(resp.read())
        print(f"  {fname} — OK ({os.path.getsize(dest)//1024} KB)")
    except Exception as e:
        print(f"  {fname} — FAILED: {e}")

# --- Voiceover durations ---
def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True
    )
    return float(r.stdout.strip())

shots = [
    {"line": "line1.mp3", "text": "Electric Go-Karts\\nAre Here", "sub": "", "img": None, "bg": "#0a1628"},
    {"line": "line2.mp3", "text": "Segway GoKart Pro 2", "sub": "$1,499 | 26.7 MPH | 4,800W", "img": "segway_pro2.jpg", "bg": "#0d1826"},
    {"line": "line3.mp3", "text": "Razor Crazy Cart XL", "sub": "$1,259 | 14 MPH | Drift System", "img": "razor_crazy_xl.jpg", "bg": "#0d1826"},
    {"line": "line4.mp3", "text": "Razor Ground Force Elite", "sub": "$549 | 14 MPH | Ages 13+", "img": "razor_gf_elite.png", "bg": "#0d1826"},
    {"line": "line5.mp3", "text": "Razor Ground Force One", "sub": "$299 | 12 MPH | Ages 8+", "img": "razor_gf_one.png", "bg": "#0d1826"},
    {"line": "line6.mp3", "text": "S.E.T. Solar", "sub": "Full guide + links in bio", "img": None, "bg": "#0d1826", "endcard": True},
]

# Get durations
PAD = 0.5
for s in shots:
    vo_path = os.path.join(VO_DIR, s["line"])
    s["dur"] = get_duration(vo_path)
    s["total"] = s["dur"] + PAD
    print(f"  {s['line']}: {s['dur']:.2f}s (total: {s['total']:.2f}s)")

total_dur = sum(s["total"] for s in shots)
print(f"\nTotal video duration: {total_dur:.1f}s")

# --- Generate each shot as a short clip, then concatenate ---
clip_files = []

for i, s in enumerate(shots):
    print(f"\nRendering shot {i+1}/{len(shots)}: {s['text'][:30]}...")
    clip_path = os.path.join(TEMP_DIR, f"shot{i:02d}.mp4")
    vo_path = os.path.join(VO_DIR, s["line"])

    if s.get("endcard"):
        # End card with logo
        logo_path = LOGO
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=0x0d1826:s=1080x1920:d={s['total']:.3f}:r=30",
            "-i", logo_path,
            "-i", vo_path,
            "-filter_complex",
            # Place logo centered, add text below
            f"[1:v]scale=300:-1[logo];"
            f"[0:v][logo]overlay=(W-w)/2:(H-h)/2-200[bg];"
            f"[bg]drawtext=text='{s['text']}':"
            f"fontsize=56:fontcolor=white:x=(w-text_w)/2:y=(h/2)+40:"
            f"font=Arial:fontfile=/Windows/Fonts/arialbd.ttf,"
            f"drawtext=text='{s['sub']}':"
            f"fontsize=30:fontcolor=0x00d4aa:x=(w-text_w)/2:y=(h/2)+110:"
            f"font=Arial:fontfile=/Windows/Fonts/arial.ttf,"
            f"drawtext=text='sunenergytechnology.com':"
            f"fontsize=24:fontcolor=0xe0e0e0:x=(w-text_w)/2:y=(h/2)+160:"
            f"font=Arial:fontfile=/Windows/Fonts/arial.ttf"
            f"[out]",
            "-map", "[out]", "-map", "2:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-t", f"{s['total']:.3f}",
            clip_path
        ]
    elif s["img"]:
        # Product shot: dark bg + product image centered top + text bottom
        img_path = os.path.join(IMG_DIR, s["img"])
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=0x0d1826:s=1080x1920:d={s['total']:.3f}:r=30",
            "-i", img_path,
            "-i", vo_path,
            "-filter_complex",
            # Scale product image to fit upper portion, overlay centered
            f"[1:v]scale=900:-1:force_original_aspect_ratio=decrease,scale='min(900,iw)':'min(900,ih)':force_original_aspect_ratio=decrease[prod];"
            f"[0:v][prod]overlay=(W-w)/2:(H/2-h)/2[bg];"
            f"[bg]drawtext=text='{s['text']}':"
            f"fontsize=52:fontcolor=white:x=(w-text_w)/2:y=h-320:"
            f"font=Arial:fontfile=/Windows/Fonts/arialbd.ttf,"
            f"drawtext=text='{s['sub']}':"
            f"fontsize=30:fontcolor=0x00d4aa:x=(w-text_w)/2:y=h-250:"
            f"font=Arial:fontfile=/Windows/Fonts/arial.ttf"
            f"[out]",
            "-map", "[out]", "-map", "2:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-t", f"{s['total']:.3f}",
            clip_path
        ]
    else:
        # Hook: text-only on dark gradient
        # Escape single quotes for ffmpeg drawtext
        hook_text = s["text"].replace("\\n", chr(10))
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=0x0a1628:s=1080x1920:d={s['total']:.3f}:r=30",
            "-i", vo_path,
            "-filter_complex",
            f"[0:v]drawtext=text='{hook_text}':"
            f"fontsize=72:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:"
            f"font=Arial:fontfile=/Windows/Fonts/arialbd.ttf:line_spacing=20"
            f"[out]",
            "-map", "[out]", "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-t", f"{s['total']:.3f}",
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

out_path = os.path.join(OUT_DIR, "video28-electric-gokarts-segway-razor.mp4")
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

result = subprocess.run(concat_cmd, capture_output=True, text=True, timeout=300)
if result.returncode == 0:
    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print(f"\n✅ RENDER COMPLETE!")
    print(f"File: {out_path}")
    print(f"Size: {size_mb:.1f} MB")
    print(f"Duration: ~{total_dur:.0f}s")
else:
    print(f"\nConcatenation FAILED: {result.stderr[-500:]}")

# Cleanup temp
# shutil.rmtree(TEMP_DIR)  # Uncomment after verifying
print("\nDone. Temp files kept at:", TEMP_DIR)
