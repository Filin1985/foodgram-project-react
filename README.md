# Проект Foodgram!

##Описание проекта\*\*

Проект для создания рецептов. Рецепты можно добавлять визбранное, создавать список покупок, а также подписываться на других авторов.

**Используемые технологии**

- Django
- Django RestFramework

### Как запустить проект

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

5. Устанавливаем зависимости из файла requirements.txt

```
pip install -r requirements.txt
```

6. Выполняем миграции

```
python3 manage.py migrate
```

7. Запускаем проект

```
python3 manage.py runserver
```

### Примеры запросов

1. Получить (GET), создать (POST) - /api/v1/recipes/
2. Получить (GET), удалить (DELETE) по id - /api/v1/recipes/{id}/
3. Изменить рецепт (PUT, PATCH) по id - /api/v1/recipes/{id}/
