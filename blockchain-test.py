# blockchain-test.py

import sys
import os
import bitcoinlib
from bitcoinlib.wallets import HDWallet, Wallet
from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.services.services import Service
from bitcoinlib.keys import HDKey

def check_bitcoinlib():
    try:
        import bitcoinlib
        print("Bitcoinlib успешно инициализирована и готова к работе.")
        return True
    except ImportError:
        print("Ошибка: библиотека bitcoinlib не установлена.")
        return False
    except Exception as e:
        print(f"Произошла ошибка при инициализации bitcoinlib: {e}")
        return False

def initialize_bitcoinlib():
    if not check_bitcoinlib():
        sys.exit(1)

    # Настройка соединения с сетью (например, bitcoin mainnet)
    service = Service(network='bitcoin')
    print(f"Подключен к сети: {service.network}")

    # Создание или загрузка кошелька (обновленный синтаксис)
    wallet_name = "MyHDWallet"
    wallet_path = f"{wallet_name}.wallet"
    passphrase = 'example data'  # Или укажите вашу парольную фразу, если она есть
    if not os.path.exists(wallet_path):
        # Создаем новый HD-кошелек с использованием мнемонической фразы
        mnemo = Mnemonic()
        words = mnemo.generate(strength=128)  # Генерируем мнемоническую фразу
        wallet = HDWallet.from_passphrase(words, network='bitcoin', passphrase=passphrase)
        wallet.save(wallet_name) 
        print(f"Создан кошелек: {wallet_name} с мнемоникой: {words}")
    else:
        # Загружаем существующий кошелек
        wallet = Wallet.load(wallet_name, passphrase=passphrase)
        print(f"Загружен существующий кошелек: {wallet_name}")
    return wallet

def generate_self_auth_keys(num_keys=5):
    """Создает набор ключей для самоавторизации."""
    keys = []
    for _ in range(num_keys):
        key = HDKey()
        keys.append({
            'private_key': key.private_hex,
            'public_key': key.public_hex,
            'address': key.address
        })
    print(f"Сгенерировано {num_keys} ключей для самоавторизации.")
    return keys

def setup_local_authorization_center(auth_keys):
    """Настраивает локальный центр авторизации."""
    auth_center_path = "local_auth_center"
    if not os.path.exists(auth_center_path):
        os.makedirs(auth_center_path)

    # Сохранение ключей в файлы с обработкой ошибок
    for i, key in enumerate(auth_keys):
        try:
            with open(f"{auth_center_path}/key_{i}.txt", "w") as f:
                f.write(f"Private Key: {key['private_key']}\n")
                f.write(f"Public Key: {key['public_key']}\n")
                f.write(f"Address: {key['address']}\n")
        except IOError as e:
            print(f"Ошибка при записи ключа {i}: {e}")
    print(f"Локальный центр авторизации настроен. Ключи сохранены в {auth_center_path} (с возможными ошибками).")


if __name__ == "__main__":
    # Инициализация bitcoinlib и настройка кошелька
    wallet = initialize_bitcoinlib()

    # Генерация ключей самоавторизации
    auth_keys = generate_self_auth_keys()

    # Настройка локального центра авторизации
    setup_local_authorization_center(auth_keys)

    # Получение адреса для получения средств (обновленный синтаксис)
    receiving_address = wallet.get_key().address 
    print(f"Адрес для получения средств: {receiving_address}")
