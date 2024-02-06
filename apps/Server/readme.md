# Создать вируальную среду
python -m venv .  

# рабта с pip
pip freeze > requirements.txt
pip install -r requirements.txt

# Собрать образ Docker
docker build -t server_from_diplob_1year .

# Добавить ТЕГ
docker tag server_from_diplob_1year dockermalex/server_from_diplob_1year

# Посмотреть список собранных образов
docker images

# Запуск Docker контейнера
**-it** объединяет команды:
* **-i** оставляет строку для ввода, а 
* **-t** выделяет терминал; <br>
**docker run -it --rm -p=8081:8081 -e HOST=0.0.0.0 -e PORT=8081 dockermalex/server_from_diplob_1year**
