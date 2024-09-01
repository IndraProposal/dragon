# bitcoinlib.py

import sys

def check_bitcoinlib():
    try:
        # Попытка импортировать библиотеку bitcoinlib
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
        sys.exit(1)  # Завершение работы, если библиотека не инициализирована
    # Здесь можно добавить дополнительную логику по настройке bitcoinlib, если нужно
    # Например, установка соединений с сетью или загрузка кошельков

if __name__ == "__main__":
    initialize_bitcoinlib()
