"""
Patch v2: Split Scene 2 into two clips — solar image first, then text card.
Simple approach: no alpha compositing, just two clean clips concatenated.
"""
import os
import subprocess
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
VO_DIR = os.path.join(BASE, "mango-tesla-vo")
IMG_DIR = os.path.join(os.path.dirname(BASE), "images", "mango-power")
TEMP_DIR = os.path.join(BASE, "mango-tesla-temp")
OUT_DIR = os.path.expanduser("~/OneDrive/video-assets/exports")

FONT_BOLD = "/Windows/Fonts/arialbd.ttf"
FONT_REG = "/Windows/Fonts/arial.ttf"

def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True
    )
    return float(r.stdout.strip())

solar_img = os.path.join(IMG_DIR, "rooftop-solar-panels.jpg")
vo_path = os.path.join(VO_DIR, "line2.mp3")
vo_dur = get_duration(vo_path)
total_dur = vo_dur + 0.5

# Split: 3.5s solar image, rest is text card
SOLAR_DUR = 3.5
TEXT_DUR = total_dur - SOLAR_DUR

print(f"Scene 2: {total_dur:.2f}s total — {SOLAR_DUR}s solar image + {TEXT_DUR:.2f}s text card")

# --- Part A: Solar panel image fills the frame with text overlay ---
part_a = os.path.join(TEMP_DIR, "shot01a.mp4")

# Scale image to fill 1080x1920 vertical (crop center)
cmd_a = [
    "ffmpeg", "-y",
    "-loop", "1", "-t", f"{SOLAR_DUR}",
    "-i", solar_img,
    "-f", "lavfi", "-t", f"{SOLAR_DUR}",
    "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
    "-filter_complex",
    f"[0:v]scale=-1:1920,crop=1080:1920:(iw-1080)/2:0,format=yuv420p,"
    f"drawtext=text='YOUR SOLAR PANELS':"
    f"fontsize=52:fontcolor=white:x=(w-text_w)/2:y=h-380:"
    f"fontfile={FONT_BOLD}:shadowcolor=black:shadowx=2:shadowy=2,"
    f"drawtext=text='shut off during outages':"
    f"fontsize=36:fontcolor=0xfc8181:x=(w-text_w)/2:y=h-310:"
    f"fontfile={FONT_REG}:shadowcolor=black:shadowx=2:shadowy=2"
    f"[out]",
    "-map", "[out]", "-map", "1:a",
    "-c:v", "libx264", "-preset", "fast", "-crf", "20",
    "-c:a", "aac", "-b:a", "128k", "-ar", "24000", "-ac", "1",
    "-r", "30",
    "-pix_fmt", "yuv420p",
    part_a
]

print("Rendering Part A (solar panel image)...")
result = subprocess.run(cmd_a, capture_output=True, text=True, timeout=60)
if result.returncode != 0:
    print(f"PART A FAILED:\n{result.stderr[-800:]}")
    exit(1)
print(f"  OK — {os.path.getsize(part_a)/1024/1024:.1f} MB")

# --- Part B: Text card "NO BATTERY = NO BACKUP" ---
part_b = os.path.join(TEMP_DIR, "shot01b.mp4")

cmd_b = [
    "ffmpeg", "-y",
    "-f", "lavfi", "-i", f"color=c=0x0f1825:s=1080x1920:d={TEXT_DUR:.3f}:r=30",
    "-f", "lavfi", "-t", f"{TEXT_DUR:.3f}",
    "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
    "-filter_complex",
    f"[0:v]drawtext=text='NO BATTERY = NO BACKUP':"
    f"fontsize=56:fontcolor=white:x=(w-text_w)/2:y=(h/2)-40:"
    f"fontfile={FONT_BOLD},"
    f"drawtext=text='Solar panels shut off during outages':"
    f"fontsize=28:fontcolor=0x00d4aa:x=(w-text_w)/2:y=(h/2)+40:"
    f"fontfile={FONT_REG}"
    f"[out]",
    "-map", "[out]", "-map", "1:a",
    "-c:v", "libx264", "-preset", "fast", "-crf", "20",
    "-c:a", "aac", "-b:a", "128k", "-ar", "24000", "-ac", "1",
    "-pix_fmt", "yuv420p",
    part_b
]

print("Rendering Part B (text card)...")
result = subprocess.run(cmd_b, capture_output=True, text=True, timeout=60)
if result.returncode != 0:
    print(f"PART B FAILED:\n{result.stderr[-800:]}")
    exit(1)
print(f"  OK — {os.path.getsize(part_b)/1024/1024:.1f} MB")

# --- Merge A + B with the voiceover ---
shot01_final = os.path.join(TEMP_DIR, "shot01.mp4")

# Concat video parts, then replace audio with the actual VO
concat_tmp = os.path.join(TEMP_DIR, "concat_scene2.txt")
with open(concat_tmp, "w") as f:
    f.write(f"file '{part_a}'\n")
    f.write(f"file '{part_b}'\n")

merged_tmp = os.path.join(TEMP_DIR, "shot01_merged.mp4")
cmd_merge = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", concat_tmp,
    "-c:v", "libx264", "-preset", "fast", "-crf", "20",
    "-c:a", "aac", "-b:a", "128k",
    "-pix_fmt", "yuv420p",
    merged_tmp
]
print("Merging A + B...")
result = subprocess.run(cmd_merge, capture_output=True, text=True, timeout=60)
if result.returncode != 0:
    print(f"MERGE FAILED:\n{result.stderr[-500:]}")
    exit(1)

# Replace the silent audio with the real voiceover
cmd_audio = [
    "ffmpeg", "-y",
    "-i", merged_tmp,
    "-i", vo_path,
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "128k",
    "-map", "0:v", "-map", "1:a",
    "-shortest",
    shot01_final
]
print("Adding voiceover...")
result = subprocess.run(cmd_audio, capture_output=True, text=True, timeout=60)
if result.returncode != 0:
    print(f"AUDIO FAILED:\n{result.stderr[-500:]}")
    exit(1)

final_dur = get_duration(shot01_final)
print(f"  OK — shot01.mp4: {os.path.getsize(shot01_final)/1024/1024:.1f} MB, {final_dur:.2f}s")

# --- Screenshot at t=1.5s to verify solar image is visible ---
debug_path = os.path.join(TEMP_DIR, "debug-frame-solar.jpg")
subprocess.run([
    "ffmpeg", "-y", "-ss", "1.5", "-i", shot01_final,
    "-frames:v", "1", "-q:v", "2", debug_path
], capture_output=True, timeout=30)
print(f"  Debug frame: {debug_path}")

# --- Re-concatenate all 7 shots into final video ---
print("\nRe-concatenating all 7 shots...")
clip_files = [os.path.join(TEMP_DIR, f"shot{i:02d}.mp4") for i in range(7)]

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

    local_out = os.path.join(os.path.dirname(BASE), "video-assets", "exports", "tiktok-mango-vs-tesla-powerwall.mp4")
    shutil.copy2(out_path, local_out)
    print(f"   Local copy: {local_out}")
