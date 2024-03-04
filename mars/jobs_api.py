import flask

from mars.data import db_session
from flask import jsonify, make_response

from mars.data.jobs import Jobs

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('job', 'work_size', 'is_finished', 'team_lead_user.surname'))
                 for item in jobs]
        }
    )


@blueprint.route('/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobs_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'job': job.to_dict(rules=('-team_lead_user.jobs',))
        }
    )
