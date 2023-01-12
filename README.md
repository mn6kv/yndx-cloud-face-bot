# CLOUD-Yndex-Vision
Обработка фотографий с лицами людей

# Обработка фотографий с лицами людей
## Объекты
### Бакеты
- itis-2022-2023-vvot03-photos
- itis-2022-2023-vvot03-faces
### БД
- vvot03-db-photo-face
### Очереди
- vvot03-tasks
### Триггеры
- vvot03-photo-trigger (сервисный аакаунт **vvot03-face-detection**)
- vvot03-task-trigger (сервисный аккаунт **vvot03-cut-invoker**)
### Функции
- vvot03-face-detection (сервисный аккаунт **vvot03-face-detection**, код из файла **function/crop.py**)
- vvot03-boot (сервисный аккаунт **vvot03-boot-function**, код из файла **function/bot.py**)
### Контейнер
- vvot03-face-cut (сервисный аккаунт **vvot03-cut-invoker**, код из папки **container**)
