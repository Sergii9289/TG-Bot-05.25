from pathlib import Path
import datetime

BASE_DIR = Path(__file__).resolve().parent.parent  # Піднімаємо рівень вище
LOG_DIR = BASE_DIR / 'app/logging'
LOG_DIR.mkdir(parents=True, exist_ok=True)  # Створюємо папку, якщо її немає

def log_line(func_name, error=None):
    return f'Call:{datetime.datetime.now()}.Name:{func_name}.Status:{error if error else "OK"}\n'

def log_to_file(func_name, error=None):
    """Записує рядок логування у файл"""
    curr_date = datetime.datetime.now().date()
    log_file_name = f'log_function_call_{curr_date}.txt'
    log_file_path = LOG_DIR / log_file_name

    with log_file_path.open('a') as file:
        file.write(log_line(func_name, error))