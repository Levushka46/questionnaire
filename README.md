# questionnaire
Руководство по запуску проекта:  
Запустить docker compose.
```
docker compose up --build -d
```
Перейти по http://127.0.0.1:8000/admin/ и войти используя admin/admin.  
Пароль можно изменить после входа.  

В админ панели присутствуют:  
CRUD.  

В проекте присутствуют тесты и русский язык в админ панели.  

Команда для генерации тестового опроса(необходимо выполнить в терминале):
```
docker exec -it questionnaire-web-1 /app/load_test_data.sh
```

На главной странице присутствуют регистрация/авторизация.  
Параметры -  
sign up:
```
{"user":"leva", "email":"leva@mail.ru","password":"12345"}
```   
sign in:
```
{"email":"leva@mail.ru","password":"12345"}
```
На странице http://127.0.0.1:8000/page/1/ начинается тестирование, после прохождения теста идет переадресация на http://127.0.0.1:8000/done/  
Подробная документация доступная по ссылке:  
https://docs.google.com/document/d/1x1CfRCzMX-GJsX259x6SMD426I9bNaObxKKKeJ7lk2A/edit?usp=sharing
