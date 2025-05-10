# crypto_pipeline_eldar
<h1>Инструкция для по настройке окружения от первого входа на сервер до запуска Apache Airflow</h1> 

<h4>Скачивание и установка всех необходимых программ.</h4>

1. Подключение к серверу по SSH - на моем личном ПК стоит Windows, сервер на ОС linux, поэтому я использовал для удобства wsl
    ```bash
    ssh root@your-server-ip
    ```

2. Обновление системы
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

3. Установка git
    ```bash
    sudo apt install git
    ```

4. Убедитесь, что установка прошла успешно
    ```bash
    git --version
    ```

5. Установка Docker
    ```bash
    sudo apt-get install ca-certificates curl -y
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc > /dev/null
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
    ```

6. Проверка Docker
    ```bash
    sudo docker run hello-world
    ```

7. Установка Docker compose
    ```bash
    sudo apt-get update
    sudo apt-get install docker-compose-plugin
    ```

<h4>Генерация SSH-ключа и привязка к GitHub</h4>

1. Проверка существующих SSH-ключей
    ```bash
    ls -al ~/.ssh
    ```
2. Создание нового SSH-ключа
    ```bash
    ssh-keygen -t rsa -b 4096 -C "email@example.com"
    ```

3. Добавление SSH-ключа в агент автоматически предоставляет ключ для аутентификации Git, не требуя вашего вмешательства.
    Запускаем shh агент
    ```bash
    eval "$(ssh-agent -s)"
    ```
    Добавляем ключ в агент
    ```bash
    ssh-add ~/.ssh/id_rsa
    ```
4. Для добавления SSH-ключ на GitHub-аккаунт выведем его
    ```bash
    cat ~/.ssh/id_rsa.pub
    ```
    Скопируй весь вывод (он начинается с ssh-rsa и заканчивается названием сервера или email-адресом).
    Открой GitHub → Настройки SSH-ключей.
    Нажми "New SSH key", введи любое название и вставь туда ключ.
    Нажми "Add SSH Key".

5. Проверка соединения
    ```bash
    ssh -T git@github.com
    ```
    вывод: Hi username! You've successfully authenticated...

6. Клонирование репозитория
    git clone ...

<h4>Для дальнейшей работы и написения кода я буду использовать редакор VS Code</h4>

1. Для подключения к серверу установливаем расширение Remote - SSH
2. Настройка SSH-подключения. 
    Ctrl+Shift+P -> Remote-SSH: Add New SSH -> ssh root@server-ip
    Далее в выпадающем списке выбираем ~/.ssh/config. Больше не нужно вручную вводить ssh root@server-ip
    После снова Ctrl+Shift+P  -> Remote-SSH: Connect to -> Выбираем имя сервера -> вводим root пароль.


<h4>Настройка и создание Airflow и БД(у меня postgre)</h4>
    Совздаем внурти проекта следующие файлы: 
    - docker-compose.yml настройки, зависимости и связи между контейнерами Airflow, PostgreSQL и т.д.
    - .env хранит переменные например, пароли, логины, которые подставляются в docker-compose.yml
    - /docker/airflow/Dockerfile Описывает, как собрать Airflow с нужными Python-библиотеками
    - /docker/airflow/requirements.txt Список Python библиотек, которые устанавливаются внутрь Airflow-контейнера

<h4>Запуск контейнеров</h4>

1. Сборка и запуск всех контейнеров
    ```bash 
    docker compose up -d 
    ``` 
2. Пересобрать контейнеры (например, если изменил Dockerfile или добавил/ удалил бибилотеки из requirements.txt)
    ```bash 
    docker compose up -d --build 
    ``` 
3. Посмотреть статус контейнеров
    ```bash 
    docker compose ps 
    ```
4. Посмотреть логи контейнера
    ```
    bash docker logs <контейнер> 
    ``` 
5. Остановить контейнеры 
    ```
    bash docker compose down -v 
    ```
 
