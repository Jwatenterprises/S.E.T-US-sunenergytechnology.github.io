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
# JWAT Video 4 — "5 Ways to Fund Your Business in 2026"
# Educational content to keep JWAT channel active
# Same cartoon animation style
# Soft CTA to ROK Financial at end
# ============================================================

SCENE_1_HOOK = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#0f2744 0%,#1a365d 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;position:relative;">
<style>
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}
</style>
<div style="position:absolute;top:60px;right:80px;font-size:70px;animation:float 2s ease-in-out infinite;">&#x1F4B0;</div>
<div style="position:absolute;top:180px;left:60px;font-size:55px;animation:float 2.5s ease-in-out infinite 0.5s;">&#x1F4B8;</div>
<div style="font-size:60px;margin-bottom:16px;">&#x1F3AF;</div>
<p style="font-size:80px;font-weight:900;color:#ffd700;margin:0;">5 Ways</p>
<p style="font-size:44px;font-weight:700;color:#ffffff;margin:12px 40px 0;text-align:center;line-height:1.2;">to fund your business<br/>in 2026</p>
<p style="font-size:28px;font-weight:400;color:rgba(255,255,255,0.6);margin:16px 0 0 0;animation:pulse 1.5s ease-in-out infinite;">Save this &#x1F4CC;</p>
</div>"""

SCENE_2_WAY1 = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#1a1a2e 0%,#16213e 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;">
<style>
@keyframes slideIn{0%{transform:translateX(-60px);opacity:0}100%{transform:translateX(0);opacity:1}}
</style>
<div style="background:rgba(255,215,0,0.15);border-radius:50%;width:120px;height:120px;display:flex;align-items:center;justify-content:center;margin-bottom:20px;">
<p style="font-size:60px;font-weight:900;color:#ffd700;margin:0;">1</p>
</div>
<div style="font-size:80px;margin-bottom:12px;">&#x1F3E6;</div>
<p style="font-size:42px;font-weight:800;color:#ffffff;margin:0 40px;text-align:center;animation:slideIn 0.5s ease-out 0.2s both;">SBA Loans</p>
<p style="font-size:28px;font-weight:400;color:rgba(255,255,255,0.7);margin:16px 40px 0;text-align:center;animation:slideIn 0.5s ease-out 0.5s both;">Low rates. But 60-90 days to close.<br/>Need 680+ credit score.</p>
</div>"""

SCENE_3_WAY2 = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#16213e 0%,#1a1a2e 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;">
<style>
@keyframes slideIn{0%{transform:translateX(-60px);opacity:0}100%{transform:translateX(0);opacity:1}}
</style>
<div style="background:rgba(255,215,0,0.15);border-radius:50%;width:120px;height:120px;display:flex;align-items:center;justify-content:center;margin-bottom:20px;">
<p style="font-size:60px;font-weight:900;color:#ffd700;margin:0;">2</p>
</div>
<div style="font-size:80px;margin-bottom:12px;">&#x1F4B3;</div>
<p style="font-size:42px;font-weight:800;color:#ffffff;margin:0 40px;text-align:center;animation:slideIn 0.5s ease-out 0.2s both;">Business Credit Cards</p>
<p style="font-size:28px;font-weight:400;color:rgba(255,255,255,0.7);margin:16px 40px 0;text-align:center;animation:slideIn 0.5s ease-out 0.5s both;">Fast access. But 18-28% APR.<br/>Easy to overspend.</p>
</div>"""

SCENE_4_WAY3 = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#1a1a2e 0%,#16213e 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;">
<style>
@keyframes slideIn{0%{transform:translateX(-60px);opacity:0}100%{transform:translateX(0);opacity:1}}
</style>
<div style="background:rgba(255,215,0,0.15);border-radius:50%;width:120px;height:120px;display:flex;align-items:center;justify-content:center;margin-bottom:20px;">
<p style="font-size:60px;font-weight:900;color:#ffd700;margin:0;">3</p>
</div>
<div style="font-size:80px;margin-bottom:12px;">&#x1F91D;</div>
<p style="font-size:42px;font-weight:800;color:#ffffff;margin:0 40px;text-align:center;animation:slideIn 0.5s ease-out 0.2s both;">Investors / Angels</p>
<p style="font-size:28px;font-weight:400;color:rgba(255,255,255,0.7);margin:16px 40px 0;text-align:center;animation:slideIn 0.5s ease-out 0.5s both;">Big money. But you give up equity.<br/>Hard to find. Takes months.</p>
</div>"""

SCENE_5_WAY4 = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#16213e 0%,#1a1a2e 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;">
<style>
@keyframes slideIn{0%{transform:translateX(-60px);opacity:0}100%{transform:translateX(0);opacity:1}}
</style>
<div style="background:rgba(255,215,0,0.15);border-radius:50%;width:120px;height:120px;display:flex;align-items:center;justify-content:center;margin-bottom:20px;">
<p style="font-size:60px;font-weight:900;color:#ffd700;margin:0;">4</p>
</div>
<div style="font-size:80px;margin-bottom:12px;">&#x1F3E0;</div>
<p style="font-size:42px;font-weight:800;color:#ffffff;margin:0 40px;text-align:center;animation:slideIn 0.5s ease-out 0.2s both;">Home Equity / HELOC</p>
<p style="font-size:28px;font-weight:400;color:rgba(255,255,255,0.7);margin:16px 40px 0;text-align:center;animation:slideIn 0.5s ease-out 0.5s both;">Lower rates. But your house<br/>is on the line. &#x1F6A8;</p>
</div>"""

SCENE_6_WAY5 = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#0a1628 0%,#1a365d 60%,#2d5a8c 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;position:relative;">
<style>
@keyframes rocketIn{0%{transform:translateY(200px) scale(0.3);opacity:0}100%{transform:translateY(0) scale(1);opacity:1}}
@keyframes glow{0%,100%{text-shadow:0 0 20px rgba(74,222,128,0.5)}50%{text-shadow:0 0 40px rgba(74,222,128,0.9)}}
@keyframes sparkle{0%,100%{opacity:0.3}50%{opacity:1}}
</style>
<div style="position:absolute;top:80px;left:60px;font-size:28px;animation:sparkle 1s infinite;">&#x2B50;</div>
<div style="position:absolute;top:150px;right:80px;font-size:24px;animation:sparkle 1s infinite 0.3s;">&#x2B50;</div>
<div style="background:rgba(74,222,128,0.15);border-radius:50%;width:120px;height:120px;display:flex;align-items:center;justify-content:center;margin-bottom:20px;">
<p style="font-size:60px;font-weight:900;color:#4ade80;margin:0;">5</p>
</div>
<div style="font-size:80px;animation:rocketIn 0.8s ease-out forwards;margin-bottom:12px;">&#x1F680;</div>
<p style="font-size:42px;font-weight:800;color:#4ade80;margin:0 40px;text-align:center;animation:glow 2s ease-in-out infinite;">Revenue-Based Funding</p>
<p style="font-size:28px;font-weight:400;color:#ffffff;margin:16px 40px 0;text-align:center;">24-48hr approvals. No collateral.<br/>No perfect credit. <span style="color:#ffd700;font-weight:700;">$5K&#x2013;$5M.</span></p>
</div>"""

SCENE_7_CTA = """<div style="width:100%;height:100%;background:linear-gradient(180deg,#0d1b2a 0%,#1a365d 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Helvetica Neue',Arial,sans-serif;overflow:hidden;">
<style>
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
@keyframes fadeSlide{0%{transform:translateY(30px);opacity:0}100%{transform:translateY(0);opacity:1}}
</style>
<div style="background:#ffd700;border-radius:20px;padding:16px 40px;margin-bottom:28px;animation:fadeSlide 0.5s ease-out forwards;">
<p style="font-size:32px;font-weight:900;color:#1a365d;margin:0;letter-spacing:2px;">JWAT</p>
</div>
<p style="font-size:36px;font-weight:700;color:#ffffff;margin:0 40px;text-align:center;animation:fadeSlide 0.5s ease-out 0.3s both;">Option 5 is what<br/>we recommend.</p>
<p style="font-size:28px;font-weight:400;color:rgba(255,255,255,0.7);margin:12px 40px 0;text-align:center;animation:fadeSlide 0.5s ease-out 0.5s both;">Check your rate. Free. 2 minutes.</p>
<p style="font-size:32px;font-weight:700;color:#ffd700;margin:32px 0 0 0;animation:bounce 1s ease-in-out infinite;">Link in bio &#x2B07;&#xFE0F;</p>
</div>"""

shots = [
    {"dur": 4.0, "html": SCENE_1_HOOK},
    {"dur": 4.0, "html": SCENE_2_WAY1},
    {"dur": 4.0, "html": SCENE_3_WAY2},
    {"dur": 4.0, "html": SCENE_4_WAY3},
    {"dur": 4.0, "html": SCENE_5_WAY4},
    {"dur": 5.0, "html": SCENE_6_WAY5},
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

print(f"=== JWAT Video 4: 5 Ways to Fund Your Business in 2026 ===")
print(f"Total duration: {t:.1f}s")
print(f"Shots: {len(shots)}")
print(f"All HTML cartoon cards — no external URLs")

json_path = os.path.join(os.path.dirname(__file__), "jwat-video4-5ways-funding-cartoon-render.json")
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

                out_path = os.path.join(os.path.dirname(__file__), "exports", "jwat-5ways-funding-cartoon.mp4")
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                dl = requests.get(dl_url, stream=True, timeout=120)
                with open(out_path, "wb") as vf:
                    for chunk in dl.iter_content(chunk_size=8192):
                        vf.write(chunk)
                print(f"Saved to: {out_path}")
                print(f"Size: {os.path.getsize(out_path) / 1024 / 1024:.1f} MB")

                onedrive_path = os.path.expanduser("~/OneDrive/video-assets/exports/jwat-5ways-funding-cartoon.mp4")
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
