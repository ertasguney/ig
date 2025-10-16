from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests

router = APIRouter()

class SessionID(BaseModel):
    sessionid: str

@router.post("/accept")
def accept_terms(data: SessionID):
    headers = {
        "accept": "/",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-length": "76",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": f'sessionid={data.sessionid}',
        "origin": "https://www.instagram.com",
        "referer": "https://www.instagram.com/terms/unblock/?next=/api/v1/web/fxcal/ig_sso_users/",
        "sec-ch-prefers-color-scheme": "light",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "viewport-width": "453",
        "x-asbd-id": "198387",
        "x-csrftoken": "m2kPFuLMBSGix4E8ZbRdIDyh0parUk5r",
        "x-ig-app-id": "936619743392459",
        "x-ig-www-claim": "hmac.AR2BpT3Q3cBoHtz_yRH8EvKCYkOb7loHvR4Jah_iP8s8BmTf",
        "x-instagram-ajax": "9080db6b6a51",
        "x-requested-with": "XMLHttpRequest",
    }

    data1 = "updates=%7B%22existing_user_intro_state%22%3A2%7D&current_screen_key=qp_intro"
    data2 = "updates=%7B%22tos_data_policy_consent_state%22%3A2%7D&current_screen_key=tos"

    resp1 = requests.post("https://www.instagram.com/web/consent/update/", headers=headers, data=data1)
    resp2 = requests.post("https://www.instagram.com/web/consent/update/", headers=headers, data=data2)

    if '{"status":"ok"}' in resp1.text or '{"status":"ok"}' in resp2.text:
        return {"status": "ok", "message": "Terms accepted"}
    else:
        raise HTTPException(status_code=400, detail="Failed to accept terms")
