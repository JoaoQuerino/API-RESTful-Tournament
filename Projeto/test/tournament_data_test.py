import random
from app import app
from flask import json


__CONTENT_TYPE_JSON = 'application/json'
__CONTENT_TYPE_FORM_DATA = 'multipart/form-data'


def test_get_all_tournaments_data():
    response = app.test_client().get('/tournament')
    data = json.loads(response.data.decode('utf-8'))
    
    assert response.status_code == 200

def test_create_tournament_data():
    response = app.test_client().get('/team')
    dataTeam = json.loads(response.data.decode('utf-8'))
    team_id = dataTeam[-1]['id']

    payload = {
        "name": "Teste11",
        "team_id": team_id,
        "favor_goal": 1,
        "against_goal": 1,
        "wins": 1,
        "loses": 1,
        "draws": 1
    }

    response = app.test_client().get('/tournament')
    data = json.loads(response.data.decode('utf-8'))

    response_post = app.test_client().post('/tournament', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))

    response = app.test_client().get('/tournament')
    data_after = json.loads(response.data.decode('utf-8'))

    assert response_post.status_code == 200
    assert len(data) + 1 == len(data_after)


def test_get_tournament_data_by_id():
    response = app.test_client().get('/tournament')
    data = json.loads(response.data.decode('utf-8'))

    tournament_data_id = data[-1]['id']
    response = app.test_client().get(f'/tournament/{tournament_data_id}')
    data = json.loads(response.data.decode('utf-8'))
    
    assert response.status_code == 200
    assert data['id'] == tournament_data_id

def test_put_tournament():
    response = app.test_client().get('/team')
    dataTeam = json.loads(response.data.decode('utf-8'))
    team_id = dataTeam[-1]['id']

    response = app.test_client().get('/tournament')
    data = json.loads(response.data.decode('utf-8'))
    tournament = data[-1]

    payload = {
        "name": "Teste atualizado2",
        "team_id": team_id,
        "favor_goal": 1,
        "against_goal": 1,
        "wins": 1,
        "loses": 1,
        "draws": 1
    }

    response_put = app.test_client().put(f'tournament/{tournament["id"]}', content_type=__CONTENT_TYPE_JSON, data=json.dumps(payload))

    response = app.test_client().get(f'/tournament/{tournament["id"]}')
    data = json.loads(response.data.decode('utf-8'))

    assert response_put.status_code == 200
    assert data['id'] == tournament['id']
    any_field_different = False

    any_field_different = data != tournament

    # Verifica se pelo menos um campo é diferente
    assert any_field_different 
 

def test_delete_tournament():
    response = app.test_client().get('/tournament')
    data = json.loads(response.data.decode('utf-8'))
    
    response_del = app.test_client().delete(f'tournament/{data[-1]["id"]}')

    response = app.test_client().get('/tournament')
    data_after = json.loads(response.data.decode('utf-8'))

    assert response_del.status_code == 200
    assert len(data) - 1 == len(data_after)

def test_get_tournament_data_by_team_id():
    response = app.test_client().get('/team')
    dataTeam = json.loads(response.data.decode('utf-8'))
    team_id = dataTeam[-1]['id']

    response = app.test_client().get('/tournament')
    data = json.loads(response.data.decode('utf-8'))

    response_post = app.test_client().get(f'/tournament/team/{team_id}')

    response = app.test_client().get('/tournament')
    data_after = json.loads(response.data.decode('utf-8'))

    assert response_post.status_code == 200

#Deleta todos os cadastros
# def test_delete_all_tournament():
    # response = app.test_client().get('/tournament')
    # data = json.loads(response.data.decode('utf-8'))
    
    # response_del = app.test_client().delete(f'tournament')

    # response = app.test_client().get('/tournament')
    # data_after = json.loads(response.data.decode('utf-8'))

    # assert response_del.status_code == 200



