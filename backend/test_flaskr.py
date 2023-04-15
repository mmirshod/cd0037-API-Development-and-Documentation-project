import json
import unittest
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from backend.flaskr.models import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            "localhost:5432", self.database_name
        )
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

    def test_get_all_categories(self):
        """Get list of all Categories"""

        res = self.client().get("/categories")
        data = res.data

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertIs(data["total_categories"], int)

    def test_get_all_questions(self):
        """Get list of all Questions"""

        res = self.client().get()
        data = res.data

        self.assertEqual(res.status_code, 200)
        self.assertIs(data["questions"], list)
        self.assertTrue(data["total_questions"])
        self.assertIs(data["total_questions"], int)

    def test_delete_question_with_id(self):
        """Delete specific question with given Question ID"""

        res = self.client().delete("/questions/1")
        data = res.data

        self.assertEqual(data["success"], True)
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
        data = res.data

        self.assertEqual(res.status_code, 200)
        self.assertIs(data["message"], str)

    def test_search_question_with_user_input(self):
        """Search questions based on User's prompt"""

        res = self.client().post(
            "/questions/search", json={"search_term": "Capital of USA"}
        )

        self.assertEqual(res.status_code, 200)
        self.assertIs(res.data["questions"], list)
        self.assertEqual(len(res.data["questions"]), res.data["total_questions"])

    def test_get_questions_by_category(self):
        """Get Questions by category and implemented pagination"""

        res = self.client().get("/category/1")

        self.assertEqual(res.status_code, 200)
        self.assertIs(res.data["questions"], list)
        self.assertIs(res.data["current_category"], str)

    # Errors
    def test_get_client_error_422(self):
        """Get handled message for 422 Not Processable error"""

        res = self.client().post("/questions", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertDictEqual(
            data,
            {
                "status_code": 422,
                "message": "Request is Not Processable.",
                "success": False,
            },
        )

    def test_create_new_question_fail(self):
        """Test for Creating new question based given data, failure scenario"""

        res = self.client().post(
            "/questions", json={"question": "question_name", "difficulty": 5}
        )  # missing data
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertDictEqual(
            data,
            {"status_code": 500, "message": "Internal Server Error", "success": False},
        )

    def test_get_all_categories_fail(self):
        """Test for failure scenario of Getting all categories"""
        res = self.client().get(
            "/category"
        )  # Misspelling the route, i.e. user typed route by himself

        self.assertEqual(res.status_code, 404)

    def test_delete_question_with_id_fail(self):
        """Test for failure of Deleting record with ID"""
        res = self.client().delete("/questions/1000")  # ID not found in the DB
        data = res.data

        self.assertEqual(res.status_code, 404)
        self.assertDictEqual(
            data,
            {"status_code": 404, "message": "Resource Not Found.", "success": False},
        )

    def test_search_question_with_user_input_fail(self):
        # Misspelling the route
        res = self.client().post("/question/search", json={})  # No data provided
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertDictEqual(
            data,
            {
                "status_code": 422,
                "message": "Request is Not Processable.",
                "success": False,
            },
        )

    def test_get_questions_by_category_fail(self):
        res = self.client().get("/category/99999999")
        data = res.data

        self.assertEqual(res.status_code, 404)
        self.assertDictEqual(
            data,
            {"status_code": 404, "message": "Resource Not Found.", "success": False},
        )

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
                ]
            },
        )
        data = res.data

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
        self.assertEqual(res.request.method, "PUT")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
