import random
from app import app
from flask import json


__CONTENT_TYPE_JSON = 'application/json'
__CONTENT_TYPE_FORM_DATA = 'multipart/form-data'


def test_create_player():
    response = app.test_client().get('/team')
    data = json.loads(response.data.decode('utf-8'))

    team_id = data[-1]['id']

    payload = {
        "name": "Joao",
        "team_id": team_id,
        "number": 1
    }

    response = app.test_client().get('/player')
    data = json.loads(response.data.decode('utf-8'))

    response_post = app.test_client().post('/player', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))

    response = app.test_client().get('/player')
    data_after = json.loads(response.data.decode('utf-8'))

    assert response_post.status_code == 200
    assert len(data) + 1 == len(data_after)

def test_get_all_player():
    response = app.test_client().get('/player')
    data = json.loads(response.data.decode('utf-8'))
    
    assert response.status_code == 200
    assert len(data) > 0

def test_get_all_player_by_team():
    response = app.test_client().get('/player')
    data = json.loads(response.data.decode('utf-8'))

    response_team = app.test_client().get('/team')
    data_team = json.loads(response_team.data.decode('utf-8'))

    team_id = data_team[-1]['id']

    
    assert response.status_code == 200
    assert len(data) > 0    

def test_get_player_by_id():
    response = app.test_client().get('/player')
    data = json.loads(response.data.decode('utf-8'))

    player_id = data[-1]['id']
    response = app.test_client().get(f'/player/{player_id}')
    data = json.loads(response.data.decode('utf-8'))
    
    assert response.status_code == 200
    assert data['id'] == player_id

def test_put_player():
    response = app.test_client().get('/player')
    data = json.loads(response.data.decode('utf-8'))
    player = data[-1]

    response_team = app.test_client().get('/team')
    data_team = json.loads(response_team.data.decode('utf-8'))

    team_id = data_team[-1]['id']

    payload = {
        "name": "Joao2", #precisa mudar alguma coisa
        "team_id": team_id,
        "number": 1
    }

    response_put = app.test_client().put(f'player/{player["id"]}', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))

    response = app.test_client().get(f'/player/{player["id"]}')
    data = json.loads(response.data.decode('utf-8'))

    assert response_put.status_code == 200
    assert data['id'] == player['id']
    any_field_different = False

    if data['name'] != player['name']:
        any_field_different = True
    elif data['team_id'] != player['team_id']:
        any_field_different = True
    elif data['number'] != player['number']:
        any_field_different = True

    # Verifica se pelo menos um campo é diferente
    assert any_field_different 
 

def test_delete_player():
    response = app.test_client().get('/player')
    data = json.loads(response.data.decode('utf-8'))
    
    response_del = app.test_client().delete(f'player/{data[-1]["id"]}')

    response = app.test_client().get('/player')
    data_after = json.loads(response.data.decode('utf-8'))

    assert response_del.status_code == 200
    assert len(data) - 1 == len(data_after)

#Deleta todos cadastros
# def test_delete_all_player():
#     response = app.test_client().get('/player')
#     data = json.loads(response.data.decode('utf-8'))
    
#     response_del = app.test_client().delete(f'player')

#     response = app.test_client().get('/player')
#     data_after = json.loads(response.data.decode('utf-8'))

#     assert response_del.status_code == 200
#     assert len(data) - 1 == len(data_after)