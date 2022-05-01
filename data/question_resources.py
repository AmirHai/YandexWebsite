from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.question import Question


class QuestionResource(Resource):
    def get(self, question_id):
        abort_if_question_not_found(question_id)
        db_sess = db_session.create_session()
        question = db_sess.query(Question).get(question_id)
        return jsonify({'question': question.to_dict(
            only=('title', 'content', 'user_id', 'created_date'))})

    def delete(self, question_id):
        abort_if_question_not_found(question_id)
        db_sess = db_session.create_session()
        question = db_sess.query(Question).get(question_id)
        db_sess.delete(question)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class QuestionListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        questions = db_sess.query(Question).all()
        return jsonify({'questions': [item.to_dict(
            only=('title', 'content', 'user_id', 'created_date')) for item in questions]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        question = Question()
        question.title = args['title']
        question.content = args['content']
        question.user_id = args['user_id']
        question.created_date = args['created_id']
        db_sess.add(question)
        db_sess.commit()
        return jsonify({'success': 'OK'})


def abort_if_question_not_found(question_id):
    db_sess = db_session.create_session()
    question = db_sess.query(Question).filter(Question.id == question_id)
    if not question:
        abort(404, message=f'Question {question_id} not found')


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('created_date')