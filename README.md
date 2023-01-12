# yndx-cloud-face-bot

# Обработка фотографий с лицами людей
## Объекты
### Бакеты
- itis-2022-2023-vvot41-photos
- itis-2022-2023-vvot41-faces
### БД
- vvot41-db-photo-face
### Очереди
- vvot41-tasks
### Триггеры
- vvot41-photo-trigger (сервисный аакаунт **vvot41-face-detection**)
- vvot41-task-trigger (сервисный аккаунт **vvot41-cut-invoker**)
### Функции
- vvot41-face-detection (сервисный аккаунт **vvot41-face-detection**, код из файла **function/crop.py**)
- vvot41-boot (сервисный аккаунт **vvot41-boot-function**, код из файла **function/bot.py**)
### Контейнер
- vvot41-face-cut (сервисный аккаунт **vvot41-cut-invoker**, код из папки **container**)
