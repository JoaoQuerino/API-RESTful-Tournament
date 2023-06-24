import random
from app import app
from flask import json
import os
from werkzeug.datastructures import FileStorage
import requests


__CONTENT_TYPE_JSON = 'application/json'
__CONTENT_TYPE_FORM_DATA = 'multipart/form-data'


def test_get_all_team():
    response = app.test_client().get('/team')
    data = json.loads(response.data.decode('utf-8'))
    
    assert response.status_code == 200
    assert len(data) > 0

def test_get_team_by_id():
    response = app.test_client().get('/team')
    data = json.loads(response.data.decode('utf-8'))

    team_id = data[-1]['id']
    response = app.test_client().get(f'/team/{team_id}')
    data = json.loads(response.data.decode('utf-8'))
    
    assert response.status_code == 200
    assert data['id'] == team_id

def test_create_team():
    payload = {
        "name": "Brasil"
    }

    response = app.test_client().get('/team')
    data = json.loads(response.data.decode('utf-8'))

    response_post = app.test_client().post('/team', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))

    response = app.test_client().get('/team')
    data_after = json.loads(response.data.decode('utf-8'))

    assert response_post.status_code == 200
    assert len(data) + 1 == len(data_after)

def test_put_team():
    response = app.test_client().get('/team')
    data = json.loads(response.data.decode('utf-8'))
    team = data[-1]

    payload = {
        "name": "Vasco"
    }

    response_put = app.test_client().put(f'team/{team["id"]}', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))

    response = app.test_client().get(f'/team/{team["id"]}')
    data = json.loads(response.data.decode('utf-8'))

    assert response_put.status_code == 200
    assert data['id'] == team['id']
    assert data['name'] != team['name']
 

def test_delete_team():
    response = app.test_client().get('/team')
    data = json.loads(response.data.decode('utf-8'))
    
    response_del = app.test_client().delete(f'team/{data[-1]["id"]}')

    response = app.test_client().get('/team')
    data_after = json.loads(response.data.decode('utf-8'))

    assert response_del.status_code == 200
    assert len(data) - 1 == len(data_after)


def test_upload_logo():
    
    file_name = "/home/querino/Downloads/lab-dev-main/Projeto/FileLogos/logo-test.jpg"
    data = {
        'file': (open(file_name, 'rb'), file_name)
    }

    response = app.test_client().post(f'/team/33/logo', content_type='multipart/form-data', data=data)
    with open("/home/querino/Downloads/lab-dev-main/Projeto/FileLogos/logErroUpload.txt", "w") as file_out:
        file_out.write(f"Status code: {response.status_code}\n")
        file_out.write(f"Headers: {response.headers}\n")
        file_out.write(f"Body: {response.get_data(as_text=True)}\n")

    assert response.status_code == 200


def test_get_logo_by_id():
    response = requests.get('http://127.0.0.1:5000/team')
    data = response.json()

    team_id = data[-1]['id']
    response = requests.get(f'http://127.0.0.1:5000/team/{team_id}/logo')

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'image/jpeg' or response.headers['Content-Type'] == 'image/png'

#Exclui todos os cadastros
# def test_delete_all_teams():
#     response = app.test_client().get('/team')
#     data = json.loads(response.data.decode('utf-8'))
    
#     response_del = app.test_client().delete(f'team')

#     response = app.test_client().get('/team')
#     data_after = json.loads(response.data.decode('utf-8'))

#     assert response_del.status_code == 200
#     assert data_after

    