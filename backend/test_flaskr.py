import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.user_name = 'postgres'
        self.password = '1234'
        self.database_path = "postgres://{}:{}@{}/{}".format(
            self.user_name, self.password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_questions_pagination(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(data["code"], 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(len(data['categories']))

    def test_give_404_when_page_is_not_existing(self):
        res = self.client().get('/api/questions/?page=10000')
        data = json.loads(res.data)

        self.assertEqual(data['code'], 404)
        self.assertFalse(data["success"])
        self.assertEqual(data['message'], 'resource not found')

    def test_add_question(self):
        previous_questions = Question.query.all()
        new_question = {
            'question': 'question',
            'answer': 'answer',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/api/questions', json=new_question)
        data = json.loads(res.data)
        current_questions = Question.query.all()

        self.assertTrue(data['success'])
        self.assertEqual(data['code'], 201)
        self.assertEqual(len(current_questions), len(previous_questions)+1)

    def test_delete_question(self):
        question = Question(question='question', answer='answer',
                            difficulty=1, category=1)
        question.insert()
        id = question.id

        res = self.client().delete(f'/api/questions/{id}')
        data = json.loads(res.data)

        deleted = Question.query.filter(
            Question.id == id).one_or_none()

        self.assertTrue(data['success'])
        self.assertEqual(data['code'], 200)
        self.assertFalse(deleted)

    def test_delete_non_existing_question(self):
        res = self.client().delete('/api/questions/10000')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['code'], 404)

    def test_search_questions(self):
        new_search = {'searchTerm': 'a'}
        res = self.client().post('/api/questions/search', json=new_search)
        data = json.loads(res.data)

        self.assertEqual(data['code'], 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_422_search_question(self):
        new_search = {
            'searchTerm': '',
        }
        res = self.client().post('/api/questions/search', json=new_search)
        data = json.loads(res.data)

        self.assertEqual(data['code'], 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable")

    def test_get_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data["code"], 200)
        self.assertTrue(data['categories'])

    def test_get_questions_by_category(self):
        res = self.client().get('/api/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(data['code'], 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_questions_by_category(self):
        res = self.client().get('/api/categories/11515/questions')
        data = json.loads(res.data)

        self.assertEqual(data['code'], 404)
        self.assertFalse(data['success'])

    def test_post_quiz(self):
        new_quiz_round = {'previous_questions': [5, 2],
                          'quiz_category': {'type': 'Entertainment', 'id': 5}}

        res = self.client().post('/api/quizzes', json=new_quiz_round)
        data = json.loads(res.data)
        question_id = data['question']['id']
        question_not_in_previous = question_id not in new_quiz_round['previous_questions']

        self.assertEqual(data['code'], 200)
        self.assertTrue(data['success'])
        self.assertTrue(question_not_in_previous)

    def test_422_post_quiz(self):
        new_quiz_round = {'previous_questions': []}
        res = self.client().post('/api/quizzes', json=new_quiz_round)
        data = json.loads(res.data)

        self.assertEqual(data['code'], 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
