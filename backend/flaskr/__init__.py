from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def random_element(lst: list):
    rand_idx = random.randint(0, len(lst))
    return lst[rand_idx]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Reference for CORS as well as after_request decorator implementation
    # was got from CORS implementation lesson
    CORS(app, resources={"/*": {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow', 'Content-Type')
        response.headers.add('Access-Control-Allow', 'GET, POST, DELETE')
        return response

    @app.route('/categories', methods=['GET'])
    def categories():
        all_categories = Category.query.all()
        data = [category.format() for category in all_categories]

        return jsonify({
            'success': True,
            'categories': data,
            'total_categories': len(data)
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = [question.format() for question in Question.query.all()]

        # Reference for pagination was got from
        # https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/4b381563-32ec-4194-bc15-9c7c22a8578d/concepts/4aaf6823-97ed-4e1d-aaa1-44e9e9b2f81f
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10  # 10 -> number of questions per page
        end = start + 10

        if questions[start:end]:
            return jsonify({
                'questions': questions[start:end],
                'total_questions': len(questions),
                'categories': [category.name for category in Category.query.all()]
            })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id)
        if not question:
            abort(404)

        error = False
        try:
            db.session.delete(question)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

        if not error:
            return jsonify({
                'success': True,
                'message': "Question deleted successfully."
            })

    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()

        if not data:
            abort(422)

        try:
            name = data['question']
            answer = data['answer']
            difficulty = data['difficulty']
            category = data['category']

            new_question = Question(question=name, answer=answer, category=category, difficulty=difficulty)
            db.session.add(new_question)
            db.session.commit()
        except:
            abort(500)
        finally:
            db.session.close()

        return jsonify({
            'success': True,
            'message': "New Question has been added."
        })

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        search_term = request.get_json()['search_term']
        if not search_term:
            abort(422)

        data = [question.format() for question in Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()]

        return jsonify({
            'questions': data,
            'total_questions': len(data),
        })

    @app.route('/category/<int:category_id>', methods=['GET'])
    def get_by_category(category_id):

        # category_questions --> all questions related to given category
        category_questions = Question.filter_by(category=Category.query.get(category_id))

        # formatted questions ready to be shared
        data = [question.format() for question in category_questions]

        # Reference for pagination was got from
        # https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/4b381563-32ec-4194-bc15-9c7c22a8578d/concepts/4aaf6823-97ed-4e1d-aaa1-44e9e9b2f81f
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10  # 10 -> number of questions per page
        end = start + 10

        if data[start:end]:
            return jsonify({
                'success': True,
                'questions': data[start:end],
                'total_questions': len(data),
                'current_category': Category.query.get(category_id).type,
            })
        else:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        global new_question

        if not request.method == 'POST':
            abort(405)

        quiz_data = request.get_json()

        question_ids = [question.id for question in Question.query.filter_by(category=quiz_data['quizCategory']['id'])]

        try:
            while new_question.id in quiz_data['previousQuestions']:
                new_question = Question.query.get(random_element(question_ids))
        except RuntimeError or RuntimeWarning:
            abort(422)

        return jsonify({
            'question': new_question.format(),
            'success': True
        })

    @app.errorhandler(404)
    def client_error_404(e):
        return jsonify({
            'status_code': 404,
            'message': "Resource Not Found.",
            'success': False
        })

    @app.errorhandler(422)
    def client_error_422(e):
        return jsonify({
            'status_code': 422,
            'message': "Request is Not Processable.",
            'success': False
        })

    @app.errorhandler(500)
    def server_error_500(e):
        return jsonify({
            'status_code': 500,
            'message': "Internal Server Error",
            'success': False
        })

    return app
