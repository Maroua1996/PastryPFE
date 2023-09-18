import unittest
from django.test import Client
from django.urls import reverse
import os


from django.conf import settings  # Importez les paramètres Django
class TestDjangoSettings(unittest.TestCase):
    def setUp(self):
        # Créez un client pour effectuer des requêtes HTTP
        self.client = Client()

    def test_secret_key_not_empty(self):
        # Vérifiez que la clé secrète n'est pas vide
        self.assertNotEqual(settings.SECRET_KEY, '')

    def test_debug_is_false(self):
        # Vérifiez que le débogage n'est pas activé en production
        self.assertFalse(settings.DEBUG)

    def test_allowed_hosts_not_empty(self):
        # Vérifiez que ALLOWED_HOSTS n'est pas vide
        self.assertNotEqual(settings.ALLOWED_HOSTS, [])

    def test_static_url_exists(self):
        # Vérifiez que l'URL statique est configurée
        response = self.client.get(settings.STATIC_URL)
        self.assertEqual(response.status_code, 200)

    def test_media_url_exists(self):
        # Vérifiez que l'URL multimédia est configurée
        response = self.client.get(settings.MEDIA_URL)
        self.assertEqual(response.status_code, 200)

    def test_template_dirs_exists(self):
        # Vérifiez que les répertoires de modèles existent
        for template_dir in settings.TEMPLATES[0]['DIRS']:
            self.assertTrue(os.path.exists(template_dir))

if __name__ == '__main__':
    unittest.main()