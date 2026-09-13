"""
S.E.T. Store — Electric Go-Kart Promo Video (Video #28)
Segway GoKart Pro 2 + Razor Crazy Cart XL + Ground Force Elite + Ground Force One
Real product images, AriaNeural voiceover, Shotstack render
"""
import json
import requests
import os
import sys
import time

API_KEY = os.environ.get("SHOTSTACK_PROD_KEY", "GWoBAU0VdD6QvV3nWLlZyQKzHiU7L3FFaTAOBufc")
API_URL = "https://api.shotstack.io/edit/v1/render"

VO_BASE = "https://raw.githubusercontent.com/Jwatenterprises/S.E.T-US-sunenergytechnology.github.io/main/video-assets/gokart-voiceover"
LOGO_URL = "https://raw.githubusercontent.com/Jwatenterprises/S.E.T-US-sunenergytechnology.github.io/main/set-logo.jpg"

# Real product images (verified URLs from manufacturer sites)
IMAGES = {
    "segway_pro2": "https://images.techeblog.com/wp-content/uploads/2025/07/23133944/segway-gokart-pro-2.jpg",
    "razor_crazy_xl": "https://razor.com/wp-content/uploads/2025/04/Crazy_Cart_XL_Product_photo_001.jpg",
    "razor_gf_elite": "https://razor.com/wp-content/uploads/2025/04/GroundForceElite_Product_001.png",
    "razor_gf_one": "https://razor.com/wp-content/uploads/2025/04/GroundForce_SL_Product.png",
    # Lifestyle shots for B-roll
    "razor_crazy_xl_life": "https://razor.com/wp-content/uploads/2025/04/Crazy_Cart_XL_Lifestyle_002.jpg",
    "razor_gf_elite_life": "https://razor.com/wp-content/uploads/2025/04/GroundForceElite_Lifestyle_0264.jpg",
    "razor_gf_one_life": "https://razor.com/wp-content/uploads/2025/04/GroundForce_Lifestyle_0069.jpg",
}

# Voiceover durations (from ffprobe)
PAD = 0.5

shots = [
    {
        "vo": "line1.mp3", "dur": 4.25,
        "type": "hook", "src": None,
        "text": "Electric Go-Karts Are Here ⚡🏎️",
        "sub": "",
    },
    {
        "vo": "line2.mp3", "dur": 13.49,
        "type": "product", "src": "segway_pro2",
        "text": "Segway GoKart Pro 2",
        "sub": "$1,499 · 26.7 MPH · 4,800W Dual Motors",
    },
    {
        "vo": "line3.mp3", "dur": 14.42,
        "type": "product", "src": "razor_crazy_xl",
        "text": "Razor Crazy Cart XL",
        "sub": "$1,259 · 14 MPH · Drift System · Adults",
    },
    {
        "vo": "line4.mp3", "dur": 12.94,
        "type": "product", "src": "razor_gf_elite",
        "text": "Razor Ground Force Elite",
        "sub": "$549 · 14 MPH · 36V · Ages 13+",
    },
    {
        "vo": "line5.mp3", "dur": 11.40,
        "type": "product", "src": "razor_gf_one",
        "text": "Razor Ground Force One",
        "sub": "$299 · 12 MPH · 40 Min · Ages 8+",
    },
    {
        "vo": "line6.mp3", "dur": 4.80,
        "type": "endcard", "src": None,
        "text": "S.E.T. Solar",
        "sub": "Link in bio ↓",
    },
]

# --- Brand colors ---
BG_DARK = "#0a0f1a"
BG_GRAD_START = "#0d1826"
BG_GRAD_END = "#0a1628"
ACCENT_GREEN = "#00d4aa"
ACCENT_ORANGE = "#ff6b35"
TEXT_WHITE = "#ffffff"
TEXT_LIGHT = "#e0e0e0"


def html_text(main, sub, size_main=52, size_sub=28):
    sub_html = f'<p style="font-family:Arial,sans-serif;font-size:{size_sub}px;font-weight:500;color:{ACCENT_GREEN};text-shadow:1px 1px 6px rgba(0,0,0,0.9);margin:8px 0 0 0;line-height:1.3;letter-spacing:0.5px;">{sub}</p>' if sub else ""
    return f"""<div style="display:flex;flex-direction:column;align-items:center;justify-content:flex-end;
        width:100%;height:100%;text-align:center;padding:0 40px 80px 40px;">
        <p style="font-family:Arial,sans-serif;font-size:{size_main}px;
        font-weight:900;color:{TEXT_WHITE};text-shadow:2px 2px 10px rgba(0,0,0,0.95);
        margin:0;line-height:1.15;letter-spacing:-0.5px;">{main}</p>
        {sub_html}</div>"""


def html_hook(text):
    return f"""<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
        width:100%;height:100%;text-align:center;
        background:linear-gradient(180deg,{BG_GRAD_START} 0%,{BG_GRAD_END} 100%);">
        <p style="font-family:Arial,sans-serif;font-size:64px;
        font-weight:900;color:{TEXT_WHITE};margin:0;line-height:1.15;
        text-shadow:2px 3px 12px rgba(0,0,0,0.8);">{text}</p>
        <div style="width:80px;height:4px;background:{ACCENT_ORANGE};margin:20px auto 0;border-radius:2px;"></div>
        </div>"""


def html_endcard():
    return f"""<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
        width:100%;height:100%;background:linear-gradient(180deg,{BG_GRAD_START} 0%,#1a3a5c 100%);">
        <img src="{LOGO_URL}" style="width:300px;height:auto;margin-bottom:24px;border-radius:16px;" />
        <p style="font-family:Arial,sans-serif;font-size:42px;
        font-weight:700;color:{TEXT_WHITE};margin:0;">S.E.T. Solar</p>
        <p style="font-family:Arial,sans-serif;font-size:26px;
        font-weight:400;color:{ACCENT_GREEN};margin:14px 0 0 0;">Full guide + buying links ↓</p>
        <p style="font-family:Arial,sans-serif;font-size:20px;
        font-weight:400;color:{TEXT_LIGHT};margin:10px 0 0 0;">sunenergytechnology.com</p>
        </div>"""


# --- Build timeline ---
text_clips = []
video_clips = []
audio_clips = []

t = 0.0
for i, s in enumerate(shots):
    length = s["dur"] + PAD

    # Text overlay (bottom)
    text_clips.append({
        "asset": {
            "type": "html",
            "html": html_text(s["text"], s["sub"]),
            "width": 1080,
            "height": 500,
        },
        "start": t,
        "length": length,
        "position": "bottom",
        "offset": {"y": 0.02},
        "transition": {"in": "fade", "out": "fade"},
    })

    # Background / product / hook
    if s["type"] == "hook":
        # Animated HTML hook — no external video needed
        video_clips.append({
            "asset": {
                "type": "html",
                "html": html_hook(s["text"]),
                "width": 1080,
                "height": 1920,
            },
            "start": t,
            "length": length,
            "transition": {"in": "fade", "out": "fade"},
        })
    elif s["type"] == "product":
        # Dark gradient background
        video_clips.append({
            "asset": {
                "type": "html",
                "html": f'<div style="width:100%;height:100%;background:linear-gradient(180deg,{BG_GRAD_START},#111828);"></div>',
                "width": 1080,
                "height": 1920,
            },
            "start": t,
            "length": length,
            "transition": {"in": "fade", "out": "fade"},
        })
        # Product image overlay (centered, upper portion)
        text_clips.append({
            "asset": {
                "type": "html",
                "html": f'<div style="display:flex;align-items:center;justify-content:center;width:100%;height:100%;padding:40px;"><img src="{IMAGES[s["src"]]}" style="max-width:90%;max-height:85%;object-fit:contain;filter:drop-shadow(0 8px 24px rgba(0,0,0,0.6));"/></div>',
                "width": 1080,
                "height": 1100,
            },
            "start": t,
            "length": length,
            "position": "top",
            "offset": {"y": 0.04},
            "effect": "zoomInSlow",
            "transition": {"in": "fade", "out": "fade"},
        })
    elif s["type"] == "endcard":
        video_clips.append({
            "asset": {
                "type": "html",
                "html": html_endcard(),
                "width": 1080,
                "height": 1920,
            },
            "start": t,
            "length": length,
            "transition": {"in": "fade", "out": "fade"},
        })

    # Voiceover audio
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

# --- Render config ---
render_config = {
    "timeline": {
        "background": BG_DARK,
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

json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gokart-shotstack-render.json")
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
    for attempt in range(90):
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

                print("\nDownloading to OneDrive exports folder...")
                dl = requests.get(dl_url, stream=True, timeout=120)
                out_dir = os.path.expanduser("~/OneDrive/video-assets/exports")
                os.makedirs(out_dir, exist_ok=True)
                out_path = os.path.join(out_dir, "video28-electric-gokarts-segway-razor.mp4")
                with open(out_path, "wb") as vf:
                    for chunk in dl.iter_content(chunk_size=8192):
                        vf.write(chunk)
                print(f"Saved to: {out_path}")
                print(f"Size: {os.path.getsize(out_path) / 1024 / 1024:.1f} MB")
                break
            elif state == "failed":
                print(f"\nRENDER FAILED!")
                print(json.dumps(data, indent=2))
                break
        else:
            print(f"  [{attempt*10}s] Check failed: {check.status_code}")
    else:
        print("\nTimed out waiting for render (15 minutes)")
else:
    print("\nRender submission failed!")
