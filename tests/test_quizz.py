import unittest
from Quizz.models import Quizz
class QuizzModelTestCase(unittest.TestCase):
    def test_quizz_creation(self):
        # Créez un objet Quizz pour le test
        quizz = Quizz(
            name="Test Quizz",
            description="Test Description",
            number_of_questions=10,
            time=30,
            required_score_to_pass=60,
            difficulty="easy",
        )

        # Vérifiez si les données du quizz sont correctement enregistrées
        self.assertEqual(quizz.name, "Test Quizz")
        self.assertEqual(quizz.description, "Test Description")
        self.assertEqual(quizz.number_of_questions, 10)
        self.assertEqual(quizz.time, 30)
        self.assertEqual(quizz.required_score_to_pass, 60)
        self.assertEqual(quizz.difficulty, "easy")
