from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import base64
import requests

router = APIRouter()

class ChangeBioRequest(BaseModel):
    sessionid: str
    bio_text: str

@router.post("/change_bio")
def change_bio(data: ChangeBioRequest):
    try:
        auth_payload = '{"ds_user_id":"' + data.sessionid.split("%3A")[0] + '","sessionid":"' + data.sessionid + '"}'
        encoded_auth = base64.b64encode(auth_payload.encode('utf-8')).decode('utf-8')

        headers = {
            'User-Agent': "Instagram 237.0.0.14.102 Android (28/9; 300dpi; 1600x900; samsung; SM-N975F; SM-N975F; intel; en_US; 373310563)",
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': f"Bearer IGT:2:{encoded_auth}"
        }

        req = requests.post("https://i.instagram.com/api/v1/accounts/set_biography/", headers=headers, data=f"raw_text={data.bio_text}")

        if '"ok"' in req.text:
            return {"status": "success", "message": "Bio changed successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to change bio")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
