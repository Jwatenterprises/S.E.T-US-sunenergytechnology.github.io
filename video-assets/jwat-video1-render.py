import json
import requests
import os
import sys
import time
import shutil

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = os.environ.get("SHOTSTACK_PROD_KEY", "GWoBAU0VdD6QvV3nWLlZyQKzHiU7L3FFaTAOBufc")
API_URL = "https://api.shotstack.io/edit/v1/render"

BROLL = {
    "dark":   "https://videos.pexels.com/video-files/3571264/3571264-hd_1920_1080_30fps.mp4",
    "street": "https://videos.pexels.com/video-files/3773486/3773486-hd_1920_1080_30fps.mp4",
    "tech":   "https://videos.pexels.com/video-files/4065388/4065388-hd_1920_1080_30fps.mp4",
    "laptop": "https://videos.pexels.com/video-files/5752729/5752729-hd_1920_1080_30fps.mp4",
}

PAD = 0.5

# JWAT brand colors
NAVY = "#1a365d"
GOLD = "#ffd700"
DARK_BG = "#0d1b2a"

shots = [
    {
        "dur": 5.0, "broll": "dark", "trim": 0,
        "text": "Your phone rings at 8 PM.",
        "sub": "You're off the clock.",
    },
    {
        "dur": 5.0, "broll": "street", "trim": 2,
        "text": "You miss it.",
        "sub": "They call your competitor.",
    },
    {
        "dur": 5.0, "broll": None, "trim": 0,
        "text": "63%",
        "sub": "of missed calls NEVER call back",
        "card": "stat",
    },
    {
        "dur": 5.0, "broll": "tech", "trim": 0,
        "text": "What if AI answered",
        "sub": "every single call?",
    },
    {
        "dur": 5.0, "broll": None, "trim": 0,
        "text": "",
        "sub": "",
        "card": "features",
    },
    {
        "dur": 4.0, "broll": None, "trim": 0,
        "text": "",
        "sub": "",
        "card": "cost",
    },
    {
        "dur": 4.0, "broll": None, "trim": 0,
        "text": "",
        "sub": "",
        "card": "cta",
    },
]

def text_overlay(main, sub, size_main=54, size_sub=32):
    return f"""<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
        width:100%;height:100%;text-align:center;padding:40px;">
        <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:{size_main}px;
        font-weight:800;color:#ffffff;text-shadow:2px 2px 8px rgba(0,0,0,0.9);
        margin:0 0 12px 0;line-height:1.2;">{main}</p>
        <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:{size_sub}px;
        font-weight:400;color:#f0f0f0;text-shadow:1px 1px 6px rgba(0,0,0,0.8);
        margin:0;line-height:1.3;">{sub}</p></div>"""

STAT_CARD = f"""<div style="display:flex;align-items:center;justify-content:center;
    width:100%;height:100%;background:linear-gradient(135deg,{DARK_BG} 0%,{NAVY} 100%);">
    <div style="text-align:center;padding:40px;">
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:120px;
    font-weight:900;color:{GOLD};margin:0;line-height:1;">63%</p>
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:32px;
    font-weight:400;color:#ffffff;margin:20px 0 0 0;line-height:1.3;">of missed calls</p>
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:36px;
    font-weight:700;color:#ff6b6b;margin:8px 0 0 0;">NEVER call back</p>
    </div></div>"""

FEATURES_CARD = f"""<div style="display:flex;align-items:center;justify-content:center;
    width:100%;height:100%;background:linear-gradient(180deg,{DARK_BG} 0%,{NAVY} 100%);">
    <div style="text-align:center;padding:40px;">
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:42px;
    font-weight:800;color:#ffffff;margin:0 0 32px 0;">AI Phone Answering</p>
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:32px;
    font-weight:400;color:{GOLD};margin:0 0 16px 0;">&#x2713; Sounds Human</p>
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:32px;
    font-weight:400;color:{GOLD};margin:0 0 16px 0;">&#x2713; Books Appointments</p>
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:32px;
    font-weight:400;color:{GOLD};margin:0;">&#x2713; Available 24/7</p>
    </div></div>"""

COST_CARD = f"""<div style="display:flex;align-items:center;justify-content:center;
    width:100%;height:100%;background:linear-gradient(135deg,{NAVY} 0%,#2d5a8c 100%);">
    <div style="text-align:center;padding:40px;">
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:36px;
    font-weight:700;color:#ffffff;margin:0 0 8px 0;">Start with a</p>
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:64px;
    font-weight:900;color:#4ade80;margin:0;">FREE TRIAL</p>
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:32px;
    font-weight:400;color:rgba(255,255,255,0.8);margin:20px 0 0 0;">Then just</p>
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:72px;
    font-weight:900;color:{GOLD};margin:4px 0 0 0;">$24.95/mo</p>
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:24px;
    font-weight:300;color:rgba(255,255,255,0.7);margin:12px 0 0 0;">No salary. No sick days. No missed customers.</p>
    </div></div>"""

CTA_CARD = f"""<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
    width:100%;height:100%;background:linear-gradient(180deg,{DARK_BG} 0%,{NAVY} 100%);">
    <div style="background:{GOLD};border-radius:16px;padding:16px 32px;margin-bottom:24px;">
        <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:28px;
        font-weight:900;color:{NAVY};margin:0;letter-spacing:1px;">JWAT</p>
    </div>
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:44px;
    font-weight:700;color:#ffffff;margin:0 0 8px 0;">JWAT Enterprise Inc</p>
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:24px;
    font-weight:400;color:rgba(255,255,255,0.7);margin:0 0 24px 0;">AI-Powered Business Consulting</p>
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:28px;
    font-weight:600;color:{GOLD};margin:0;">Link in bio &#x2193;</p>
    </div>"""

CARD_MAP = {
    "stat": STAT_CARD,
    "features": FEATURES_CARD,
    "cost": COST_CARD,
    "cta": CTA_CARD,
}

text_clips = []
video_clips = []

t = 0.0
for i, s in enumerate(shots):
    length = s["dur"] + PAD

    if s.get("card"):
        video_clips.append({
            "asset": {
                "type": "html",
                "html": CARD_MAP[s["card"]],
                "width": 1080,
                "height": 1920,
            },
            "start": t,
            "length": length,
            "transition": {"in": "fade", "out": "fade"},
        })
    elif s["broll"]:
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

    if s["text"] or s["sub"]:
        if not s.get("card"):
            text_clips.append({
                "asset": {
                    "type": "html",
                    "html": text_overlay(s["text"], s["sub"]),
                    "width": 1080,
                    "height": 400,
                },
                "start": t,
                "length": length,
                "position": "center",
                "transition": {"in": "fade", "out": "fade"},
            })

    t += length

render_config = {
    "timeline": {
        "background": "#000000",
        "tracks": [
            {"clips": text_clips},
            {"clips": video_clips},
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

json_path = os.path.join(os.path.dirname(__file__), "jwat-video1-shotstack-render.json")
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
                out_path = os.path.join(os.path.dirname(__file__), "exports", "jwat-missed-calls-ai.mp4")
                with open(out_path, "wb") as vf:
                    for chunk in dl.iter_content(chunk_size=8192):
                        vf.write(chunk)
                print(f"Saved to: {out_path}")
                print(f"Size: {os.path.getsize(out_path) / 1024 / 1024:.1f} MB")

                onedrive_path = os.path.expanduser("~/OneDrive/video-assets/exports/jwat-missed-calls-ai.mp4")
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
