from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.user import User


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        return jsonify({'user:': user.to_dict(
            only=('name', 'about', 'email', 'created_date'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('name', 'about', 'email', 'created_date')) for item in users]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        user = User()
        user.name = args['name']
        user.about = args['about']
        user.email = args['email']
        user.created_date = args['created_date']
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


def abort_if_user_not_found(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        abort(404, message=f'User {user_id} not found')


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('email', required=True)
parser.add_argument('created_date', required=True)
