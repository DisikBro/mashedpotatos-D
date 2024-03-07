import pytest
import requests

from mars.data import db_session
from mars.data.jobs import Jobs

url = 'http://127.0.0.1:5000/api'


@pytest.fixture()
def db_init():
    db_session.global_init("db/mars_explorer.db")


def test_all_jobs(db_init):
    response = requests.get(url + '/jobs')
    db_sess = db_session.create_session()
    jobs = {
            'jobs':
                [item.to_dict(only=('job', 'work_size', 'is_finished', 'team_lead_user.surname'))
                 for item in db_sess.query(Jobs).all()]
        }
    assert response.json() == jobs


def test_one_job(db_init):
    response = requests.get(url + '/jobs/1')
    db_sess = db_session.create_session()
    jobs = {
        'jobs': db_sess.query(Jobs).get(1).to_dict(rules=('-team_lead_user.jobs',))
    }
    assert response.json() == jobs


def test_one_wrong_id(db_init):
    response = requests.get(url + '/jobs/123')
    assert response.json() == {"error": "Not found"}


def test_one_wrong_path(db_init):
    response = requests.get(url + '/jobs/aaa')
    assert response.json() == {"error": "Not found"}
