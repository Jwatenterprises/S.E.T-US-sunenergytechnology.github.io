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
NAVY = "#1a365d"
GOLD = "#ffd700"
DARK_BG = "#0d1b2a"

# All shots are HTML cartoon cards — no external B-roll URLs needed

SCENE_1 = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#0f2744 0%,#1a365d 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;position:relative;">
<style>
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
@keyframes blink{0%,90%,100%{opacity:1}95%{opacity:0}}
</style>
<div style="position:absolute;top:60px;right:80px;font-size:80px;animation:float 2s ease-in-out infinite;">&#x1F4B0;</div>
<div style="position:absolute;top:180px;left:60px;font-size:60px;animation:float 2.5s ease-in-out infinite 0.5s;">&#x1F4B8;</div>
<div style="font-size:160px;margin-bottom:20px;animation:blink 3s infinite;">&#x1F468;&#x200D;&#x1F4BC;</div>
<p style="font-size:52px;font-weight:800;color:#ffffff;margin:0 40px;text-align:center;line-height:1.2;">Your business<br/>needs capital.</p>
<p style="font-size:36px;font-weight:400;color:#ffd700;margin:16px 0 0 0;animation:pulse 1.5s ease-in-out infinite;">But where do you go?</p>
</div>"""

SCENE_2 = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#1a1a2e 0%,#16213e 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;position:relative;">
<style>
@keyframes shake{0%,100%{transform:rotate(0)}25%{transform:rotate(-3deg)}75%{transform:rotate(3deg)}}
@keyframes stampIn{0%{transform:scale(3) rotate(-20deg);opacity:0}60%{transform:scale(1) rotate(-12deg);opacity:1}100%{transform:scale(1) rotate(-12deg);opacity:1}}
</style>
<div style="font-size:140px;animation:shake 0.5s ease-in-out infinite;">&#x1F3E6;</div>
<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) rotate(-12deg);animation:stampIn 0.8s ease-out forwards;">
<div style="border:8px solid #ff4444;border-radius:12px;padding:12px 40px;background:rgba(255,68,68,0.15);">
<p style="font-size:64px;font-weight:900;color:#ff4444;margin:0;letter-spacing:8px;">DENIED</p>
</div>
</div>
<p style="font-size:40px;font-weight:700;color:#ffffff;margin:40px 40px 0;text-align:center;line-height:1.2;">The bank said <span style="color:#ff4444;">NO.</span></p>
</div>"""

SCENE_3 = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#1a1a2e 0%,#0d1b2a 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;position:relative;">
<style>
@keyframes spin{0%{transform:rotate(0)}100%{transform:rotate(360deg)}}
@keyframes flyUp{0%{transform:translateY(0) rotate(0);opacity:1}100%{transform:translateY(-400px) rotate(45deg);opacity:0}}
</style>
<div style="position:absolute;top:100px;left:80px;font-size:50px;animation:flyUp 2s linear infinite;">&#x1F4C4;</div>
<div style="position:absolute;top:200px;right:60px;font-size:45px;animation:flyUp 2s linear infinite 0.7s;">&#x1F4C3;</div>
<div style="position:absolute;top:300px;left:160px;font-size:40px;animation:flyUp 2s linear infinite 1.3s;">&#x1F4DD;</div>
<div style="font-size:120px;animation:spin 3s linear infinite;">&#x23F3;</div>
<p style="font-size:48px;font-weight:800;color:#ffffff;margin:24px 40px 0;text-align:center;line-height:1.2;">Weeks of paperwork.</p>
<p style="font-size:40px;font-weight:400;color:#ff6b6b;margin:12px 0 0 0;">Still waiting...</p>
</div>"""

SCENE_4_STAT = """<div style="width:100%;height:100%;background:linear-gradient(135deg,#0d1b2a 0%,#1a365d 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;">
<style>
@keyframes countUp{0%{opacity:0;transform:scale(0.5)}100%{opacity:1;transform:scale(1)}}
@keyframes slideUp{0%{transform:translateY(40px);opacity:0}100%{transform:translateY(0);opacity:1}}
</style>
<div style="font-size:80px;margin-bottom:16px;">&#x1F4C9;</div>
<p style="font-size:120px;font-weight:900;color:#ffd700;margin:0;animation:countUp 0.8s ease-out forwards;">82%</p>
<p style="font-size:32px;font-weight:400;color:#ffffff;margin:16px 40px 0;text-align:center;animation:slideUp 0.6s ease-out 0.4s both;">of small businesses</p>
<p style="font-size:38px;font-weight:700;color:#ff6b6b;margin:8px 0 0 0;animation:slideUp 0.6s ease-out 0.7s both;">fail from cash flow problems</p>
</div>"""

SCENE_5_HERO = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#0a1628 0%,#1a365d 60%,#2d5a8c 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;position:relative;">
<style>
@keyframes rocketIn{0%{transform:translateY(200px) scale(0.3);opacity:0}100%{transform:translateY(0) scale(1);opacity:1}}
@keyframes glow{0%,100%{text-shadow:0 0 20px rgba(255,215,0,0.5)}50%{text-shadow:0 0 40px rgba(255,215,0,0.9)}}
@keyframes sparkle{0%,100%{opacity:0.3}50%{opacity:1}}
</style>
<div style="position:absolute;top:80px;left:60px;font-size:30px;animation:sparkle 1s infinite;">&#x2B50;</div>
<div style="position:absolute;top:150px;right:80px;font-size:25px;animation:sparkle 1s infinite 0.3s;">&#x2B50;</div>
<div style="position:absolute;top:120px;left:200px;font-size:20px;animation:sparkle 1s infinite 0.6s;">&#x2B50;</div>
<div style="font-size:100px;animation:rocketIn 0.8s ease-out forwards;margin-bottom:24px;">&#x1F680;</div>
<p style="font-size:52px;font-weight:900;color:#ffd700;margin:0;animation:glow 2s ease-in-out infinite;">ROK Financial</p>
<p style="font-size:36px;font-weight:600;color:#ffffff;margin:20px 40px 0;text-align:center;">gets businesses funded<br/><span style="color:#4ade80;font-size:44px;font-weight:900;">FAST.</span></p>
</div>"""

SCENE_6_FEATURES = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#0d1b2a 0%,#1a365d 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;">
<style>
@keyframes checkIn1{0%{transform:translateX(-100px);opacity:0}100%{transform:translateX(0);opacity:1}}
@keyframes checkIn2{0%{transform:translateX(-100px);opacity:0}100%{transform:translateX(0);opacity:1}}
@keyframes checkIn3{0%{transform:translateX(-100px);opacity:0}100%{transform:translateX(0);opacity:1}}
</style>
<p style="font-size:42px;font-weight:800;color:#ffffff;margin:0 0 40px 0;">Why ROK?</p>
<div style="display:flex;align-items:center;gap:16px;margin:0 40px 20px;animation:checkIn1 0.5s ease-out 0.2s both;">
<span style="font-size:44px;">&#x1F4B5;</span>
<p style="font-size:32px;color:#ffd700;margin:0;font-weight:600;">$5K &#x2013; $5M funding</p>
</div>
<div style="display:flex;align-items:center;gap:16px;margin:0 40px 20px;animation:checkIn2 0.5s ease-out 0.6s both;">
<span style="font-size:44px;">&#x26A1;</span>
<p style="font-size:32px;color:#ffd700;margin:0;font-weight:600;">Approved in 24&#x2013;48 hrs</p>
</div>
<div style="display:flex;align-items:center;gap:16px;margin:0 40px 20px;animation:checkIn3 0.5s ease-out 1.0s both;">
<span style="font-size:44px;">&#x1F513;</span>
<p style="font-size:32px;color:#ffd700;margin:0;font-weight:600;">No collateral required</p>
</div>
</div>"""

SCENE_7_CASE = """<div style="width:100%;height:100%;background:linear-gradient(135deg,#1a365d 0%,#2d5a8c 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;position:relative;">
<style>
@keyframes popIn{0%{transform:scale(0);opacity:0}60%{transform:scale(1.15)}100%{transform:scale(1);opacity:1}}
@keyframes confetti1{0%{transform:translateY(0) rotate(0);opacity:1}100%{transform:translateY(300px) rotate(360deg);opacity:0}}
@keyframes confetti2{0%{transform:translateY(0) rotate(0);opacity:1}100%{transform:translateY(250px) rotate(-270deg);opacity:0}}
</style>
<div style="position:absolute;top:80px;left:100px;font-size:30px;animation:confetti1 2s linear infinite;">&#x1F389;</div>
<div style="position:absolute;top:60px;right:120px;font-size:28px;animation:confetti2 2s linear infinite 0.5s;">&#x1F38A;</div>
<div style="position:absolute;top:150px;left:200px;font-size:24px;animation:confetti1 2s linear infinite 1s;">&#x2728;</div>
<p style="font-size:30px;font-weight:400;color:rgba(255,255,255,0.7);margin:0 0 8px 0;">Real result:</p>
<p style="font-size:100px;font-weight:900;color:#4ade80;margin:0;animation:popIn 0.6s ease-out forwards;">$1M</p>
<p style="font-size:38px;font-weight:600;color:#ffffff;margin:16px 0 0 0;">funded in 48 hours</p>
<p style="font-size:26px;font-weight:300;color:rgba(255,255,255,0.7);margin:20px 40px 0;text-align:center;">No bank. No waiting. No BS.</p>
</div>"""

SCENE_8_CTA = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#0d1b2a 0%,#1a365d 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;">
<style>
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
@keyframes fadeSlide{0%{transform:translateY(30px);opacity:0}100%{transform:translateY(0);opacity:1}}
</style>
<div style="background:#ffd700;border-radius:20px;padding:16px 40px;margin-bottom:28px;animation:fadeSlide 0.5s ease-out forwards;">
<p style="font-size:32px;font-weight:900;color:#1a365d;margin:0;letter-spacing:2px;">JWAT</p>
</div>
<p style="font-size:42px;font-weight:700;color:#ffffff;margin:0 40px;text-align:center;animation:fadeSlide 0.5s ease-out 0.3s both;">Stop waiting on banks.</p>
<p style="font-size:32px;font-weight:400;color:rgba(255,255,255,0.7);margin:12px 40px 0;text-align:center;animation:fadeSlide 0.5s ease-out 0.5s both;">Get funded in 48 hours.</p>
<p style="font-size:32px;font-weight:700;color:#ffd700;margin:32px 0 0 0;animation:bounce 1s ease-in-out infinite;">Link in bio &#x2B07;&#xFE0F;</p>
</div>"""

shots = [
    {"dur": 4.0, "html": SCENE_1},
    {"dur": 3.5, "html": SCENE_2},
    {"dur": 4.0, "html": SCENE_3},
    {"dur": 4.0, "html": SCENE_4_STAT},
    {"dur": 4.0, "html": SCENE_5_HERO},
    {"dur": 4.5, "html": SCENE_6_FEATURES},
    {"dur": 4.0, "html": SCENE_7_CASE},
    {"dur": 3.5, "html": SCENE_8_CTA},
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

print(f"Total duration: {t:.1f}s")
print(f"Shots: {len(shots)}")
print(f"All HTML cards — no external URLs")

json_path = os.path.join(os.path.dirname(__file__), "jwat-video2-rok-cartoon-render.json")
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

                os.makedirs(os.path.join(os.path.dirname(__file__), "exports"), exist_ok=True)
                dl = requests.get(dl_url, stream=True, timeout=120)
                out_path = os.path.join(os.path.dirname(__file__), "exports", "jwat-rok-financial-cartoon.mp4")
                with open(out_path, "wb") as vf:
                    for chunk in dl.iter_content(chunk_size=8192):
                        vf.write(chunk)
                print(f"Saved to: {out_path}")
                print(f"Size: {os.path.getsize(out_path) / 1024 / 1024:.1f} MB")

                onedrive_path = os.path.expanduser("~/OneDrive/video-assets/exports/jwat-rok-financial-cartoon.mp4")
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
