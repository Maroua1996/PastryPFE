
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class EmailLoginTest(TestCase):
    def setUp(self):
        # Créez un utilisateur avec un e-mail et un mot de passe
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            username="testuser",
            password="password123"
        )

    def test_email_login(self):
        # Test de la connexion en utilisant l'e-mail
        login_url = reverse("login")  # Assurez-vous d'utiliser le nom réel de votre vue de connexion
        response = self.client.post(login_url, {
            "username": "test@example.com",  # Utilisez l'e-mail comme identifiant
            "password": "password123",
        })

        # Vérifiez que la connexion a réussi
        self.assertEqual(response.status_code, 302)  # Redirection après la connexion
        self.assertRedirects(response, reverse("home"))  # Assurez-vous d'ajuster le nom de l'URL de redirection après la connexion

    def test_invalid_email_login(self):
        # Test de la connexion avec un e-mail invalide
        login_url = reverse("login")  # Assurez-vous d'utiliser le nom réel de votre vue de connexion
        response = self.client.post(login_url, {
            "username": "nonexistent@example.com",  # E-mail inexistant
            "password": "password123",
        })

        # Vérifiez que la connexion a échoué
        self.assertEqual(response.status_code, 200)  # Page de connexion à nouveau affichée
