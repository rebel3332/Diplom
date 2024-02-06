# Создать виртуальное окружение
python.exe -m venv .

# Активирую виртуальное окружение
.\Scripts\activate

# рабта с pip
pip freeze > requirements.txt
pip install -r requirements.txt

# Собрать образ Docker
docker build -t dockermalex/telegram_bot_from_diplob_1year .
# ТЕГ
docker tag telegram_bot_from_diplob_1year dockermalex/telegram_bot_from_diplob_1year

# Посмотреть список собранных образов
docker images

# Запуск Docker контейнера
-it объединяет команды: -i оставляет строку для ввода, а -t выделяет терминал; <br>
**docker run -it --rm -e TELEGRAM_API='your telegram api key' -e SERVER_URL='http://127.0.0.1:8081' dockermalex/telegram_bot_from_diplob_1year**pippgdfg
