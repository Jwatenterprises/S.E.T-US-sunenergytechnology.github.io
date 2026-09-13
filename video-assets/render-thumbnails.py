import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
import os

out_dir = r'C:\Users\Milli\Documents\SunEnergyTechnology\video-assets'

apartment_html = """
<div style="width:1280px;height:720px;background:linear-gradient(135deg,#0a1628 0%,#1a3a5c 50%,#0d2847 100%);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;">
    <div style="position:absolute;top:0;left:0;width:100%;height:100%;background:radial-gradient(circle at 30% 40%,rgba(0,212,170,0.15),transparent 60%);z-index:1;"></div>
    <div style="z-index:2;text-align:center;padding:40px;">
        <div style="background:rgba(0,212,170,0.2);border:2px solid #00d4aa;border-radius:12px;padding:8px 24px;display:inline-block;margin-bottom:24px;">
            <span style="font-family:Arial,sans-serif;font-size:22px;font-weight:700;color:#00d4aa;letter-spacing:2px;">NO ROOF? NO PROBLEM</span>
        </div>
        <h1 style="font-family:Arial,sans-serif;font-size:72px;font-weight:900;color:#ffffff;margin:0 0 16px 0;line-height:1.1;text-shadow:2px 2px 10px rgba(0,0,0,0.5);">APARTMENT<br/>SOLAR POWER</h1>
        <p style="font-family:Arial,sans-serif;font-size:36px;font-weight:400;color:#88bbff;margin:0 0 24px 0;">BLUETTI AC200L &bull; 2,048Wh</p>
        <div style="display:flex;gap:16px;justify-content:center;">
            <div style="background:rgba(255,255,255,0.1);border-radius:8px;padding:12px 20px;">
                <span style="font-family:Arial,sans-serif;font-size:20px;color:#ffffff;">&#x26A1; Balcony Charging</span>
            </div>
            <div style="background:rgba(255,255,255,0.1);border-radius:8px;padding:12px 20px;">
                <span style="font-family:Arial,sans-serif;font-size:20px;color:#ffffff;">&#x1F50C; Under $2K</span>
            </div>
        </div>
    </div>
    <div style="position:absolute;bottom:20px;right:30px;z-index:3;">
        <div style="background:#00d4aa;border-radius:8px;padding:8px 16px;">
            <span style="font-family:Arial,sans-serif;font-size:18px;font-weight:700;color:#0a1628;">S.E.T. Solar</span>
        </div>
    </div>
</div>
"""

gas_vs_solar_html = """
<div style="width:1280px;height:720px;background:linear-gradient(135deg,#1a0a0a 0%,#2a1a0a 50%,#0d1f3c 100%);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;">
    <div style="position:absolute;top:0;left:0;width:50%;height:100%;background:linear-gradient(180deg,rgba(255,80,80,0.15),transparent 70%);z-index:1;"></div>
    <div style="position:absolute;top:0;right:0;width:50%;height:100%;background:linear-gradient(180deg,rgba(0,212,170,0.15),transparent 70%);z-index:1;"></div>
    <div style="z-index:2;text-align:center;padding:40px;">
        <h1 style="font-family:Arial,sans-serif;font-size:80px;font-weight:900;color:#ffffff;margin:0 0 20px 0;line-height:1.0;text-shadow:3px 3px 12px rgba(0,0,0,0.7);">GAS <span style="color:#ff5050;">vs</span> SOLAR</h1>
        <p style="font-family:Arial,sans-serif;font-size:44px;font-weight:700;color:#f0f0f0;margin:0 0 30px 0;">The Real Cost Breakdown</p>
        <div style="display:flex;gap:40px;justify-content:center;align-items:center;">
            <div style="text-align:center;">
                <p style="font-family:Arial,sans-serif;font-size:56px;font-weight:900;color:#ff5050;margin:0;">$800+</p>
                <p style="font-family:Arial,sans-serif;font-size:22px;color:#ffaaaa;margin:4px 0 0 0;">per year / gas</p>
            </div>
            <div style="font-family:Arial,sans-serif;font-size:48px;color:#666;">&#x2192;</div>
            <div style="text-align:center;">
                <p style="font-family:Arial,sans-serif;font-size:56px;font-weight:900;color:#00d4aa;margin:0;">$0</p>
                <p style="font-family:Arial,sans-serif;font-size:22px;color:#88ffdd;margin:4px 0 0 0;">per year / solar</p>
            </div>
        </div>
    </div>
    <div style="position:absolute;bottom:20px;right:30px;z-index:3;">
        <div style="background:#00d4aa;border-radius:8px;padding:8px 16px;">
            <span style="font-family:Arial,sans-serif;font-size:18px;font-weight:700;color:#0a1628;">S.E.T. Solar</span>
        </div>
    </div>
</div>
"""

noroof_html = """
<div style="width:1280px;height:720px;background:linear-gradient(135deg,#0d1f3c 0%,#1a3a5c 50%,#0a2240 100%);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;">
    <div style="position:absolute;top:0;left:0;width:100%;height:100%;background:radial-gradient(circle at 70% 30%,rgba(255,200,0,0.12),transparent 60%);z-index:1;"></div>
    <div style="z-index:2;text-align:center;padding:40px;">
        <div style="background:rgba(255,200,0,0.2);border:2px solid #ffc800;border-radius:12px;padding:8px 24px;display:inline-block;margin-bottom:20px;">
            <span style="font-family:Arial,sans-serif;font-size:22px;font-weight:700;color:#ffc800;letter-spacing:2px;">2026 GUIDE</span>
        </div>
        <h1 style="font-family:Arial,sans-serif;font-size:68px;font-weight:900;color:#ffffff;margin:0 0 12px 0;line-height:1.1;text-shadow:2px 2px 10px rgba(0,0,0,0.5);">SOLAR GENERATOR<br/>FOR APARTMENTS</h1>
        <p style="font-family:Arial,sans-serif;font-size:38px;font-weight:600;color:#ffc800;margin:0 0 24px 0;">No Roof Needed</p>
        <div style="display:flex;gap:16px;justify-content:center;">
            <div style="background:rgba(255,255,255,0.1);border-radius:8px;padding:10px 18px;">
                <span style="font-family:Arial,sans-serif;font-size:18px;color:#ffffff;">Renter Friendly</span>
            </div>
            <div style="background:rgba(255,255,255,0.1);border-radius:8px;padding:10px 18px;">
                <span style="font-family:Arial,sans-serif;font-size:18px;color:#ffffff;">Portable</span>
            </div>
            <div style="background:rgba(255,255,255,0.1);border-radius:8px;padding:10px 18px;">
                <span style="font-family:Arial,sans-serif;font-size:18px;color:#ffffff;">Blackout Ready</span>
            </div>
        </div>
    </div>
    <div style="position:absolute;bottom:20px;right:30px;z-index:3;">
        <div style="background:#00d4aa;border-radius:8px;padding:8px 16px;">
            <span style="font-family:Arial,sans-serif;font-size:18px;font-weight:700;color:#0a1628;">S.E.T. Solar</span>
        </div>
    </div>
</div>
"""

thumbnails = [
    ("video-thumb-apartment-solar.png", "pm2XoUMW-4M", apartment_html),
    ("video-thumb-gas-vs-solar.png", "5B4RUYWq9v4", gas_vs_solar_html),
    ("video-thumb-apartment-noroof.png", "r2uJQ3UnO3A", noroof_html),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 720})

    for filename, video_id, html in thumbnails:
        page.set_content(html)
        out_path = os.path.join(out_dir, filename)
        page.screenshot(path=out_path, type="png")
        file_size = os.path.getsize(out_path)
        print(f"Created: {filename} ({file_size/1024:.0f} KB) for {video_id}")

    browser.close()

print("\nAll 3 thumbnails rendered.")
