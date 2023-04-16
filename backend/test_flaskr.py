import json
import os
import unittest
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = os.getenv("DB_NAME", "trivia_test")
        # self.database_user = os.getenv("DB_USER", "postgres")
        # self.database_password = os.getenv("DB_PASSWORD", " ")
        # self.database_host = os.getenv("DB_HOST", "127.0.0.1:5432")
        # self.database_path = "postgresql+psycopg2://{}:{}@{}/{}".format(
        #     self.database_user, self.database_password, self.database_host, self.database_name
        # )
        #
        # setup_db(self.app, self.database_path)

        # binds the app to the current context
        self.db = db

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_categories(self):
        """Get list of all Categories"""

        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIs(data["total_categories"], int)

    def test_get_all_questions(self):
        """Get list of all Questions"""

        res = self.client().get()
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIs(data["total_questions"], int)

    def test_delete_question_with_id(self):
        """Delete specific question with given Question ID"""

        res = self.client().delete("/questions/1")
        data = json.loads(res.data)

        self.assertTrue(data["success"])
        self.assertIs(data["message"], str)

    def test_create_new_question(self):
        """Create New Question with the given JSON data"""

        res = self.client().post(
            "/questions",
            json={
                "question": "Test Case",
                "answer": "Answer to the test case",
                "difficulty": 3,
                "category": "sample category",
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIs(data["message"], str)

    def test_search_question_with_user_input(self):
        """Search questions based on User's prompt"""

        res = self.client().post(
            "/questions/search", json={"search_term": "Capital of USA"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIs(data["questions"], list)

    def test_get_questions_by_category(self):
        """Get Questions by category and implemented pagination"""

        res = self.client().get("/category/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIs(data["current_category"], str)

    def test_get_client_error_422(self):
        """Get handled message for 422 Not Processable error"""

        res = self.client().post("/questions", json={})
        data = json.loads(res.data)

        self.assertFalse(data["success"])
        self.assertEqual(data["status_code"], 422)
        self.assertEqual(res.status_code, 200)

    def test_create_new_question_fail(self):
        """Test for Creating new question based given data, failure scenario"""

        res = self.client().post(
            "/questions", json={"question": "question_name", "difficulty": 5}
        )  # missing data
        data = json.loads(res.data)

        self.assertEqual(data["status_code"], 500)
        self.assertFalse(data["success"])
        self.assertEqual(res.status_code, 200)

    def test_get_all_categories_fail(self):
        """Test for failure scenario of Getting all categories"""
        res = self.client().get(
            "/category"
        )  # Misspelling the route, i.e. user typed route by himself

        self.assertEqual(json.loads(res.data)["status_code"], 404)
        self.assertEqual(res.status_code, 200)

    def test_delete_question_with_id_fail(self):
        """Test for failure of Deleting record with ID"""
        res = self.client().delete("/questions/1000")  # ID not found in the DB
        data = json.loads(res.data)

        self.assertEqual(data["status_code"], 404)
        self.assertFalse(data["success"])
        self.assertEqual(res.status_code, 200)

    def test_search_question_with_user_input_fail(self):
        # Misspelling the route
        res = self.client().post("/question/search", json={})  # No data provided
        data = json.loads(res.data)

        self.assertEqual(data["status_code"], 422)
        self.assertFalse(data["success"])

    def test_get_questions_by_category_fail(self):
        res = self.client().get("/category/99999999")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["status_code"], 404)
        self.assertIs(data["message"], str)
        self.assertFalse(data["success"])

    def test_play_quiz_success(self):
        res = self.client().post(
            "/quizzes",
            json={
                "previousQuestions": [
                    {
                        "id": 1,
                        "question": "question_name",
                        "answer": "answer",
                        "category": "Classic",
                        "difficulty": 4,
                    }
                ],
                "quizCategory": {
                    "type": "Classic",
                    "id": 1
                }
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIs(data["question"], dict)

    def test_play_quiz_fail(self):
        res = self.client().put(
            "/quizzes",
            json={
                "previousQuestions": [
                    {
                        "id": 1,
                        "question": "question_name",
                        "answer": "answer",
                        "category": "Classic",
                        "difficulty": 4,
                    }
                ]
            },
        )
        self.assertEqual(res.status_code, 405)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
