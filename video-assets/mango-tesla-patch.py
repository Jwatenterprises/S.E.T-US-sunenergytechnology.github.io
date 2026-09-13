"""
Patch: Re-render Scene 2 with rooftop solar panel image, then re-concatenate.
Adds solar panel B-roll at ~0:05 mark in the video.
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

FONT_BOLD = "/Windows/Fonts/arialbd.ttf"
FONT_REG = "/Windows/Fonts/arial.ttf"

def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True
    )
    return float(r.stdout.strip())

# --- Re-render Scene 2 with rooftop solar image ---
vo_path = os.path.join(VO_DIR, "line2.mp3")
solar_img = os.path.join(IMG_DIR, "rooftop-solar-panels.jpg")
clip_path = os.path.join(TEMP_DIR, "shot01.mp4")  # overwrite existing shot01

dur = get_duration(vo_path)
total = dur + 0.5
print(f"Scene 2 VO: {dur:.2f}s, total: {total:.2f}s")

# Build filter: solar image for first 3.5s with fade, then text card for rest
filter_complex = (
    f"[1:v]scale=1080:-1:force_original_aspect_ratio=decrease,"
    f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x0f1825,"
    f"format=yuva420p,"
    f"fade=in:st=0:d=0.4:alpha=1,"
    f"fade=out:st=3.0:d=0.5:alpha=1[solar];"
    f"[0:v][solar]overlay=0:0:enable='between(t\\,0\\,3.5)'[bg];"
    f"[bg]drawtext=text='YOUR SOLAR PANELS':"
    f"fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-400:"
    f"fontfile={FONT_BOLD}:enable='between(t\\,0\\,3.5)',"
    f"drawtext=text='shut off during outages':"
    f"fontsize=36:fontcolor=0xfc8181:x=(w-text_w)/2:y=h-340:"
    f"fontfile={FONT_REG}:enable='between(t\\,0\\,3.5)',"
    f"drawtext=text='NO BATTERY = NO BACKUP':"
    f"fontsize=56:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-40:"
    f"fontfile={FONT_BOLD}:enable='gte(t\\,3.5)',"
    f"drawtext=text='Solar panels shut off during outages':"
    f"fontsize=28:fontcolor=0x00d4aa:x=(w-text_w)/2:y=(h/2)+40:"
    f"fontfile={FONT_REG}:enable='gte(t\\,3.5)'"
    f"[out]"
)

cmd = [
    "ffmpeg", "-y",
    "-f", "lavfi", "-i", f"color=c=0x0f1825:s=1080x1920:d={total:.3f}:r=30",
    "-i", solar_img,
    "-i", vo_path,
    "-filter_complex", filter_complex,
    "-map", "[out]", "-map", "2:a",
    "-c:v", "libx264", "-preset", "fast", "-crf", "20",
    "-c:a", "aac", "-b:a", "128k",
    "-pix_fmt", "yuv420p",
    "-t", f"{total:.3f}",
    clip_path
]

print("Rendering Scene 2 with solar panel image...")
result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
if result.returncode != 0:
    print(f"FAILED: {result.stderr[-800:]}")
    exit(1)
else:
    size_mb = os.path.getsize(clip_path) / 1024 / 1024
    print(f"OK — shot01.mp4: {size_mb:.1f} MB")

# --- Re-concatenate all 7 shots ---
print("\nRe-concatenating all 7 shots...")
clip_files = [os.path.join(TEMP_DIR, f"shot{i:02d}.mp4") for i in range(7)]

# Verify all exist
for c in clip_files:
    if not os.path.exists(c):
        print(f"MISSING: {c}")
        exit(1)
    d = get_duration(c)
    print(f"  {os.path.basename(c)}: {d:.2f}s")

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
    total_dur = get_duration(out_path)
    print(f"\n✅ DONE: {out_path}")
    print(f"   Size: {size_mb:.1f} MB")
    print(f"   Duration: {total_dur:.1f}s")

    # Copy to local exports
    local_out = os.path.join(os.path.dirname(BASE), "video-assets", "exports", "tiktok-mango-vs-tesla-powerwall.mp4")
    shutil.copy2(out_path, local_out)
    print(f"   Local copy: {local_out}")
