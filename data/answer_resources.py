from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.answer import Answer


class AnswerResource(Resource):
    def get(self, answer_id):
        abort_if_answer_not_found(answer_id)
        db_sess = db_session.create_session()
        answer = db_sess.query(Answer).get(answer_id)
        return jsonify({'answer': answer.to_dict(
            only=('content', 'created_date', 'question_id', 'user_id'))})

    def delete(self, answer_id):
        abort_if_answer_not_found(answer_id)
        db_sess = db_session.create_session()
        answer = db_sess.query(Answer).get(answer_id)
        db_sess.delete(answer)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class AnswerListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        answers = db_sess.query(Answer).all()
        return jsonify({'answers': [item.to_dict(
            only=('content', 'created_date', 'question_id', 'user_id')) for item in answers]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        answer = Answer()
        answer.content = args['content']
        answer.created_date = args['created_date']
        answer.question_id = args['question_id']
        answer.user_id = args['user_id']
        db_sess.add(answer)
        db_sess.commit()
        return jsonify({'success': 'OK'})


def abort_if_answer_not_found(answer_id):
    db_sess = db_session.create_session()
    answer = db_sess.query(Answer).get(answer_id)
    if not answer:
        abort(404, message=f'Answer {answer_id} not found')


parser = reqparse.RequestParser()
parser.add_argument('content', required=True)
parser.add_argument('created_date', required=True)
parser.add_argument('question_id', required=True, type=int)
parser.add_argument('user_id', required=True, type=int)