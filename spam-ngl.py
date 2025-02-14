import random
import time
import threading
import requests
import urllib3

# Desactivar las advertencias
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Leer proxies
with open('proxies.txt', 'r') as file:
    proxies_list = file.read().splitlines()

counter_lock = threading.Lock()

def send_single_message(prox, username, message, counter):
    while True:
        try:
            # Configurar proxy
            px = {
                'http': f'{prox}',
                'https': f'{prox}'
            }

            current_time = time.localtime()
            formatted_time = time.strftime("%H:%M", current_time)

            deviceId = ''.join(random.choices('0123456789abcdef', k=42))

            url = 'https://ngl.link/api/submit'
            headers = {
                'User-Agent': 'ZARCO-SPAM-BOT',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Referer': f'https://ngl.link/{username}',
                'Origin': 'https://ngl.link'
            }
            data = {
                'username': username,
                'question': message,
                'deviceId': deviceId,
                'gameSlug': '',
                'referrer': ''
            }

            # Enviar solicitud POST
            response = requests.post(url, headers=headers, data=data, proxies=px, timeout=10, verify=False)

            if response.status_code != 200:
                print(f'[{formatted_time}] [Err] Ratelimited')
                time.sleep(10)
            else:
                with counter_lock:
                    counter[0] += 1
                    print(f'[{formatted_time}] [Msg] Sent: {counter[0]}')

        except Exception as e:
            time.sleep(10)

def send_message(username, message):
    counter = [0]  # Usar lista para pasar por referencia
    threads = []

    # Crear 10 hilos, uno para cada proxy
    for prox in proxies_list:
        for _ in range(5):  # Enviar 5 mensajes por cada proxy
            t = threading.Thread(target=send_single_message, args=(prox, username, message, counter))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    username = input('User => ')
    message = input('Message => ')
    creator = '♡ﮩ٨ـﮩﮩ٨ـﮩ٨zαя¢σ-ѕραмﮩ٨ـﮩ٨♡'

    if message == '':
        message = '☠✞𝑍𝐴𝑅𝐶𝑂-𝐵𝑂𝑇-𝑆𝑃𝐴𝑀✞☠'

    message = f'{creator}\n\n{message}'

    send_message(username, message)
