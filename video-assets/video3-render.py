import json
import requests
import os
import sys

API_KEY = os.environ.get("SHOTSTACK_PROD_KEY", "GWoBAU0VdD6QvV3nWLlZyQKzHiU7L3FFaTAOBufc")
API_URL = "https://api.shotstack.io/edit/v1/render"

VO_BASE = "https://raw.githubusercontent.com/Jwatenterprises/S.E.T-US-sunenergytechnology.github.io/main/video-assets/video3-voiceover"
LOGO_URL = "https://raw.githubusercontent.com/Jwatenterprises/S.E.T-US-sunenergytechnology.github.io/main/set-logo.jpg"

BROLL = {
    "apartment": "https://videos.pexels.com/video-files/13761469/13761469-uhd_2560_1440_30fps.mp4",
    "candle":    "https://videos.pexels.com/video-files/855262/855262-hd_1920_1080_25fps.mp4",
    "solar":     "https://videos.pexels.com/video-files/5233552/5233552-uhd_2560_1440_30fps.mp4",
    "laptop":    "https://videos.pexels.com/video-files/5725445/5725445-uhd_2560_1440_25fps.mp4",
    "money":     "https://videos.pexels.com/video-files/6266251/6266251-uhd_1440_2560_25fps.mp4",
}
AC200L_IMG = "https://cdn.shopify.com/s/files/1/0536/3390/8911/files/AC200L_9783dcdd-db2a-4939-8ce5-7134f35d43a4.png?v=1758766225"

shots = [
    {"vo": "line1.mp3", "dur": 5.21, "pad": 0.29, "broll": "apartment", "trim": 2,
     "text": "Living in an apartment?",  "sub": "You can't install rooftop solar."},
    {"vo": "line2.mp3", "dur": 2.86, "pad": 0.34, "broll": "candle", "trim": 0,
     "text": "But you CAN own",          "sub": "a solar generator."},
    {"vo": "line3.mp3", "dur": 6.41, "pad": 0.29, "broll": None, "trim": 0,
     "text": "BLUETTI AC200L",            "sub": "2,048Wh — fits under your desk"},
    {"vo": "line4.mp3", "dur": 4.82, "pad": 0.28, "broll": "solar", "trim": 3,
     "text": "Charge from a balcony",     "sub": "or plug into the wall overnight"},
    {"vo": "line5.mp3", "dur": 4.66, "pad": 0.34, "broll": "laptop", "trim": 1,
     "text": "Fridge · Laptop · Phone · Fan", "sub": "All running during a blackout"},
    {"vo": "line6.mp3", "dur": 6.05, "pad": 0.25, "broll": "money", "trim": 0,
     "text": "No gas. No fumes.",         "sub": "No landlord permission needed."},
    {"vo": "line7.mp3", "dur": 5.06, "pad": 0.24, "broll": None, "trim": 0,
     "text": "Under $2,000",              "sub": "Apartment-proof backup power"},
    {"vo": "line8.mp3", "dur": 5.04, "pad": 0.36, "broll": None, "trim": 0,
     "text": "S.E.T. Solar",              "sub": "Find your perfect generator in 5 minutes"},
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
    length = s["dur"] + s["pad"]

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
            "transition": {"in": "fade"},
        })
    elif i == 2:
        video_clips.append({
            "asset": {
                "type": "image",
                "src": AC200L_IMG,
            },
            "start": t,
            "length": length,
            "fit": "contain",
            "effect": "zoomInSlow",
            "transition": {"in": "fade"},
        })
    elif i == 6:
        video_clips.append({
            "asset": {
                "type": "html",
                "html": """<div style="display:flex;align-items:center;justify-content:center;
                    width:100%;height:100%;background:linear-gradient(135deg,#0a1628 0%,#1a2a4a 50%,#0d1f3c 100%);">
                    <div style="text-align:center;">
                    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:90px;
                    font-weight:900;color:#00d4aa;margin:0;">UNDER $2,000</p>
                    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:36px;
                    font-weight:400;color:#ffffff;margin:20px 0 0 0;">Apartment-proof backup power</p>
                    </div></div>""",
                "width": 1080,
                "height": 1920,
            },
            "start": t,
            "length": length,
        })
    elif i == 7:
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
    },
}

print(f"Total duration: {t:.1f}s")
print(f"Shots: {len(shots)}")
print(f"Text clips: {len(text_clips)}")
print(f"Video clips: {len(video_clips)}")
print(f"Audio clips: {len(audio_clips)}")

json_path = os.path.join(os.path.dirname(__file__), "video3-shotstack-render.json")
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
    print(f"Check status: curl -s -H 'x-api-key: {API_KEY}' {API_URL}/{render_id}")
