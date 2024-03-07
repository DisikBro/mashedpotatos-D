from flask import jsonify
from flask_restful import Resource, abort, reqparse

from mars.data import db_session
from mars.data.users import User


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"News {user_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('age', type=int)
parser.add_argument('position')
parser.add_argument('speciality', required=True)
parser.add_argument('address')
parser.add_argument('email', required=True)


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            rules=('-hashed_password', '-jobs.team_lead_user'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'name', 'surname', 'position')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args.name,
            surname=args.surname,
            age=args.age,
            position=args.position,
            speciality=args.speciality,
            address=args.address,
            email=args.email
        )
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})