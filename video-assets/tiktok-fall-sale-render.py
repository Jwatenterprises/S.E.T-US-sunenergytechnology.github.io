"""
TikTok Video: ALLPOWERS Fall Sale 2026 — Price Shock Hook
30 seconds, 9:16 (1080x1920), text + product images
Renders via Shotstack API
"""
import json
import requests
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = os.environ.get("SHOTSTACK_PROD_KEY", "GWoBAU0VdD6QvV3nWLlZyQKzHiU7L3FFaTAOBufc")
API_URL = "https://api.shotstack.io/edit/v1/render"

IMG_BASE = "https://raw.githubusercontent.com/Jwatenterprises/S.E.T-US-sunenergytechnology.github.io/main/images"
LOGO_URL = "https://raw.githubusercontent.com/Jwatenterprises/S.E.T-US-sunenergytechnology.github.io/main/set-logo.jpg"

# B-roll from Pexels (free, no attribution needed for video)
BROLL = {
    "solar": "https://videos.pexels.com/video-files/5233552/5233552-uhd_2560_1440_30fps.mp4",
    "power": "https://videos.pexels.com/video-files/4065388/4065388-hd_1920_1080_30fps.mp4",
}

def html_slide(main_text, sub_text, price_old=None, price_new=None, save_pct=None, code=None,
               size_main=56, size_sub=36, bg_color="rgba(0,0,0,0.75)"):
    """Generate HTML overlay for a TikTok slide."""
    price_html = ""
    if price_old and price_new:
        price_html = f"""
        <div style="margin:16px 0;">
          <span style="font-size:42px;color:#999;text-decoration:line-through;font-weight:400;">${price_old}</span>
          <span style="font-size:18px;color:#999;margin:0 8px;">→</span>
          <span style="font-size:64px;color:#FF4444;font-weight:900;">${price_new}</span>
        </div>"""
        if save_pct:
            price_html += f"""
        <div style="display:inline-block;background:#D97706;color:#fff;padding:6px 20px;border-radius:8px;
            font-size:28px;font-weight:800;letter-spacing:1px;margin-top:4px;">
          {save_pct}% OFF
        </div>"""

    code_html = ""
    if code:
        code_html = f"""
        <div style="margin-top:20px;background:#1E1E2E;border:2px solid #00C896;border-radius:12px;
            padding:12px 24px;display:inline-block;">
          <span style="font-size:16px;color:#aaa;font-weight:500;">USE CODE</span><br>
          <span style="font-family:'Courier New',monospace;font-size:40px;color:#00C896;font-weight:900;
              letter-spacing:3px;">{code}</span>
        </div>"""

    return f"""<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
        width:100%;height:100%;text-align:center;padding:60px 40px;background:{bg_color};">
        <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:{size_main}px;
            font-weight:900;color:#FFFFFF;margin:0;line-height:1.15;text-shadow:2px 2px 8px rgba(0,0,0,0.5);">
            {main_text}</p>
        <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:{size_sub}px;
            font-weight:500;color:rgba(255,255,255,0.8);margin:12px 0 0;line-height:1.3;
            text-shadow:1px 1px 4px rgba(0,0,0,0.5);">
            {sub_text}</p>
        {price_html}
        {code_html}
    </div>"""


# Define slides: 30 seconds total
slides = [
    {
        "start": 0, "dur": 5,
        "text": html_slide(
            "This solar generator<br>was <span style='color:#999;text-decoration:line-through'>$1,060</span>",
            "Right now it's",
            price_old=None, price_new=None,
            size_main=48, size_sub=32,
            bg_color="rgba(10,10,20,0.85)"
        ),
        "text2": html_slide(
            "", "",
            price_old="1,060", price_new="439", save_pct=59,
            bg_color="transparent"
        ),
        "img": f"{IMG_BASE}/allpowers-p1800.webp",
        "broll": "solar",
    },
    {
        "start": 5, "dur": 6,
        "text": html_slide(
            "ALLPOWERS R2500 V2",
            "1,920Wh · 2,500W Output",
            price_old="1,599", price_new="659", save_pct=59,
            bg_color="rgba(10,10,20,0.85)"
        ),
        "img": f"{IMG_BASE}/allpowers-r2400.webp",
        "broll": None,
    },
    {
        "start": 11, "dur": 5,
        "text": html_slide(
            "100W Solar Panel",
            "Cheapest from any real brand",
            price_old="199", price_new="69.99", save_pct=65,
            bg_color="rgba(10,10,20,0.85)"
        ),
        "img": None,
        "broll": "solar",
    },
    {
        "start": 16, "dur": 5,
        "text": html_slide(
            "S2000 Pro",
            "1,500Wh · 2,000W Output",
            price_old="1,399", price_new="549", save_pct=61,
            bg_color="rgba(10,10,20,0.85)"
        ),
        "img": None,
        "broll": "power",
    },
    {
        "start": 21, "dur": 4,
        "text": html_slide(
            "Extra Codes Stack<br>On Top",
            "",
            code="APSEP10",
            size_main=44,
            bg_color="rgba(10,10,20,0.92)"
        ),
        "img": None,
        "broll": None,
    },
    {
        "start": 25, "dur": 5,
        "text": html_slide(
            "Sale Ends Sep 30 🍂",
            "Every deal ranked ↓<br><br><span style='font-size:28px;color:#D97706;font-weight:800;'>Link in bio</span>",
            size_main=48, size_sub=32,
            bg_color="rgba(10,10,20,0.88)"
        ),
        "img": None,
        "broll": "solar",
    },
]


def build_timeline():
    """Build Shotstack timeline for 9:16 TikTok video."""
    tracks = []

    # Track 1: Text overlays (top layer)
    text_clips = []
    for s in slides:
        text_clips.append({
            "asset": {
                "type": "html",
                "html": s["text"],
                "width": 1080,
                "height": 1920,
            },
            "start": s["start"],
            "length": s["dur"],
            "transition": {
                "in": "fade",
                "out": "fade"
            },
            "effect": "zoomIn" if s["start"] == 0 else None,
        })
    # Remove None effects
    for c in text_clips:
        if c.get("effect") is None:
            del c["effect"]
    tracks.append({"clips": text_clips})

    # Track 2: Product images (middle layer)
    img_clips = []
    for s in slides:
        if s.get("img"):
            img_clips.append({
                "asset": {
                    "type": "image",
                    "src": s["img"],
                },
                "start": s["start"],
                "length": s["dur"],
                "fit": "contain",
                "position": "center",
                "offset": {"y": 0.15},
                "scale": 0.5,
                "opacity": 0.3,
                "transition": {
                    "in": "fade",
                    "out": "fade"
                },
            })
    if img_clips:
        tracks.append({"clips": img_clips})

    # Track 3: Background (b-roll or solid)
    bg_clips = []
    for s in slides:
        if s.get("broll") and s["broll"] in BROLL:
            bg_clips.append({
                "asset": {
                    "type": "video",
                    "src": BROLL[s["broll"]],
                    "trim": s["start"] % 10,
                    "volume": 0,
                },
                "start": s["start"],
                "length": s["dur"],
                "fit": "cover",
            })
        else:
            bg_clips.append({
                "asset": {
                    "type": "html",
                    "html": '<div style="width:100%;height:100%;background:linear-gradient(180deg,#0a0a1a 0%,#1a1a3e 50%,#2d1b00 100%);"></div>',
                    "width": 1080,
                    "height": 1920,
                },
                "start": s["start"],
                "length": s["dur"],
            })
    tracks.append({"clips": bg_clips})

    # Track 4: Logo watermark (persistent)
    tracks.insert(0, {
        "clips": [{
            "asset": {
                "type": "image",
                "src": LOGO_URL,
            },
            "start": 0,
            "length": 30,
            "position": "topRight",
            "offset": {"x": -0.04, "y": -0.03},
            "scale": 0.08,
            "opacity": 0.7,
        }]
    })

    return {
        "timeline": {
            "tracks": tracks,
            "background": "#0a0a1a",
        },
        "output": {
            "format": "mp4",
            "resolution": "1080",
            "aspectRatio": "9:16",
            "fps": 30,
        },
    }


def render_video():
    """Submit render to Shotstack and poll for result."""
    config = build_timeline()

    # Save config for reference
    config_path = os.path.join(os.path.dirname(__file__), "tiktok-fall-sale-config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Config saved to: {config_path}")

    # Submit render
    print("Submitting render to Shotstack...")
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }
    resp = requests.post(API_URL, json=config, headers=headers)
    if resp.status_code != 201:
        print(f"Error {resp.status_code}: {resp.text}")
        return None

    data = resp.json()
    render_id = data["response"]["id"]
    print(f"Render submitted! ID: {render_id}")

    # Poll for completion
    status_url = f"{API_URL}/{render_id}"
    for i in range(60):
        time.sleep(5)
        status_resp = requests.get(status_url, headers=headers)
        status_data = status_resp.json()
        state = status_data["response"]["status"]
        print(f"  [{i*5}s] Status: {state}")

        if state == "done":
            url = status_data["response"]["url"]
            print(f"\n✅ Video ready: {url}")
            return url
        elif state == "failed":
            print(f"\n❌ Render failed: {status_data}")
            return None

    print("Timed out waiting for render.")
    return None


if __name__ == "__main__":
    url = render_video()
    if url:
        print(f"\nDownload and post to TikTok @setuslove")
        print(f"Caption: This $1,060 solar generator is $439 right now 🍂 ALLPOWERS Fall Sale — up to 65% OFF through Sep 30. Codes APSEP10 (10% off) and APSEP110 ($110 off $1K+) stack on top. Every deal ranked → link in bio #solargenerator #allpowers #fallsale #solarpower #offgrid #powerstation #hurricane #prepper")
