from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import time
from io import BytesIO

router = APIRouter()

class SessionID(BaseModel):
    sessionid: str

def generate_random_csrf():
    import random, string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return {"profile_pic": ("profile.jpg", BytesIO(response.content), "image/jpeg")}
    except:
        return None

def change_profile_picture(sessionid, url_img):
    url = 'https://www.instagram.com/accounts/web_change_profile_picture/'
    csrf_token = generate_random_csrf()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/edit/",
        "X-CSRFToken": csrf_token,
        "Cookie": f"sessionid={sessionid}; csrftoken={csrf_token};"
    }
    files = download_image(url_img)
    if files is None:
        return False
    try:
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200 and response.json().get("status") == "ok":
            return True
        else:
            return False
    except:
        return False

@router.post("/remove_former_users")
def remove_former_users(data: SessionID):
    pfp_urls = [
        'https://i.pinimg.com/550x/35/3f/c5/353fc517a4f4fac8d9ecfc734818e048.jpg',
        'https://i.pinimg.com/236x/c1/43/43/c1434392c4c11ac42b782e9397eb2b58.jpg',
        'https://i.pinimg.com/originals/0f/42/27/0f42279ce48796e63c920ba9aa0295a2.jpg',
        'https://i.pinimg.com/236x/bf/8d/0d/bf8d0d9df86c121ad4e9ed65b4bb92cb.jpg'
    ]
    sessionid = data.sessionid
    total_changes = 0
    errors = 0
    MAX_CHANGES = 20  # Pour limiter la boucle

    for url in pfp_urls * (MAX_CHANGES // len(pfp_urls)):
        success = change_profile_picture(sessionid, url)
        if success:
            total_changes += 1
        else:
            errors += 1
        time.sleep(20)  # Respect des délais Instagram

    return {
        "status": "done",
        "total_changes": total_changes,
        "errors": errors
    }
