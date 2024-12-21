import datetime
import pyperclip

# Получаем текущее время в нужном формате
current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

# Копируем строку в буфер обмена
pyperclip.copy(current_time)

# Выводим строку на экран
print(current_time)
