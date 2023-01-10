# Проект Foodgram!

##Описание проекта\*\*

Проект для создания рецептов. Рецепты можно добавлять визбранное, создавать список покупок, а также подписываться на других авторов.

**Используемые технологии**

- Django
- Django RestFramework

### Как запустить проект локально

1. Клонируем репозиторий

```
git clone https://github.com/Filin1985/foodgram-project-react.git
```

2. Заходим в папку с проектом

```
cd backend/foodgram
```

3. Устанавливаем виртуальное окружение

```
python3 -m venv venv
```

4. Активируем виртуальное окружение

```
source venv/bin/activate
```

5. Cоздайте файл .env в директории /infra/ с содержанием:

```
SECRET_KEY=секретный ключ django
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

6. Устанавливаем зависимости из файла requirements.txt

```
pip install -r requirements.txt
```

7. Выполняем миграции

```
python3 manage.py migrate
```

8. Запускаем проект

```
python3 manage.py runserver
```

### Как запустить проект с помощью Docker контейнера

1. Установите Docker

2. Запустите docker compose:

```
sudo docker compose up -d --build
```

3. Сделайте миграции:

```
sudo docker compose exec backend python manage.py migrate
```

4. Загрузите ингредиенты:

```
sudo docker compose exec backend python manage.py loaddatatobase
```

5. Создайте суперпользователся:

```
sudo docker compose exec backend python manage.py createsuperuser
```

6. Соберите статику:

```
sudo docker compose exec backend python manage.py collectstatic --no-input
```

### Примеры запросов

1. Получить (GET), создать (POST) - /api/v1/recipes/
2. Получить (GET), удалить (DELETE) по id - /api/v1/recipes/{id}/
3. Изменить рецепт (PUT, PATCH) по id - /api/v1/recipes/{id}/

### Ссылка на проект на сервере

[foodgram](http://158.160.20.155)

### Actions badge

![workflow bagde](https://github.com/Filin1985/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
