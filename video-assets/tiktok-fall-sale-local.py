"""
TikTok: ALLPOWERS Fall Sale — Price Shock (30s, 9:16)
Local render using Pillow + ffmpeg. No API credits needed.
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

W, H = 1080, 1920
FPS = 30
DURATION = 30  # seconds
TOTAL_FRAMES = FPS * DURATION

OUT_DIR = Path(__file__).parent / "tiktok-fall-frames"
EXPORT_DIR = Path(os.environ.get("USERPROFILE", "~")) / "OneDrive" / "video-assets" / "exports"
IMG_DIR = Path(__file__).parent.parent / "images"
LOGO_PATH = Path(__file__).parent.parent / "set-logo.jpg"

# Colors
BG_DARK = (10, 10, 26)
BG_GRAD_MID = (26, 26, 62)
BG_GRAD_BOT = (45, 27, 0)
WHITE = (255, 255, 255)
WHITE_70 = (255, 255, 255, 178)
MUTED = (153, 153, 153)
RED = (255, 68, 68)
ORANGE = (217, 119, 6)
GREEN = (0, 200, 150)
CHARCOAL = (30, 30, 46)


def get_font(size, bold=False):
    """Get a font, falling back to default if needed."""
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]
    for f in candidates:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def gradient_bg():
    """Create a dark gradient background image."""
    img = Image.new("RGBA", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        if ratio < 0.5:
            r = int(BG_DARK[0] + (BG_GRAD_MID[0] - BG_DARK[0]) * (ratio * 2))
            g = int(BG_DARK[1] + (BG_GRAD_MID[1] - BG_DARK[1]) * (ratio * 2))
            b = int(BG_DARK[2] + (BG_GRAD_MID[2] - BG_DARK[2]) * (ratio * 2))
        else:
            r2 = (ratio - 0.5) * 2
            r = int(BG_GRAD_MID[0] + (BG_GRAD_BOT[0] - BG_GRAD_MID[0]) * r2)
            g = int(BG_GRAD_MID[1] + (BG_GRAD_BOT[1] - BG_GRAD_MID[1]) * r2)
            b = int(BG_GRAD_MID[2] + (BG_GRAD_BOT[2] - BG_GRAD_MID[2]) * r2)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return img


def center_text(draw, text, y, font, fill=WHITE, anchor="mt"):
    """Draw centered text at y position."""
    bbox = draw.textbbox((W // 2, y), text, font=font, anchor=anchor)
    # Shadow
    draw.text((W // 2 + 2, y + 2), text, font=font, fill=(0, 0, 0, 128), anchor=anchor)
    draw.text((W // 2, y), text, font=font, fill=fill, anchor=anchor)
    return bbox[3]  # bottom y


def draw_price_block(draw, y, old_price, new_price, save_pct):
    """Draw strikethrough old price → new price + save badge."""
    font_old = get_font(48)
    font_arrow = get_font(24)
    font_new = get_font(72, bold=True)
    font_badge = get_font(32, bold=True)

    # Measure widths for centering
    old_w = draw.textlength(f"${old_price}", font=font_old)
    arrow_w = draw.textlength(" → ", font=font_arrow)
    new_w = draw.textlength(f"${new_price}", font=font_new)
    total_w = old_w + arrow_w + new_w

    x_start = (W - total_w) / 2

    # Old price with strikethrough
    draw.text((x_start, y), f"${old_price}", font=font_old, fill=MUTED)
    old_bbox = draw.textbbox((x_start, y), f"${old_price}", font=font_old)
    strike_y = (old_bbox[1] + old_bbox[3]) // 2
    draw.line([(old_bbox[0] - 4, strike_y), (old_bbox[2] + 4, strike_y)], fill=MUTED, width=3)

    # Arrow
    draw.text((x_start + old_w, y + 15), " → ", font=font_arrow, fill=MUTED)

    # New price
    draw.text((x_start + old_w + arrow_w, y - 10), f"${new_price}", font=font_new, fill=RED)

    # Save badge
    badge_text = f"{save_pct}% OFF"
    badge_w = draw.textlength(badge_text, font=font_badge) + 40
    badge_h = 50
    badge_x = (W - badge_w) / 2
    badge_y = y + 85
    draw.rounded_rectangle(
        [(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)],
        radius=10, fill=ORANGE
    )
    draw.text((W // 2, badge_y + badge_h // 2), badge_text, font=font_badge, fill=WHITE, anchor="mm")

    return badge_y + badge_h + 20


def draw_code_block(draw, y, code):
    """Draw a coupon code display box."""
    font_label = get_font(20)
    font_code = get_font(48, bold=True)

    box_w = 400
    box_h = 100
    box_x = (W - box_w) / 2

    # Box background
    draw.rounded_rectangle(
        [(box_x, y), (box_x + box_w, y + box_h)],
        radius=14, fill=CHARCOAL, outline=GREEN, width=3
    )

    # Label
    draw.text((W // 2, y + 18), "USE CODE", font=font_label, fill=MUTED, anchor="mt")
    # Code
    draw.text((W // 2, y + 60), code, font=font_code, fill=GREEN, anchor="mt")

    return y + box_h + 20


def add_logo(img):
    """Add S.E.T. logo watermark to top-right."""
    if not LOGO_PATH.exists():
        return img
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo_size = 80
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    # Make semi-transparent
    alpha = logo.split()[3]
    alpha = alpha.point(lambda x: int(x * 0.7))
    logo.putalpha(alpha)
    img.paste(logo, (W - logo_size - 40, 40), logo)
    return img


def add_product_image(img, product_path, y_center=700, max_h=500, opacity=1.0):
    """Overlay a product image prominently."""
    if not product_path or not Path(product_path).exists():
        return img
    prod = Image.open(product_path).convert("RGBA")
    # Scale larger — fill most of the width
    ratio = min(W * 0.85 / prod.width, max_h / prod.height)
    new_w = int(prod.width * ratio)
    new_h = int(prod.height * ratio)
    prod = prod.resize((new_w, new_h), Image.LANCZOS)
    # Apply opacity (now full by default)
    if opacity < 1.0:
        alpha = prod.split()[3]
        alpha = alpha.point(lambda x: int(x * opacity))
        prod.putalpha(alpha)
    # Add a subtle glow/backdrop behind the product
    backdrop = Image.new("RGBA", (new_w + 40, new_h + 40), (0, 0, 0, 0))
    bd_draw = ImageDraw.Draw(backdrop)
    bd_draw.rounded_rectangle(
        [(0, 0), (new_w + 39, new_h + 39)],
        radius=20, fill=(20, 20, 40, 180)
    )
    x = (W - new_w) // 2
    y = y_center - new_h // 2
    img.paste(backdrop, (x - 20, y - 20), backdrop)
    img.paste(prod, (x, y), prod)
    return img


# ═══════════════════════════════════════
# SLIDE DEFINITIONS
# ═══════════════════════════════════════

def slide_hook(frame_num):
    """Slide 1 (0-5s): Price shock hook — P1800 $1,060 → $439"""
    img = gradient_bg()
    img = add_product_image(img, IMG_DIR / "allpowers-p1800.webp", y_center=700, max_h=450, opacity=1.0)
    draw = ImageDraw.Draw(img)

    font_big = get_font(52, bold=True)
    font_sub = get_font(36)

    y = center_text(draw, "This solar generator", 280, font_big)
    y = center_text(draw, "was $1,060", y + 20, font_big, fill=MUTED)
    center_text(draw, "Right now it's", y + 40, font_sub, fill=WHITE_70)

    draw_price_block(draw, 1150, "1,060", "439", 59)

    img = add_logo(img)
    return img


def slide_r2500(frame_num):
    """Slide 2 (5-11s): R2500 V2 — $1,599 → $659"""
    img = gradient_bg()
    img = add_product_image(img, IMG_DIR / "allpowers-r2400.webp", y_center=700, max_h=450, opacity=1.0)
    draw = ImageDraw.Draw(img)

    font_title = get_font(56, bold=True)
    font_sub = get_font(32)

    center_text(draw, "ALLPOWERS R2500 V2", 280, font_title)
    center_text(draw, "1,920Wh · 2,500W Output", 360, font_sub, fill=WHITE_70)

    draw_price_block(draw, 1150, "1,599", "659", 59)

    img = add_logo(img)
    return img


def slide_panel(frame_num):
    """Slide 3 (11-16s): SE100 panel — $199 → $69.99"""
    img = gradient_bg()
    img = add_product_image(img, IMG_DIR / "allpowers-r600.webp", y_center=700, max_h=400, opacity=1.0)
    draw = ImageDraw.Draw(img)

    font_title = get_font(56, bold=True)
    font_sub = get_font(34)

    center_text(draw, "100W Solar Panel", 300, font_title)
    center_text(draw, "Cheapest from any", 380, font_sub, fill=WHITE_70)
    center_text(draw, "real brand in 2026", 425, font_sub, fill=WHITE_70)

    draw_price_block(draw, 1150, "199", "69.99", 65)

    img = add_logo(img)
    return img


def slide_s2000(frame_num):
    """Slide 4 (16-21s): S2000 Pro — $1,399 → $549"""
    img = gradient_bg()
    img = add_product_image(img, IMG_DIR / "allpowers-r3500.webp", y_center=700, max_h=450, opacity=1.0)
    draw = ImageDraw.Draw(img)

    font_title = get_font(56, bold=True)
    font_sub = get_font(32)

    center_text(draw, "ALLPOWERS S2000 Pro", 300, font_title)
    center_text(draw, "1,500Wh · 2,000W Output", 380, font_sub, fill=WHITE_70)

    draw_price_block(draw, 1150, "1,399", "549", 61)

    img = add_logo(img)
    return img


def slide_codes(frame_num):
    """Slide 5 (21-25s): Coupon codes"""
    img = gradient_bg()
    draw = ImageDraw.Draw(img)

    font_title = get_font(48, bold=True)
    font_sub = get_font(28)

    center_text(draw, "Extra Codes Stack", 400, font_title)
    center_text(draw, "On Top of Sale Prices", 465, font_sub, fill=WHITE_70)

    draw_code_block(draw, 700, "APSEP10")
    center_text(draw, "10% off storewide", 830, font_sub, fill=WHITE_70)

    draw_code_block(draw, 920, "APSEP110")
    center_text(draw, "$110 off orders over $1,000", 1050, font_sub, fill=WHITE_70)

    img = add_logo(img)
    return img


def slide_cta(frame_num):
    """Slide 6 (25-30s): CTA — Sale ends Sep 30"""
    img = gradient_bg()
    draw = ImageDraw.Draw(img)

    font_big = get_font(52, bold=True)
    font_sub = get_font(34)
    font_cta = get_font(40, bold=True)
    font_sm = get_font(24)

    center_text(draw, "Sale Ends Sep 30", 450, font_big)

    # Leaf emoji substitute — simple text
    center_text(draw, "ALLPOWERS Fall Power Sale", 530, font_sub, fill=ORANGE)
    center_text(draw, "Up to 65% OFF", 585, font_sub, fill=WHITE_70)

    # "Every deal ranked" box
    box_w = 500
    box_h = 70
    box_x = (W - box_w) // 2
    box_y = 750
    draw.rounded_rectangle(
        [(box_x, box_y), (box_x + box_w, box_y + box_h)],
        radius=12, fill=ORANGE
    )
    draw.text((W // 2, box_y + box_h // 2), "Link in bio", font=font_cta, fill=WHITE, anchor="mm")

    center_text(draw, "sunenergytechnology.com", 900, font_sm, fill=MUTED)

    img = add_logo(img)
    return img


# ═══════════════════════════════════════
# RENDER
# ═══════════════════════════════════════

SLIDES = [
    (0, 5, slide_hook),
    (5, 11, slide_r2500),
    (11, 16, slide_panel),
    (16, 21, slide_s2000),
    (21, 25, slide_codes),
    (25, 30, slide_cta),
]


def render_frames():
    """Generate all frames as PNG files."""
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    print(f"Rendering {TOTAL_FRAMES} frames to {OUT_DIR}...")

    # Pre-render each slide (they're static per slide)
    slide_images = {}
    for start_s, end_s, render_fn in SLIDES:
        img = render_fn(0)
        slide_images[(start_s, end_s)] = img.convert("RGB")
        print(f"  Slide {start_s}-{end_s}s rendered")

    # Write frames
    for f in range(TOTAL_FRAMES):
        t = f / FPS
        # Find which slide this frame belongs to
        for start_s, end_s, _ in SLIDES:
            if start_s <= t < end_s:
                slide_img = slide_images[(start_s, end_s)]
                break
        else:
            slide_img = slide_images[(25, 30)]  # fallback to last slide

        frame_path = OUT_DIR / f"frame_{f:05d}.png"
        slide_img.save(frame_path, "PNG")

        if f % (FPS * 5) == 0:
            print(f"  Frame {f}/{TOTAL_FRAMES} ({t:.0f}s)")

    print(f"  All {TOTAL_FRAMES} frames saved.")


def encode_video():
    """Encode frames to MP4 with audio using ffmpeg."""
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    output = EXPORT_DIR / "tiktok-allpowers-fall-sale.mp4"
    audio_file = Path(__file__).parent / "fall-sale-beat2.wav"

    print(f"\nEncoding video to {output}...")

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(OUT_DIR / "frame_%05d.png"),
    ]

    # Add audio if the beat file exists
    if audio_file.exists():
        cmd += ["-i", str(audio_file)]
        print(f"  Adding audio: {audio_file.name}")

    cmd += [
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "18",
    ]

    if audio_file.exists():
        cmd += [
            "-c:a", "aac",
            "-b:a", "128k",
            "-shortest",
        ]

    cmd += [
        "-movflags", "+faststart",
        str(output),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg error: {result.stderr[-500:]}")
        return None

    size_mb = output.stat().st_size / (1024 * 1024)
    print(f"Video saved: {output} ({size_mb:.1f} MB)")
    return output


def cleanup():
    """Remove temp frame directory."""
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
        print("Cleaned up temp frames.")


if __name__ == "__main__":
    render_frames()
    output = encode_video()
    cleanup()

    if output:
        print(f"\n{'='*60}")
        print(f"DONE: {output}")
        print(f"{'='*60}")
        print(f"\nCaption for TikTok @setuslove:")
        print(f"This $1,060 solar generator is $439 right now 🍂 ALLPOWERS Fall Sale — up to 65% OFF through Sep 30. Codes APSEP10 (10% off) and APSEP110 ($110 off $1K+) stack on top. Every deal ranked → link in bio")
        print(f"\n#solargenerator #allpowers #fallsale #solarpower #offgrid #powerstation #hurricane #prepper #solarpanel #solar")
