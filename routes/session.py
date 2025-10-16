from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import hashlib, time, random, string, requests, re, base64, uuid

router = APIRouter()
uu = '83f2000a-4b95-4811-bc8d-0f3539ef07cf'

class LoginRequest(BaseModel):
    username: str
    password: str

def generate_device_id(ID: str):
    volatile_ID = "12345"
    m = hashlib.md5()
    m.update(ID.encode('utf-8') + volatile_ID.encode('utf-8'))
    return 'android-' + m.hexdigest()[:16]

@router.post("/get_session_code")
def get_session_code(data: LoginRequest):
    timestamp = str(int(time.time()))
    device_id = generate_device_id(data.username)
    login_data = {
        'guid': uu,
        'enc_password': f"#PWD_INSTAGRAM:0:{timestamp}:{data.password}",
        'username': data.username,
        'device_id': device_id,
        'login_attempt_count': '0',
    }
    headers = {
        'User-Agent': 'Instagram 155.0.0.37.107 Android (28/9)',
        'Host': 'i.instagram.com',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    req = requests.post("https://i.instagram.com/api/v1/accounts/login/", headers=headers, data=login_data)
    if "logged_in_user" in req.text:
        cookies = req.cookies
        return {
            "status": "success",
            "username": data.username,
            "sessionid": cookies.get("sessionid"),
            "csrftoken": cookies.get("csrftoken"),
            "mid": cookies.get("mid"),
        }
    elif 'checkpoint_challenge_required' in req.text:
        raise HTTPException(status_code=403, detail="Challenge required")
    else:
        error_message = re.search(r'"message":"(.*?)",', req.text)
        raise HTTPException(status_code=400, detail=error_message.group(1) if error_message else "Login failed")

class AcceptSessionRequest(BaseModel):
    username: str
    password: str

@router.post("/get_session_acception")
def get_session_acception(data: AcceptSessionRequest):
    # Implémentation adaptée complète du login d'option 2 avec suppression des input()
    my_uuid = uuid.uuid4()
    my_uuid_str = str(my_uuid)
    modified_uuid_str = my_uuid_str[:8] + "should_trigger_override_login_success_action" + my_uuid_str[8:]
    rd = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

    data = {
        "params": "{\"client_input_params\":{\"contact_point\":\"" + data.username + "\",\"password\":\"#PWD_INSTAGRAM:0:0:" + data.password +
                  "\",\"fb_ig_device_id\":[],\"event_flow\":\"login_manual\",\"openid_tokens\":{},\"machine_id\":\"ZG93WAABAAEkJZWHLdW_Dm4nIE9C\",\"family_device_id\":\"\",\"accounts_list\":[],\"try_num\":1,\"login_attempt_count\":1,\"device_id\":\"android-" + rd + "\",\"auth_secure_device_id\":\"\",\"device_emails\":[],\"secure_family_device_id\":\"\",\"event_step\":\"home_page\"},\"server_params\":{\"is_platform_login\":0,\"qe_device_id\":\"\",\"family_device_id\":\"\",\"credential_type\":\"password\",\"waterfall_id\":\"" + modified_uuid_str + "\",\"username_text_input_id\":\"9cze54:46\",\"password_text_input_id\":\"9cze54:47\",\"offline_experiment_group\":\"caa_launch_ig4a_combined_60_percent\",\"INTERNAL__latency_qpl_instance_id\":56600226400306,\"INTERNAL_INFRA_THEME\":\"default\",\"device_id\":\"android-" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=16)) + "\",\"server_login_source\":\"login\",\"login_source\":\"Login\",\"should_trigger_override_login_success_action\":0,\"ar_event_source\":\"login_home_page\",\"INTERNAL__latency_qpl_marker_id\":36707139}}"
    }
    data["params"] = data["params"].replace("\"family_device_id\":\"\"", "\"family_device_id\":\"" + my_uuid_str + "\"")
    data["params"] = data["params"].replace("\"qe_device_id\":\"\"", "\"qe_device_id\":\"" + my_uuid_str + "\"")

    headers = {
        "Host": "i.instagram.com", "X-Ig-App-Locale": "ar_SA", "X-Ig-Device-Locale": "ar_SA",
        "X-Ig-Mapped-Locale": "ar_AR", "X-Pigeon-Session-Id": f"UFS-{uuid.uuid4()}-0", "X-Pigeon-Rawclienttime": "1685026670.130",
        "X-Ig-Bandwidth-Speed-Kbps": "-1.000", "X-Ig-Bandwidth-Totalbytes-B": "0", "X-Ig-Bandwidth-Totaltime-Ms": "0",
        "X-Bloks-Version-Id": "8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb", "X-Ig-Www-Claim": "0",
        "X-Bloks-Is-Layout-Rtl": "true", "X-Ig-Device-Id": f"{uuid.uuid4()}", "X-Ig-Family-Device-Id": f"{uuid.uuid4()}",
        "X-Ig-Android-Id": f"android-{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}",
        "X-Ig-Timezone-Offset": "10800", "X-Fb-Connection-Type": "WIFI", "X-Ig-Connection-Type": "WIFI",
        "X-Ig-Capabilities": "3brTv10=", "X-Ig-App-Id": "567067343352427", "Priority": "u=3",
        "User-Agent": f"Instagram 303.0.0.0.59 Android (28/9; 320dpi; 900x1600; {''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}/{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; en_GB;)",
        "Accept-Language": "ar-SA, en-US", "Ig-Intended-User-Id": "0", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Content-Length": "1957", "Accept-Encoding": "gzip, deflate", "X-Fb-Http-Engine": "Liger", "X-Fb-Client-Ip": "True", "X-Fb-Server-Cluster": "True"
    }
    response = requests.post('https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/', headers=headers, data=data)
    body = response.text
    if "Bearer" in body:
        session = re.search(r'Bearer IGT:2:(.*?),', response.text).group(1).strip()[:-8]
        full = base64.b64decode(session).decode('utf-8')
        if "sessionid" in full:
            sessionid = re.search(r'"sessionid":"(.*?)"}', full).group(1).strip()
            return {"status":"success", "sessionid": sessionid}
    elif "The password you entered is incorrect" in body or "Please check your username and try again." in body or "inactive user" in body or "should_dismiss_loading\", \"has_identification_error\"" in body:
        raise HTTPException(status_code=400, detail="Bad password or inactive user")
    elif "challenge_required" in body or "two_step_verification" in body:
        raise HTTPException(status_code=403, detail="Challenge required")
    else:
        raise HTTPException(status_code=500, detail="Unknown error")
