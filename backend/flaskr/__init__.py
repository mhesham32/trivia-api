import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(req, selection):
    page_num = req.args.get('page', 1, type=int)
    start = (page_num - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    all_questions = [question.format() for question in selection]
    current_questions = all_questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/api/categories')
    def get_categories():
        all_categories = Category.query.all()
        formatted_categories = {}
        for category in all_categories:
            formatted = category.format()
            formatted_categories[formatted['id']] = formatted['type']
        return jsonify({"categories": formatted_categories, "success": True, "code": 200})

    @app.route('/api/questions')
    def get_questions():
        selection = Question.query.all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.all()

        formatted_categories = {}
        for category in categories:
            formatted = category.format()
            formatted_categories[formatted['id']] = formatted['type']

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            "questions": current_questions,
            "total_questions": len(selection),
            "categories": formatted_categories,
            "current_category": categories[0].format(),
            "success": True,
            "code": 200
        })

    @app.route('/api/questions/<int:id>', methods=["DELETE"])
    def delete_question(id):
        question = Question.query.get(id)

        if question:
            question.delete()
        else:
            abort(404)

        return jsonify({
            "success": True,
            "code": 200,
        })

    @app.route('/api/questions', methods=["POST"])
    def add_question():
        body = request.get_json()
        question = body.get('question')
        answer = body.get('answer')
        difficulty = int(body.get("difficulty"))
        category = int(body.get("category"))

        try:
            new_question = Question(question, answer, category, difficulty)
            new_question.insert()

            return jsonify({
                "success": True,
                "code": 201
            })
        except:
            abort(422)

    @app.route('/api/questions/search', methods=["POST"])
    def search_questions():
        search_term = request.get_json().get("searchTerm")
        if search_term:
            result = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            return jsonify({
                'success': True,
                'questions': [question.format() for question in result],
                'total_questions': len(result),
                'current_category': None,
                "code": 200
            })
        abort(422)

    @app.route('/api/categories/<int:id>/questions')
    def get_questions_by_category(id):
        questions = Question.query.filter(Question.category == id).all()
        category = Category.query.get(id)
        formatted_category = None

        if category:
            formatted_category = category.format()

        if len(questions) == 0 and not formatted_category:
            abort(404)

        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'total_questions': len(questions),
            'current_category': formatted_category,
            "code": 200
        })

    @app.route('/api/quizzes', methods=["POST"])
    def get_quiz_question():
        try:
            body = request.get_json()
            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            questions = Question.query.filter(
                Question.category == quiz_category['id']).all()
            questions_list = [question.format() for question in questions]
            filtered_questions = []

            for q in questions_list:
                if q['id'] not in previous_questions:
                    filtered_questions.append(q)

            if len(filtered_questions):
                question = filtered_questions[0]
            else:
                question = None

            return jsonify({
                "success": True,
                "code": 200,
                "question": question
            })
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "code": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "code": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "code": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "code": 500,
            "message": "internal server Error"
        }), 500

    return app
