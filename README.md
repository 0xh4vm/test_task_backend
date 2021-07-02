# Тестовое задание
## Описание: https://www.notion.so/Test-task-backend-6e166d1405de4191bdb92f9db0d7a5b7

Для запуска необходимо выполнить следующие команды в домашней директории проекта:
```
docker build -t xh4vm/test_task_backend .
docker run -d --name test_task_backend -p 8000:5000 --rm xh4vm/test_task_backend
```
Для запуска тестов необходимо выполнить команду:
`docker exec -it test_task_backend pytest -vv`