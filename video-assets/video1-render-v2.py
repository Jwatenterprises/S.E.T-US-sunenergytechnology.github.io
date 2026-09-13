import json
import requests
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = os.environ.get("SHOTSTACK_PROD_KEY", "GWoBAU0VdD6QvV3nWLlZyQKzHiU7L3FFaTAOBufc")
API_URL = "https://api.shotstack.io/edit/v1/render"

VO_BASE = "https://raw.githubusercontent.com/Jwatenterprises/S.E.T-US-sunenergytechnology.github.io/main/voiceover"
LOGO_URL = "https://raw.githubusercontent.com/Jwatenterprises/S.E.T-US-sunenergytechnology.github.io/main/set-logo.jpg"

BROLL = {
    "house":     "https://videos.pexels.com/video-files/3773486/3773486-hd_1920_1080_30fps.mp4",
    "storm":     "https://videos.pexels.com/video-files/3163534/3163534-hd_1920_1080_30fps.mp4",
    "solar":     "https://videos.pexels.com/video-files/5233552/5233552-uhd_2560_1440_30fps.mp4",
    "candle":    "https://videos.pexels.com/video-files/3571264/3571264-hd_1920_1080_30fps.mp4",
    "device":    "https://videos.pexels.com/video-files/4065388/4065388-hd_1920_1080_30fps.mp4",
    "nature":    "https://videos.pexels.com/video-files/3129671/3129671-hd_1920_1080_30fps.mp4",
}

AC300_IMG = "https://raw.githubusercontent.com/Jwatenterprises/S.E.T-US-sunenergytechnology.github.io/main/images/bluetti-ac300.png"

PAD = 0.5

# Voiceover durations measured from mp3 files:
# line1: 2.57s — Hook: "Can a solar generator power your whole house?"
# line2: 7.87s — Problem: blackout scenario, grid goes down
# line3: 6.60s — Product intro: BLUETTI AC300 + B300, 3,072Wh LiFePO4
# line4: 2.16s — Key stat: 3,000W pure sine wave
# line5: 8.11s — What it runs: fridge, lights, router, medical devices, 24+ hours
# line6: 8.83s — Differentiator: modular, expand to 12,288Wh, UPS mode
# line7: 4.66s — Honest answer: what it can't do (AC, water heater)
# line8: 2.81s — CTA: S.E.T. Solar, link in bio

shots = [
    {"vo": "line1.mp3", "dur": 2.57, "broll": "house", "trim": 0,
     "text": "Can a solar generator",     "sub": "power your WHOLE house?"},
    {"vo": "line2.mp3", "dur": 7.87, "broll": "storm", "trim": 2,
     "text": "When the grid goes down",   "sub": "your family is in the dark."},
    {"vo": "line3.mp3", "dur": 6.60, "broll": None, "trim": 0,
     "text": "BLUETTI AC300 + B300",       "sub": "3,072Wh of LiFePO4 power"},
    {"vo": "line4.mp3", "dur": 2.16, "broll": None, "trim": 0,
     "text": "3,000W Pure Sine Wave",     "sub": "6,000W surge capacity"},
    {"vo": "line5.mp3", "dur": 8.11, "broll": "device", "trim": 0,
     "text": "Fridge · Lights · Router",  "sub": "Medical devices — 24+ hours"},
    {"vo": "line6.mp3", "dur": 8.83, "broll": "solar", "trim": 3,
     "text": "Modular & expandable",      "sub": "Up to 12,288Wh · UPS mode"},
    {"vo": "line7.mp3", "dur": 4.66, "broll": "nature", "trim": 0,
     "text": "The honest answer",         "sub": "What it can — and can't — do"},
    {"vo": "line8.mp3", "dur": 2.81, "broll": None, "trim": 0,
     "text": "S.E.T. Solar",              "sub": "Find your perfect generator"},
]

def html_text(main, sub, size_main=54, size_sub=32):
    return f"""<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
        width:100%;height:100%;text-align:center;padding:40px;">
        <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:{size_main}px;
        font-weight:800;color:#ffffff;text-shadow:2px 2px 8px rgba(0,0,0,0.9);
        margin:0 0 12px 0;line-height:1.2;">{main}</p>
        <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:{size_sub}px;
        font-weight:400;color:#f0f0f0;text-shadow:1px 1px 6px rgba(0,0,0,0.8);
        margin:0;line-height:1.3;">{sub}</p></div>"""

text_clips = []
video_clips = []
audio_clips = []

t = 0.0
for i, s in enumerate(shots):
    length = s["dur"] + PAD

    text_clips.append({
        "asset": {
            "type": "html",
            "html": html_text(s["text"], s["sub"]),
            "width": 1080,
            "height": 400,
        },
        "start": t,
        "length": length,
        "position": "bottom",
        "offset": {"y": -0.08},
        "transition": {"in": "fade", "out": "fade"},
    })

    if s["broll"]:
        video_clips.append({
            "asset": {
                "type": "video",
                "src": BROLL[s["broll"]],
                "trim": s["trim"],
                "volume": 0,
            },
            "start": t,
            "length": length,
            "fit": "crop",
            "transition": {"in": "fade", "out": "fade"},
        })
    elif i == 2:
        # AC300 product shot
        video_clips.append({
            "asset": {
                "type": "image",
                "src": AC300_IMG,
            },
            "start": t,
            "length": length,
            "fit": "contain",
            "effect": "zoomInSlow",
            "transition": {"in": "fade", "out": "fade"},
        })
    elif i == 3:
        # Power stats card
        video_clips.append({
            "asset": {
                "type": "html",
                "html": """<div style="display:flex;align-items:center;justify-content:center;
                    width:100%;height:100%;background:linear-gradient(135deg,#0a1628 0%,#1a2a4a 50%,#0d1f3c 100%);">
                    <div style="text-align:center;">
                    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:80px;
                    font-weight:900;color:#00d4aa;margin:0;">3,000W</p>
                    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:36px;
                    font-weight:400;color:#ffffff;margin:16px 0 0 0;">Pure Sine Wave Inverter</p>
                    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:28px;
                    font-weight:300;color:#88bbff;margin:12px 0 0 0;">6,000W Surge Capacity</p>
                    </div></div>""",
                "width": 1080,
                "height": 1920,
            },
            "start": t,
            "length": length,
            "transition": {"in": "fade", "out": "fade"},
        })
    elif i == 7:
        # CTA / logo card
        video_clips.append({
            "asset": {
                "type": "html",
                "html": f"""<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                    width:100%;height:100%;background:linear-gradient(180deg,#0d1f3c 0%,#1a3a5c 100%);">
                    <img src="{LOGO_URL}" style="width:320px;height:auto;margin-bottom:30px;border-radius:16px;" />
                    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:44px;
                    font-weight:700;color:#ffffff;margin:0;">S.E.T. Solar</p>
                    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:28px;
                    font-weight:400;color:#00d4aa;margin:16px 0 0 0;">Link in bio ↓</p>
                    </div>""",
                "width": 1080,
                "height": 1920,
            },
            "start": t,
            "length": length,
            "transition": {"in": "fade", "out": "fade"},
        })

    audio_clips.append({
        "asset": {
            "type": "audio",
            "src": f"{VO_BASE}/line{i+1}.mp3",
            "volume": 1,
        },
        "start": t,
        "length": s["dur"],
    })

    t += length

render_config = {
    "timeline": {
        "background": "#000000",
        "tracks": [
            {"clips": text_clips},
            {"clips": video_clips},
            {"clips": audio_clips},
        ],
    },
    "output": {
        "format": "mp4",
        "resolution": "hd",
        "size": {"width": 1080, "height": 1920},
        "fps": 30,
        "quality": "high",
    },
}

print(f"Total duration: {t:.1f}s")
print(f"Shots: {len(shots)}")
print(f"Text clips: {len(text_clips)}")
print(f"Video clips: {len(video_clips)}")
print(f"Audio clips: {len(audio_clips)}")

json_path = os.path.join(os.path.dirname(__file__), "video1-shotstack-render-v2.json")
with open(json_path, "w") as f:
    json.dump(render_config, f, indent=2)
print(f"\nRender JSON saved to: {json_path}")

print("\nSubmitting to Shotstack Production API...")
resp = requests.post(
    API_URL,
    headers={
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
    },
    json=render_config,
    timeout=30,
)

print(f"Status: {resp.status_code}")
result = resp.json()
print(json.dumps(result, indent=2))

if resp.status_code == 201:
    render_id = result.get("response", {}).get("id", "unknown")
    print(f"\nRender ID: {render_id}")
    print(f"\nPolling for completion...")

    status_url = f"{API_URL}/{render_id}"
    for attempt in range(60):
        time.sleep(10)
        check = requests.get(status_url, headers={"x-api-key": API_KEY}, timeout=15)
        if check.status_code == 200:
            data = check.json()
            state = data.get("response", {}).get("status", "unknown")
            print(f"  [{attempt*10}s] Status: {state}")
            if state == "done":
                dl_url = data["response"]["url"]
                print(f"\nRENDER COMPLETE!")
                print(f"Download URL: {dl_url}")

                print("\nDownloading to exports folder...")
                dl = requests.get(dl_url, stream=True, timeout=120)
                out_path = os.path.join(os.path.dirname(__file__), "exports", "video1-ac300-whole-house-v2.mp4")
                with open(out_path, "wb") as vf:
                    for chunk in dl.iter_content(chunk_size=8192):
                        vf.write(chunk)
                print(f"Saved to: {out_path}")
                print(f"Size: {os.path.getsize(out_path) / 1024 / 1024:.1f} MB")

                # Copy to OneDrive
                onedrive_path = os.path.expanduser("~/OneDrive/video-assets/exports/video1-ac300-whole-house-v2.mp4")
                import shutil
                shutil.copy2(out_path, onedrive_path)
                print(f"Copied to OneDrive: {onedrive_path}")
                break
            elif state == "failed":
                print(f"\nRENDER FAILED!")
                print(json.dumps(data, indent=2))
                break
        else:
            print(f"  [{attempt*10}s] Check failed: {check.status_code}")
    else:
        print("\nTimed out waiting for render (10 minutes)")
