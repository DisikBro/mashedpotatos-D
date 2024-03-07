import pytest
import requests

from mars.data import db_session
from mars.data.users import User

url = 'http://127.0.0.1:5000/api/v2'


@pytest.fixture
def db_init():
    db_session.global_init('db/mars_explorer.db')


def test_get_users_list(db_init):
    response = requests.get(url + '/users')
    session = db_session.create_session()
    users = session.query(User).all()
    answer = {'users': [item.to_dict(
        only=('id', 'name', 'surname', 'position')
    ) for item in users]}
    assert response.json() == answer


def test_get_user(db_init):
    response = requests.get(url + '/user/1')
    session = db_session.create_session()
    user = {'user': session.query(User).get(1).to_dict(
        rules=('-hashed_password', '-jobs.team_lead_user'))
    }
    assert response.json() == user


def test_get_user_wrong_id(db_init):
    response = requests.get(url + '/user/100')
    assert response.json() == {"message": "User 100 not found"}


def test_get_user_wrong_path(db_init):
    response = requests.get(url + '/user/asdfg')
    assert response.json() == {"error": "Not found"}


def test_delete_user(db_init):
    response = requests.delete(url + '/user/1')
    assert response.json() == {"success": "OK"}


def test_delete_user_wrong_id(db_init):
    response = requests.delete(url + '/user/100')
    assert response.json() == {"message": "User 100 not found"}


def test_delete_user_wrong_path(db_init):
    response = requests.delete(url + '/user/asdfg')
    assert response.json() == {"error": "Not found"}


def test_add_user(db_init):
    data = {
        'id': 1,
        'name': 'qwert',
        'surname': 'asdf',
        'position': 'zxcv',
        'speciality': 'speciality',
        'email': 'email@mail.ru'
    }
    response = requests.post(url + '/users', json=data)
    assert response.json() == {'id': 1}


def test_add_user_missing_required(db_init):
    data = {
        'id': 1,
        'surname': 'asdf',
        'speciality': 'speciality',
        'email': 'email@mail.ru'
    }
    response = requests.post(url + '/users', json=data)
    assert response.json() == {'message': {'name': 'Missing required parameter in the JSON body or the post '
                                                   'body or the query string'}}


def test_add_user_invalid_literal(db_init):
    data = {
        'id': 'a',
        'surname': 'asdf',
        'speciality': 'speciality',
        'email': 'email@mail.ru'
    }
    response = requests.post(url + '/users', json=data)
    assert response.json() == {'message': {'id': "invalid literal for int() with base 10: 'a'"}}
