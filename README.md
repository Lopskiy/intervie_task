# Intervie Task Project Documentation

## Требования
Docker + docker-compose
```sh
pip install -r requirements.txt
```
## Установка и настройка
```sh
git clone <your-repo-url>
cd <your-repo-directory>
```
## Запуск проекта
Поднимите контейнеры Docker:
```sh
docker-compose up --build
```
Нужно создать superuser
```sh
docker-compose exec web python manage.py createsuperuser
```
Для заполнения базы тестовами данными нужно выполнить
```sh
docker exec -it intervie_task_web_1 bash
python manage.py populate_data
```
Проект доступен по адресу http://localhost:8000, а админ-панель по адресу http://localhost:8000/admin.
## Использование api
Методы 
GET /api/tariffs/ /api/house/ /api/apartment/ /api/watermeter/ /api/watermeterreading/

Пример 
GET http://localhost:8000/api/houses/

```sh
[
    {
        "id": 1,
        "apartments": [
            {
                "id": 1,
                "water_meters": [
                    {
                        "id": 1,
                        "readings": [
                            {
                                "id": 14,
                                "date": "2024-07-17",
                                "value": "59.63",
                                "water_meter": 1
                            },
                            {
                                "id": 1,
                                "date": "2024-06-30",
                                "value": "300.00",
                                "water_meter": 1
                                
....
```

POST /api/tariffs/ /api/house/ /api/apartment/ /api/watermeter/ /api/watermeterreading
Пример
http://localhost:8000/api/tariffs/
body:
```sh
{
    "name": "cold_2024",
    "price_per_unit": "101.00"
}
```
Рассчет кварплаты
http://localhost:8000/api/calculate_rent/2/3/2024/
Запишется в базе 
Прогресс выполнения задачи можно отслеживать через Celery Flower или другие инструменты мониторинга Celery.