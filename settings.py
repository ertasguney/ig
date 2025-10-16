BASE_API_URL = "https://ig-rose-tau.vercel.app"
API_KEY = "instagram-48i9-telegram-dsofjsf9d783rhyds"

def check_session(session_id):
    API_PATH = "/session"  # ou autre préfixe selon la route
    url = f"{BASE_API_URL}{API_PATH}?key={API_KEY}&sessionid={session_id}&choice=17&data="
    response = requests.get(url)
    return response.json()  # ou autre traitement selon besoin
