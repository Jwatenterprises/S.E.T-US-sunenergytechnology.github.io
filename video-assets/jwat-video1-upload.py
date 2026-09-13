import os
import sys
import json
import pickle

sys.stdout.reconfigure(encoding='utf-8')

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN_PATH = os.path.expanduser("~/.kiyomimax/youtube_token.json")
CLIENT_PATH = os.path.expanduser("~/.kiyomimax/yt_oauth_client.json")

VIDEO_PATH = os.path.join(os.path.dirname(__file__), "exports", "jwat-missed-calls-ai.mp4")
THUMB_PATH = os.path.join(os.path.dirname(__file__), "jwat-thumbnail-missed-calls.png")

TITLE = "Is Your Business Losing Customers While You Sleep? | AI Phone Answering"
DESCRIPTION = """63% of missed calls never call back. What if AI answered every call for your business?

AI phone answering — FREE TRIAL, then just $24.95/month. No salary, no sick days, no missed customers.

JWAT Enterprise Inc — AI-Powered Business Consulting
Visit: https://jwatenterprisesinc.com

#SmallBusiness #AIPhone #BusinessAutomation #MissedCalls #Entrepreneur #JWAT"""

TAGS = [
    "AI phone answering",
    "missed calls business",
    "small business automation",
    "AI receptionist",
    "business consulting",
    "JWAT Enterprise",
    "entrepreneur tips",
    "Upfirst AI",
    "virtual receptionist",
    "business growth",
]

CATEGORY_ID = "22"  # People & Blogs

def get_youtube_service():
    with open(TOKEN_PATH, "r") as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data["token"],
        refresh_token=token_data["refresh_token"],
        token_uri=token_data["token_uri"],
        client_id=token_data["client_id"],
        client_secret=token_data["client_secret"],
        scopes=token_data["scopes"],
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_data["token"] = creds.token
        with open(TOKEN_PATH, "w") as f:
            json.dump(token_data, f, indent=2)
        print("Token refreshed.")

    return build("youtube", "v3", credentials=creds)

def upload_video(youtube):
    if not os.path.exists(VIDEO_PATH):
        print(f"ERROR: Video file not found: {VIDEO_PATH}")
        sys.exit(1)

    size_mb = os.path.getsize(VIDEO_PATH) / 1024 / 1024
    print(f"Video file: {VIDEO_PATH} ({size_mb:.1f} MB)")

    body = {
        "snippet": {
            "title": TITLE,
            "description": DESCRIPTION,
            "tags": TAGS,
            "categoryId": CATEGORY_ID,
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(VIDEO_PATH, mimetype="video/mp4", resumable=True)

    print("Uploading video...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  Upload progress: {int(status.progress() * 100)}%")

    video_id = response["id"]
    print(f"\nUpload complete! Video ID: {video_id}")
    print(f"URL: https://youtube.com/shorts/{video_id}")
    return video_id

def set_thumbnail(youtube, video_id):
    if not os.path.exists(THUMB_PATH):
        print(f"WARNING: Thumbnail file not found: {THUMB_PATH}")
        return

    print(f"\nUploading thumbnail: {THUMB_PATH}")
    media = MediaFileUpload(THUMB_PATH, mimetype="image/png")

    try:
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=media,
        ).execute()
        print("Thumbnail set successfully!")
    except Exception as e:
        print(f"Thumbnail upload failed (may need verified account): {e}")

if __name__ == "__main__":
    youtube = get_youtube_service()
    video_id = upload_video(youtube)
    set_thumbnail(youtube, video_id)
    print(f"\nDone! Video live at: https://youtube.com/shorts/{video_id}")
