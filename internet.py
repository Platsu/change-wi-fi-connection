import time
import pywifi
import requests


def connect_to_wifi(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.disconnect()

    time.sleep(1)

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = pywifi.const.AUTH_ALG_OPEN
    profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
    profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(3)

    if iface.status() == pywifi.const.IFACE_CONNECTED:
        print(f"Підключено до мережі: {iface.name()}")
        if check_internet_connection():
            print("Інтернет-з'єднання доступне.")
            return True
        else:
            print("Інтернет-з'єднання недоступне.")
            return False
    else:
        print(f"Не вдалося підключитися до мережі: {iface.name()}")
        return False


def check_internet_connection():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False


def check_and_connect_networks(networks):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    current_network = None
    previous_network = None

    while True:
        current_status = iface.status()
        current_ssid = iface.name()

        if current_ssid != current_network:
            print(f"Поточна мережа: {current_ssid}")
            current_network = current_ssid

            if current_ssid not in networks:
                print(f"Мережа {current_ssid} не визначена у списку відомих мереж.")
                continue

            password = networks[current_ssid]
            if connect_to_wifi(current_ssid, password):
                previous_network = current_ssid
            else:
                print("Спробуйте іншу мережу.")

        time.sleep(5)


known_networks = {
    "TP-LINK_15C8": "32379099"
}

check_and_connect_networks(known_networks)

# Start-Process python -ArgumentList "internet.py" -NoNewWindow   запуск через terminal