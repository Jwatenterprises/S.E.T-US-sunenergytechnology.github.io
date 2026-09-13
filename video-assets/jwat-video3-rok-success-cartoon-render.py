import json
import requests
import os
import sys
import time
import shutil

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = os.environ.get("SHOTSTACK_PROD_KEY", "GWoBAU0VdD6QvV3nWLlZyQKzHiU7L3FFaTAOBufc")
API_URL = "https://api.shotstack.io/edit/v1/render"

PAD = 0.5

# ============================================================
# JWAT Video 3 — ROK Financial Follow-Up: "Your Next Success Story"
# Based on ROK email: "Last Month's Affiliate Wins & Highlights"
# Same cartoon animation style as jwat-video2-rok-cartoon
# CTA: Submit a client → be the next success story
# ============================================================

SCENE_1_HOOK = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#0f2744 0%,#1a365d 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;position:relative;">
<style>
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}
</style>
<div style="position:absolute;top:60px;right:80px;font-size:70px;animation:float 2s ease-in-out infinite;">&#x1F4E7;</div>
<div style="position:absolute;top:180px;left:60px;font-size:55px;animation:float 2.5s ease-in-out infinite 0.5s;">&#x1F4CA;</div>
<div style="font-size:140px;margin-bottom:24px;">&#x1F3C6;</div>
<p style="font-size:48px;font-weight:800;color:#ffffff;margin:0 40px;text-align:center;line-height:1.2;">Last month's<br/>affiliate wins are in.</p>
<p style="font-size:34px;font-weight:400;color:#ffd700;margin:16px 0 0 0;animation:pulse 1.5s ease-in-out infinite;">And they're BIG.</p>
</div>"""

SCENE_2_WINS = """<div style="width:100%;height:100%;background:linear-gradient(135deg,#0d1b2a 0%,#1a365d 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;position:relative;">
<style>
@keyframes confetti1{0%{transform:translateY(0) rotate(0);opacity:1}100%{transform:translateY(300px) rotate(360deg);opacity:0}}
@keyframes confetti2{0%{transform:translateY(0) rotate(0);opacity:1}100%{transform:translateY(250px) rotate(-270deg);opacity:0}}
@keyframes popIn{0%{transform:scale(0);opacity:0}60%{transform:scale(1.15)}100%{transform:scale(1);opacity:1}}
</style>
<div style="position:absolute;top:60px;left:80px;font-size:30px;animation:confetti1 2s linear infinite;">&#x1F389;</div>
<div style="position:absolute;top:40px;right:100px;font-size:28px;animation:confetti2 2s linear infinite 0.4s;">&#x1F38A;</div>
<div style="position:absolute;top:120px;left:200px;font-size:24px;animation:confetti1 2s linear infinite 0.8s;">&#x2728;</div>
<div style="position:absolute;top:100px;right:180px;font-size:26px;animation:confetti2 2s linear infinite 1.2s;">&#x1F4B0;</div>
<p style="font-size:36px;font-weight:400;color:rgba(255,255,255,0.7);margin:0 0 8px 0;">Real affiliates. Real commissions.</p>
<p style="font-size:90px;font-weight:900;color:#4ade80;margin:0;animation:popIn 0.6s ease-out forwards;">$$$$</p>
<p style="font-size:40px;font-weight:700;color:#ffffff;margin:20px 40px 0;text-align:center;line-height:1.3;">Businesses got funded.<br/>Partners got <span style="color:#ffd700;">PAID.</span></p>
</div>"""

SCENE_3_QUESTION = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#1a1a2e 0%,#16213e 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;position:relative;">
<style>
@keyframes pointDown{0%,100%{transform:translateY(0)}50%{transform:translateY(15px)}}
@keyframes glow{0%,100%{text-shadow:0 0 20px rgba(255,215,0,0.4)}50%{text-shadow:0 0 50px rgba(255,215,0,0.9)}}
</style>
<div style="font-size:120px;margin-bottom:20px;">&#x1F914;</div>
<p style="font-size:44px;font-weight:800;color:#ffffff;margin:0 40px;text-align:center;line-height:1.3;">Ready to be<br/>the <span style="color:#ffd700;animation:glow 2s ease-in-out infinite;">NEXT</span><br/>success story?</p>
<div style="font-size:60px;margin-top:24px;animation:pointDown 1s ease-in-out infinite;">&#x1F447;</div>
</div>"""

SCENE_4_PORTAL = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#0a1628 0%,#1a365d 60%,#2d5a8c 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;position:relative;">
<style>
@keyframes slideRight{0%{transform:translateX(-80px);opacity:0}100%{transform:translateX(0);opacity:1}}
@keyframes sparkle{0%,100%{opacity:0.3}50%{opacity:1}}
</style>
<div style="position:absolute;top:80px;left:60px;font-size:28px;animation:sparkle 1s infinite;">&#x2B50;</div>
<div style="position:absolute;top:140px;right:80px;font-size:24px;animation:sparkle 1s infinite 0.3s;">&#x2B50;</div>
<div style="font-size:100px;margin-bottom:20px;">&#x1F4BB;</div>
<p style="font-size:40px;font-weight:800;color:#ffffff;margin:0 0 28px 0;text-align:center;">Here's how it works:</p>
<div style="display:flex;align-items:center;gap:16px;margin:0 40px 16px;animation:slideRight 0.5s ease-out 0.2s both;">
<span style="font-size:40px;">1&#xFE0F;&#x20E3;</span>
<p style="font-size:30px;color:#ffd700;margin:0;font-weight:600;">Submit a client into your portal</p>
</div>
<div style="display:flex;align-items:center;gap:16px;margin:0 40px 16px;animation:slideRight 0.5s ease-out 0.6s both;">
<span style="font-size:40px;">2&#xFE0F;&#x20E3;</span>
<p style="font-size:30px;color:#ffd700;margin:0;font-weight:600;">ROK matches them with funding</p>
</div>
<div style="display:flex;align-items:center;gap:16px;margin:0 40px 16px;animation:slideRight 0.5s ease-out 1.0s both;">
<span style="font-size:40px;">3&#xFE0F;&#x20E3;</span>
<p style="font-size:30px;color:#ffd700;margin:0;font-weight:600;">They get funded. You get paid.</p>
</div>
</div>"""

SCENE_5_SPEED = """<div style="width:100%;height:100%;background:linear-gradient(135deg,#1a365d 0%,#2d5a8c 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;position:relative;">
<style>
@keyframes rocketIn{0%{transform:translateY(200px) scale(0.3);opacity:0}100%{transform:translateY(0) scale(1);opacity:1}}
@keyframes countUp{0%{opacity:0;transform:scale(0.5)}100%{opacity:1;transform:scale(1)}}
</style>
<div style="font-size:100px;animation:rocketIn 0.8s ease-out forwards;margin-bottom:16px;">&#x26A1;</div>
<p style="font-size:36px;font-weight:400;color:rgba(255,255,255,0.7);margin:0 0 8px 0;">Approvals in as fast as</p>
<p style="font-size:100px;font-weight:900;color:#4ade80;margin:0;animation:countUp 0.8s ease-out forwards;">24 HRS</p>
<p style="font-size:32px;font-weight:600;color:#ffffff;margin:20px 40px 0;text-align:center;">$5K to $5M+<br/>No perfect credit needed.</p>
</div>"""

SCENE_6_SOCIAL = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#0d1b2a 0%,#1a365d 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;">
<style>
@keyframes checkIn1{0%{transform:translateX(-100px);opacity:0}100%{transform:translateX(0);opacity:1}}
@keyframes checkIn2{0%{transform:translateX(-100px);opacity:0}100%{transform:translateX(0);opacity:1}}
@keyframes checkIn3{0%{transform:translateX(-100px);opacity:0}100%{transform:translateX(0);opacity:1}}
@keyframes checkIn4{0%{transform:translateX(-100px);opacity:0}100%{transform:translateX(0);opacity:1}}
</style>
<p style="font-size:38px;font-weight:800;color:#ffffff;margin:0 0 32px 0;">Who can you refer?</p>
<div style="display:flex;align-items:center;gap:16px;margin:0 40px 18px;animation:checkIn1 0.5s ease-out 0.2s both;">
<span style="font-size:40px;">&#x1F3E0;</span>
<p style="font-size:30px;color:#ffd700;margin:0;font-weight:600;">Real estate agents</p>
</div>
<div style="display:flex;align-items:center;gap:16px;margin:0 40px 18px;animation:checkIn2 0.5s ease-out 0.5s both;">
<span style="font-size:40px;">&#x1F69A;</span>
<p style="font-size:30px;color:#ffd700;margin:0;font-weight:600;">Contractors & truckers</p>
</div>
<div style="display:flex;align-items:center;gap:16px;margin:0 40px 18px;animation:checkIn3 0.5s ease-out 0.8s both;">
<span style="font-size:40px;">&#x1F4BC;</span>
<p style="font-size:30px;color:#ffd700;margin:0;font-weight:600;">Any small biz owner</p>
</div>
<div style="display:flex;align-items:center;gap:16px;margin:0 40px 18px;animation:checkIn4 0.5s ease-out 1.1s both;">
<span style="font-size:40px;">&#x1F680;</span>
<p style="font-size:30px;color:#ffd700;margin:0;font-weight:600;">Startups needing capital</p>
</div>
</div>"""

SCENE_7_CTA = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#0d1b2a 0%,#1a365d 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;">
<style>
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
@keyframes fadeSlide{0%{transform:translateY(30px);opacity:0}100%{transform:translateY(0);opacity:1}}
@keyframes glow{0%,100%{text-shadow:0 0 20px rgba(255,215,0,0.5)}50%{text-shadow:0 0 40px rgba(255,215,0,0.9)}}
</style>
<div style="background:#ffd700;border-radius:20px;padding:16px 40px;margin-bottom:28px;animation:fadeSlide 0.5s ease-out forwards;">
<p style="font-size:32px;font-weight:900;color:#1a365d;margin:0;letter-spacing:2px;">JWAT</p>
</div>
<p style="font-size:38px;font-weight:700;color:#ffffff;margin:0 40px;text-align:center;animation:fadeSlide 0.5s ease-out 0.3s both;">Submit your client.</p>
<p style="font-size:38px;font-weight:700;color:#4ade80;margin:8px 40px 0;text-align:center;animation:fadeSlide 0.5s ease-out 0.5s both;">Be the next success story.</p>
<p style="font-size:30px;font-weight:400;color:rgba(255,255,255,0.7);margin:16px 40px 0;text-align:center;animation:fadeSlide 0.5s ease-out 0.7s both;">ROK Financial &#x2014; funding fast.</p>
<p style="font-size:32px;font-weight:700;color:#ffd700;margin:32px 0 0 0;animation:bounce 1s ease-in-out infinite;">Link in bio &#x2B07;&#xFE0F;</p>
</div>"""

shots = [
    {"dur": 4.0, "html": SCENE_1_HOOK},
    {"dur": 4.0, "html": SCENE_2_WINS},
    {"dur": 4.0, "html": SCENE_3_QUESTION},
    {"dur": 5.0, "html": SCENE_4_PORTAL},
    {"dur": 4.0, "html": SCENE_5_SPEED},
    {"dur": 5.0, "html": SCENE_6_SOCIAL},
    {"dur": 4.0, "html": SCENE_7_CTA},
]

clips = []
t = 0.0
for s in shots:
    length = s["dur"] + PAD
    clips.append({
        "asset": {
            "type": "html",
            "html": s["html"],
            "width": 1080,
            "height": 1920,
        },
        "start": t,
        "length": length,
        "transition": {"in": "fade", "out": "fade"},
    })
    t += length

render_config = {
    "timeline": {
        "background": "#000000",
        "tracks": [{"clips": clips}],
    },
    "output": {
        "format": "mp4",
        "resolution": "hd",
        "size": {"width": 1080, "height": 1920},
        "fps": 30,
        "quality": "high",
    },
}

print(f"=== JWAT Video 3: ROK Financial — Your Next Success Story ===")
print(f"Total duration: {t:.1f}s")
print(f"Shots: {len(shots)}")
print(f"All HTML cartoon cards — no external URLs")

json_path = os.path.join(os.path.dirname(__file__), "jwat-video3-rok-success-cartoon-render.json")
with open(json_path, "w") as f:
    json.dump(render_config, f, indent=2)
print(f"\nRender JSON saved to: {json_path}")

print("\nSubmitting to Shotstack Production API...")
resp = requests.post(
    API_URL,
    headers={"x-api-key": API_KEY, "Content-Type": "application/json"},
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

                out_path = os.path.join(os.path.dirname(__file__), "exports", "jwat-rok-success-story-cartoon.mp4")
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                dl = requests.get(dl_url, stream=True, timeout=120)
                with open(out_path, "wb") as vf:
                    for chunk in dl.iter_content(chunk_size=8192):
                        vf.write(chunk)
                print(f"Saved to: {out_path}")
                print(f"Size: {os.path.getsize(out_path) / 1024 / 1024:.1f} MB")

                onedrive_path = os.path.expanduser("~/OneDrive/video-assets/exports/jwat-rok-success-story-cartoon.mp4")
                os.makedirs(os.path.dirname(onedrive_path), exist_ok=True)
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
