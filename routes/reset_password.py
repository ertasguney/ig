from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
import requests
import time
import json

router = APIRouter()

class ResetPasswordRequest(BaseModel):
    username: str

def random_id(prefix="android-"):
    return prefix + uuid.uuid4().hex[:16]

def gen_headers():
    return {
        "host": "i.instagram.com",
        "x-ig-app-locale": "en_OM",
        "x-ig-device-locale": "en_OM",
        "x-ig-mapped-locale": "en_AR",
        "x-pigeon-session-id": f"UFS-{uuid.uuid4()}-1",
        "x-pigeon-rawclienttime": str(time.time()),
        "x-ig-bandwidth-speed-kbps": f"{random.randint(300, 1000):.3f}",
        "x-ig-bandwidth-totalbytes-b": str(random.randint(1_000_000, 5_000_000)),
        "x-ig-bandwidth-totaltime-ms": str(random.randint(3000, 10000)),
        "x-bloks-version-id": "8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb",
        "x-ig-www-claim": "0",
        "x-bloks-is-layout-rtl": "true",
        "x-ig-device-id": str(uuid.uuid4()),
        "x-ig-family-device-id": str(uuid.uuid4()),
        "x-ig-android-id": random_id(),
        "x-ig-timezone-offset": "14400",
        "x-fb-connection-type": "WIFI",
        "x-ig-connection-type": "WIFI",
        "x-ig-capabilities": "3brTv10=",
        "x-ig-app-id": "567067343352427",
        "priority": "u=3",
        "user-agent": "Instagram 275.0.0.27.98 Android (29/10; 443dpi; 1080x2224; HUAWEI; STK-L21; HWSTK-HF; kirin710; ar_OM; 458229237)",
        "accept-language": "en-OM, en-US",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "accept-encoding": "zstd, gzip, deflate",
        "x-fb-http-engine": "Liger",
        "ig-intended-user-id": "0",
    }

@router.post("/reset_password")
def reset_password(data: ResetPasswordRequest):
    if not data.username:
        raise HTTPException(status_code=400, detail="Missing username")

    body_json = {
        "adid": str(uuid.uuid4()),
        "guid": str(uuid.uuid4()),
        "device_id": random_id(),
        "query": data.username,
        "waterfall_id": str(uuid.uuid4())
    }
    signed_body = "SIGNATURE." + json.dumps(body_json, separators=(",", ":"))
    payload = {"signed_body": signed_body}
    headers = gen_headers()

    try:
        r = requests.post("https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/", headers=headers, data=payload)
        return {
            "status_code": r.status_code,
            "response": r.text.replace('\\', '')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
