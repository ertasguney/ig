from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import base64
import random
import requests
import re

router = APIRouter()

class ConvertSessionRequest(BaseModel):
    sessionid: str

class ConvertSessionViaMidRequest(BaseModel):
    sessionid: str
    mid: str

@router.post("/web_to_api")
def convert_session_web_to_api(data: ConvertSessionRequest):
    sessionID = data.sessionid
    try:
        auth_payload = '{"ds_user_id":"' + sessionID.split("%3A")[0] + '","sessionid":"' + sessionID + '"}'
        encoded_auth = base64.b64encode(auth_payload.encode('utf-8')).decode('utf-8')

        headers = {
            "User-Agent": "Instagram 365.0.0.14.102 Android (28/9; 300dpi; 1600x900; samsung; SM-N975F; SM-N975F; intel; en_US; 373310563)",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": f"sessionid={sessionID}",
            "X-Bloks-Version-Id": "8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb",
            "X-Bloks-Is-Layout-Rtl": "false",
        }

        req = requests.get("https://i.instagram.com/api/v1/accounts/current_user/?edit=true", headers=headers, cookies={"sessionid": sessionID})
        r = req.json()
        mid = req.headers.get("ig-set-x-mid")
        user = r["user"]["username"]
        
        data_post = {
            'device_id': f"android-{''.join(random.choice('1234567890') for _ in range(10))}",
            'authorization_token': f"Bearer IGT:2:{encoded_auth}"
        }
        headers["X-Mid"] = mid
        req_post = requests.post("https://i.instagram.com/api/v1/accounts/continue_as_instagram_login/", headers=headers, data=data_post)

        if "logged" in req_post.text:
            sess = req_post.cookies.get("sessionid")
            if not sess:
                after = base64.b64decode(req_post.headers.get('ig-set-authorization').split(":")[2]).decode('utf-8')
                sess = re.search('"sessionid":"(.*?)"', after).group(1)
            return {
                "status": "success",
                "username": user,
                "mid": mid,
                "sessionid_api": sess
            }
        else:
            raise HTTPException(status_code=400, detail="Conversion failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/web_to_api_via_mid")
def convert_session_web_to_api_via_mid(data: ConvertSessionViaMidRequest):
    sessionID = data.sessionid
    mid = data.mid
    try:
        auth_payload = '{"ds_user_id":"' + sessionID.split("%3A")[0] + '","sessionid":"' + sessionID + '"}'
        encoded_auth = base64.b64encode(auth_payload.encode('utf-8')).decode('utf-8')

        headers = {
            "User-Agent": "Instagram 237.0.0.14.102 Android",
            "X-Mid": mid,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": f"sessionid={sessionID}",
            "X-Bloks-Version-Id": "8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb",
            "X-Bloks-Is-Layout-Rtl": "false",
        }

        data_post = {
            'device_id': f"android-{''.join(random.choice('1234567890') for _ in range(10))}",
            'authorization_token': f"Bearer IGT:2:{encoded_auth}"
        }

        req = requests.post("https://i.instagram.com/api/v1/accounts/continue_as_instagram_login/", headers=headers, data=data_post)
        if "logged" in req.text:
            sess = req.cookies.get("sessionid")
            if not sess:
                auth_header = req.headers.get('ig-set-authorization')
                if auth_header:
                    after = base64.b64decode(auth_header.split(":")[2]).decode('utf-8')
                    sess_match = re.search('"sessionid":"(.*?)"', after)
                    if sess_match:
                        sess = sess_match.group(1)
                    else:
                        raise HTTPException(status_code=500, detail="No sessionid found in decoded response")
                else:
                    raise HTTPException(status_code=500, detail="Missing ig-set-authorization header")
            return {
                "status": "success",
                "sessionid_api": sess
            }
        else:
            raise HTTPException(status_code=400, detail="Login failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
