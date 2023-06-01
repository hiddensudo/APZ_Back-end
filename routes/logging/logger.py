import logging

# Створюємо новий об'єкт Logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

# Створюємо об'єкт Handler для запису повідомлень у файл app.log
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

# Створюємо об'єкт Handler для виводу повідомлень у консоль PyCharm
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Додаємо обидва об'єкти Handler до об'єкта Logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log(message):
    logger.info(message)
