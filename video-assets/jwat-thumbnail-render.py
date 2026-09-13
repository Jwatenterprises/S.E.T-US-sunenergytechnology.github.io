import asyncio
from playwright.async_api import async_playwright
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

NAVY = "#1a365d"
GOLD = "#ffd700"
DARK_BG = "#0d1b2a"

THUMBNAIL_HTML = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;width:1280px;height:720px;overflow:hidden;">
<div style="width:1280px;height:720px;background:linear-gradient(135deg,{DARK_BG} 0%,{NAVY} 60%,#2d5a8c 100%);
    display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;">

    <!-- Decorative ring -->
    <div style="position:absolute;top:40px;right:60px;width:120px;height:120px;
        border:4px solid {GOLD};border-radius:50%;opacity:0.3;"></div>
    <div style="position:absolute;bottom:60px;left:40px;width:80px;height:80px;
        border:3px solid {GOLD};border-radius:50%;opacity:0.2;"></div>

    <!-- Phone icon -->
    <div style="font-size:80px;margin-bottom:20px;filter:drop-shadow(0 4px 12px rgba(0,0,0,0.5));">
        <span style="color:{GOLD};">&#128222;</span>
    </div>

    <!-- Main headline -->
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:64px;font-weight:900;
        color:#ffffff;margin:0 0 8px 0;text-align:center;line-height:1.1;
        text-shadow:2px 2px 8px rgba(0,0,0,0.6);padding:0 60px;">
        Is Your Business<br>
        <span style="color:{GOLD};">Losing Customers</span>
    </p>

    <!-- Sub headline -->
    <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:40px;font-weight:400;
        color:rgba(255,255,255,0.85);margin:12px 0 0 0;text-align:center;
        text-shadow:1px 1px 4px rgba(0,0,0,0.5);">
        While You Sleep?
    </p>

    <!-- Stat badge -->
    <div style="display:flex;gap:12px;margin-top:28px;">
        <div style="background:rgba(255,107,107,0.9);border-radius:12px;padding:12px 24px;
            box-shadow:0 4px 16px rgba(0,0,0,0.3);">
            <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:22px;font-weight:700;
                color:#ffffff;margin:0;">63% of missed calls NEVER call back</p>
        </div>
        <div style="background:rgba(74,222,128,0.9);border-radius:12px;padding:12px 24px;
            box-shadow:0 4px 16px rgba(0,0,0,0.3);">
            <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:22px;font-weight:700;
                color:#0d1b2a;margin:0;">FREE TRIAL &bull; $24.95/mo</p>
        </div>
    </div>

    <!-- Brand bar -->
    <div style="position:absolute;bottom:0;left:0;right:0;height:56px;
        background:linear-gradient(90deg,{GOLD} 0%,#f0c800 100%);
        display:flex;align-items:center;justify-content:center;gap:16px;">
        <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:24px;font-weight:900;
            color:{NAVY};margin:0;letter-spacing:2px;">JWAT ENTERPRISE INC</p>
        <span style="color:{NAVY};font-size:20px;">|</span>
        <p style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:18px;font-weight:500;
            color:{NAVY};margin:0;">AI-Powered Business Consulting</p>
    </div>
</div>
</body>
</html>"""

async def render():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "jwat-thumbnail-missed-calls.png")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        await page.set_content(THUMBNAIL_HTML)
        await page.wait_for_timeout(500)
        await page.screenshot(path=out_path)
        await browser.close()

    size_kb = os.path.getsize(out_path) / 1024
    print(f"Thumbnail saved: {out_path}")
    print(f"Size: {size_kb:.0f} KB")

asyncio.run(render())
