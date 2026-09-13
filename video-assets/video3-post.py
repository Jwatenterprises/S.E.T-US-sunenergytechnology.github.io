"""
Video 3 — Post to YouTube Shorts, TikTok, Facebook Reels
Uses Playwright with Firefox persistent profile (active login sessions)
"""
import sys
import time
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

VIDEO_PATH = str(Path.home() / "OneDrive - Hillsborough County Public Schools" / "SET-Solar-Video3" / "video3-apartment-solar.mp4")
FF_PROFILE = str(Path.home() / "AppData/Roaming/Mozilla/Firefox/Profiles/w5f1cs38.default-release")

YT_TITLE = "Best Solar Generator for Your Apartment #shorts"
YT_DESC = """Living in an apartment? You can't install rooftop solar — but you CAN own a solar generator.

The BLUETTI AC200L packs 2,048Wh into a box that fits under your desk. Charge from a balcony solar panel or wall outlet. Runs your fridge, laptop, phone, and fan during a blackout.

No gas. No fumes. No landlord permission needed.

🔋 Compare generators in 5 minutes: https://sunenergytechnology.com
📖 Full AC200L review: https://sunenergytechnology.com/blog/bluetti-ac200l-review.html

#solarpower #apartmentliving #solargenerator #blackout #emergencypower #BLUETTI #AC200L #portablepower"""

TT_CAPTION = """Living in an apartment? You can't put panels on the roof — but you CAN own a solar generator. 🔋

BLUETTI AC200L: 2,048Wh, fits under your desk, charges from a balcony panel or wall outlet.

No gas. No fumes. No landlord permission.

Under $2,000 for apartment-proof backup power ⚡

🔗 Link in bio — find your perfect generator in 5 minutes

#solargenerator #apartmentliving #BLUETTI #AC200L #portablepower #blackout #emergencyprep #renterlife #solarpanel #offgrid #prepper #sustainability"""

FB_CAPTION = """🔋 Best Solar Generator for Your Apartment

Can't install rooftop solar? No problem.

The BLUETTI AC200L packs 2,048Wh of backup power into a box that fits under your desk:
✅ Charge from a balcony solar panel or wall outlet
✅ Runs fridge, laptop, phone & fan during a blackout
✅ No gas, no fumes, no landlord permission needed
✅ Under $2,000

Compare portable solar generators in 5 minutes → https://sunenergytechnology.com

#SolarGenerator #ApartmentLiving #BLUETTI #BackupPower #EmergencyPrep #PortablePower"""


def upload_youtube(page, context):
    """Upload to YouTube Studio as a Short"""
    print("\n=== YOUTUBE SHORTS ===")
    page.goto("https://studio.youtube.com")
    time.sleep(4)

    print(f"Page title: {page.title()}")
    page.screenshot(path=str(Path.home() / "Documents/SunEnergyTechnology/video-assets/yt-studio-landing.png"))
    print("Screenshot saved: yt-studio-landing.png")

    try:
        create_btn = page.locator("#create-icon, button[aria-label='Create'], ytcp-button#create-icon").first
        create_btn.wait_for(timeout=10000)
        create_btn.click()
        time.sleep(2)

        upload_option = page.locator("text=Upload videos, tp-yt-paper-item:has-text('Upload')").first
        upload_option.wait_for(timeout=5000)
        upload_option.click()
        time.sleep(2)
    except Exception as e:
        print(f"Trying direct upload URL... ({e})")
        page.goto("https://studio.youtube.com/channel/upload")
        time.sleep(4)

    page.screenshot(path=str(Path.home() / "Documents/SunEnergyTechnology/video-assets/yt-upload-dialog.png"))
    print("Screenshot saved: yt-upload-dialog.png")

    try:
        file_input = page.locator("input[type='file']").first
        file_input.set_input_files(VIDEO_PATH)
        print(f"Video file selected: {VIDEO_PATH}")
        time.sleep(8)

        page.screenshot(path=str(Path.home() / "Documents/SunEnergyTechnology/video-assets/yt-after-upload.png"))
        print("Screenshot saved: yt-after-upload.png")

        title_input = page.locator("#textbox[aria-label*='title'], textbox#title-textarea, div[id='textbox'][aria-label*='Add a title']").first
        title_input.wait_for(timeout=10000)
        title_input.click()
        title_input.fill("")
        time.sleep(0.5)
        title_input.type(YT_TITLE, delay=20)
        time.sleep(1)

        desc_input = page.locator("#textbox[aria-label*='description'], div[id='textbox'][aria-label*='Tell viewers']").first
        desc_input.click()
        desc_input.type(YT_DESC, delay=10)
        time.sleep(1)

        not_for_kids = page.locator("tp-yt-paper-radio-button[name='NOT_MADE_FOR_KIDS'], #radioLabel:has-text('not made for kids')").first
        not_for_kids.click()
        time.sleep(1)

        page.screenshot(path=str(Path.home() / "Documents/SunEnergyTechnology/video-assets/yt-details-filled.png"))
        print("Screenshot: yt-details-filled.png — Details filled, ready for review")
        print("YouTube upload staged. Check screenshots before publishing.")
        return True

    except Exception as e:
        print(f"YouTube upload error: {e}")
        page.screenshot(path=str(Path.home() / "Documents/SunEnergyTechnology/video-assets/yt-error.png"))
        return False


def upload_tiktok(page, context):
    """Upload to TikTok Creator Center"""
    print("\n=== TIKTOK ===")
    page.goto("https://www.tiktok.com/creator#/upload?scene=creator_center")
    time.sleep(5)

    page.screenshot(path=str(Path.home() / "Documents/SunEnergyTechnology/video-assets/tt-landing.png"))
    print(f"Page title: {page.title()}")
    print("Screenshot saved: tt-landing.png")

    try:
        file_input = page.locator("input[type='file'][accept*='video']").first
        file_input.set_input_files(VIDEO_PATH)
        print(f"Video file selected: {VIDEO_PATH}")
        time.sleep(10)

        page.screenshot(path=str(Path.home() / "Documents/SunEnergyTechnology/video-assets/tt-after-upload.png"))
        print("Screenshot saved: tt-after-upload.png")

        caption_area = page.locator("div[contenteditable='true'], .public-DraftEditor-content, div[data-contents='true']").first
        caption_area.wait_for(timeout=10000)
        caption_area.click()
        time.sleep(0.5)

        page.keyboard.press("Control+a")
        time.sleep(0.3)
        page.keyboard.type(TT_CAPTION, delay=10)
        time.sleep(2)

        page.screenshot(path=str(Path.home() / "Documents/SunEnergyTechnology/video-assets/tt-caption-filled.png"))
        print("Screenshot: tt-caption-filled.png — Caption filled, ready for review")
        print("TikTok upload staged. Check screenshots before publishing.")
        return True

    except Exception as e:
        print(f"TikTok upload error: {e}")
        page.screenshot(path=str(Path.home() / "Documents/SunEnergyTechnology/video-assets/tt-error.png"))
        return False


def upload_facebook(page, context):
    """Upload to Facebook as a Reel on Sun Energy Technology page"""
    print("\n=== FACEBOOK REEL ===")
    page.goto("https://www.facebook.com/profile.php?id=61567645495673")
    time.sleep(5)

    page.screenshot(path=str(Path.home() / "Documents/SunEnergyTechnology/video-assets/fb-page-landing.png"))
    print(f"Page title: {page.title()}")
    print("Screenshot saved: fb-page-landing.png")

    try:
        reel_btn = page.locator("text=Reel, span:has-text('Reel'), div[aria-label*='Reel']").first
        reel_btn.wait_for(timeout=8000)
        reel_btn.click()
        time.sleep(4)
    except Exception:
        print("Trying Meta Business Suite for reel upload...")
        page.goto("https://business.facebook.com/latest/content_calendar")
        time.sleep(5)

    page.screenshot(path=str(Path.home() / "Documents/SunEnergyTechnology/video-assets/fb-reel-upload.png"))
    print("Screenshot saved: fb-reel-upload.png")
    print("Facebook page opened. Manual upload may be needed — check screenshot.")
    return True


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    print(f"Video path: {VIDEO_PATH}")
    print(f"File exists: {os.path.exists(VIDEO_PATH)}")
    print(f"Target: {target}")

    with sync_playwright() as p:
        context = p.firefox.launch_persistent_context(
            FF_PROFILE,
            headless=False,
            viewport={"width": 1920, "height": 1080},
            args=["--start-maximized"],
        )
        page = context.new_page()

        results = {}
        if target in ("youtube", "yt", "all"):
            results["youtube"] = upload_youtube(page, context)

        if target in ("tiktok", "tt", "all"):
            if "youtube" in results:
                page = context.new_page()
            results["tiktok"] = upload_tiktok(page, context)

        if target in ("facebook", "fb", "all"):
            if results:
                page = context.new_page()
            results["facebook"] = upload_facebook(page, context)

        print("\n=== RESULTS ===")
        for platform, ok in results.items():
            print(f"  {platform}: {'STAGED' if ok else 'NEEDS MANUAL'}")

        print("\nBrowser stays open for review. Close manually when done.")
        input("Press Enter to close browser...")
        context.close()


if __name__ == "__main__":
    main()
