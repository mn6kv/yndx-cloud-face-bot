import os
import ydb
import ydb.iam
import json
import requests

TOKEN = os.getenv("BOT_TOKEN")

driver: ydb.Driver
PHOTO_LINK_TEMPLATE = os.getenv("PHOTO_LINK_TEMPLATE")
OBJECT_LINK_TEMPLATE = os.getenv("OBJECT_LINK_TEMPLATE")

def initDb():
    endpoint = os.getenv("DB_ENDPOINT")
    database = os.getenv("DB_DATABASE")
    creds = ydb.iam.MetadataUrlCredentials()

    driver_config = ydb.DriverConfig(
        endpoint, database, credentials=creds
    )

    return ydb.Driver(driver_config)

def getFace(chat_id):
    query = f"""
    SELECT * FROM photo WHERE name is NULL LIMIT 1;
    """
    session = driver.table_client.session().create()
    result_sets = session.transaction().execute(query, commit_tx=True)
    session.closing()

    for row in result_sets[0].rows:
        face_id = row.face_id.decode("utf-8")
        photo_url = PHOTO_LINK_TEMPLATE + face_id
        sendPhoto(chat_id, photo_url)

def setNameToPhoto(name):
    query = f"""
        SELECT * FROM photo WHERE name is NULL LIMIT 1;
        """
    session = driver.table_client.session().create()
    result_sets = session.transaction().execute(query, commit_tx=True)

    face_id = ''
    for row in result_sets[0].rows:
        face_id = row.face_id.decode("utf-8")
    if face_id == '':
        return

    query = f"""
    UPDATE photo SET name = '{name}' WHERE face_id = '{face_id}';
    """
    session.transaction().execute(query, commit_tx=True)
    session.closing()

def find(chat_id, name):
    query = f"""
    SELECT DISTINCT original_id, name FROM photo WHERE name = '{name}';
    """
    session = driver.table_client.session().create()
    result_sets = session.transaction().execute(query, commit_tx=True)
    session.closing()

    if len(result_sets[0].rows) == 0:
        sendMessage(chat_id, f'Нет фотографии с именем {name}')
    for row in result_sets[0].rows:
        object_id = row.original_id.decode("utf-8")
        photo_url = OBJECT_LINK_TEMPLATE + object_id
        sendPhoto(chat_id, photo_url)

def init():
    global driver
    driver = initDb()
    driver.wait(timeout=5)

def handler(event, context):
    init()
    
    body = json.loads(event['body'])
    chat_id = body['message']['from']['id']
    command = body['message']['text']

    if command == '/start':
        sendMessage(chat_id, 'Bot started')
        return
    if command == '/getface':
        getFace(chat_id)
        return
    if command.startswith('/find'):
        args = command.split(' ')
        find(chat_id, args[1])
        return

    setNameToPhoto(command)
    sendMessage(chat_id, f'Добавлено новое имя {command}')

def sendMessage(chat_id, text):
    url = 'https://api.telegram.org/bot' + TOKEN + '/' + 'sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, data=data)

def sendPhoto(chat_id, photo):
    url = 'https://api.telegram.org/bot' + TOKEN + '/' + 'sendPhoto'
    data = {'chat_id': chat_id, 'photo': photo}
    r = requests.post(url, data=data)
    print(r)