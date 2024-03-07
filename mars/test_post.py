import pytest
import requests

from mars.data import db_session
from mars.data.jobs import Jobs

url = 'http://127.0.0.1:5000/api'


@pytest.fixture
def db_init():
    db_session.global_init('db/mars_explorer.db')


def test_add_job(db_init):
    job_data = {'team_lead': 1,
                'job': 'Очень важное задание',
                'work_size': 5,
                'collaborators': '3, 4'}
    response = requests.post(url + '/jobs', json=job_data)
    db_sess = db_session.create_session()
    assert response.json() == {'id': db_sess.query(Jobs).all()[-1].id}


def test_add_empty(db_init):
    job_data = {}
    response = requests.post(url + '/jobs', json=job_data)
    assert response.json() == {'error': 'Empty request'}


def test_add_bad(db_init):
    job_data = {'job': 'Очень важное задание', 'work_size': 5}
    response = requests.post(url + '/jobs', json=job_data)
    assert response.json() == {'error': 'Bad request'}
