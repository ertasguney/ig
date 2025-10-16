from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import base64
import uuid
import random
import time

router = APIRouter()

class ResetLinkRequest(BaseModel):
    reset_link: str

def generate_random_android_id():
    return f"android-{''.join(random.choices('0123456789abcdef', k=16))}"

def generate_random_device_id():
    return str(uuid.uuid4())

def generate_random_user_agent():
    android_versions = ["28/9", "29/10", "30/11", "31/12"]
    dpi_options = ["240dpi", "320dpi", "480dpi"]
    resolutions = ["720x1280", "1080x1920", "1440x2560"]
    brands = ["samsung", "xiaomi", "huawei", "oneplus", "google"]
    models = ["SM-G975F", "Mi-9T", "P30-Pro", "ONEPLUS-A6003", "Pixel-4"]
    version = random.choice(android_versions)
    dpi = random.choice(dpi_options)
    resolution = random.choice(resolutions)
    brand = random.choice(brands)
    model = random.choice(models)
    code = random.randint(100000000, 999999999)
    return f"Instagram 394.0.0.46.81 Android ({version}; {dpi}; {resolution}; {brand}; {model}; {model}; intel; en_US; {code})"

USER_AGENT = generate_random_user_agent()

def generate_password():
    timestamp = int(time.time())
    nums = ''.join([str(random.randint(1, 100)) for _ in range(10)])
    password = f"suul@{nums}"
    return f"#PWD_INSTAGRAM:0:{timestamp}:{password}"

def generate_headers(mid):
    return {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Bloks-Version-Id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
        "X-Mid": mid,
        "User-Agent": USER_AGENT,
        "Content-Length": "9481"
    }

@router.post("/reset_link")
def reset_link(data: ResetLinkRequest):
    try:
        link = data.reset_link
        uidb36 = link.split("uidb36=")[1].split("&token=")[0]
        token = link.split("token=")[1].split(":")[0]

        ANDROID_ID = generate_random_android_id()
        WATERFALL_ID = generate_random_device_id()

        url = "https://i.instagram.com/api/v1/accounts/password_reset/"
        post_data = {"source": "one_click_login_email", "uidb36": uidb36, "device_id": ANDROID_ID, "token": token, "waterfall_id": WATERFALL_ID}
        headers = generate_headers("")

        response = requests.post(url, headers=headers, data=post_data)
        ig_set_x_mid = response.headers.get("Ig-Set-X-Mid")
        json_response = response.json()
        json_response["X-Mid"] = ig_set_x_mid

        if 'user_id' not in response.text:
            raise HTTPException(status_code=400, detail="Invalid reset link")

        # Après obtention de la donnée, appel à post2 et changement de mot de passe analogues
        # Pour simplifier la démo, on retourne json_response complet
        return {"status": "success", "data": json_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
