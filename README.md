# yp_ambassador_crm

Инфраструктура управления сообществом Амбассадоры Практикума


## ссылка на Swagger

[http://89.111.174.233/swagger](http://89.111.174.233/swagger)

## инструкция по сборке и запуску

- Клонируем репозиторий
```
git@github.com:K1N88/yp_ambassador_crm.git
```
- создаем переменные окружения по примеру env_example
- скачиваем образы с Docker Hub
```
sudo docker pull k1n8/crm_app:latest
sudo docker pull k1n8/crm_app_frontend:latest
```
- переходим в папку infra/
```
cd infra/
```
- собираем и запускам контейнеры
```
sudo docker-compose up -d --build
```
- открываем главную страницу [http://89.111.174.233/](http://89.111.174.233/)

## :hammer_and_wrench: Основные технологии и библиотеки :
Python 3.10
Django 4.2.5
djangorestframework 3.14
djoser
gunicorn
nginx

## :juggling_person: Над проектом работали :

| Имя | Роль | Контакты | Гит |
| - | :-: | :-: | :-: |
| Константин Назаров | бэкенд | <a href="https://t.me/constK1N" target="_blank"> :envelope:</a>  | <a href="https://github.com/K1N88" target="_blank"> :heavy_check_mark:</a> |
| Артем Натолин | бэкенд | <a href="https://t.me/nilotan" target="_blank"> :envelope:</a>  | <a href="https://github.com/dagedarr" target="_blank"> :heavy_check_mark:</a> |
| Даниил Пастунов | бэкенд | <a href="https://t.me/allwh1te" target="_blank"> :envelope:</a>  | <a href="https://github.com/dflient" target="_blank"> :heavy_check_mark:</a> |
| Александр Мыльников | бэкенд | <a href="https://t.me/ingaksdr" target="_blank"> :envelope:</a>  | <a href="https://github.com/aksdr53" target="_blank"> :heavy_check_mark:</a> |
