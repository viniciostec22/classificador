from django.test import TestCase
from django.urls import reverse

class UsuarioUrlsTest(TestCase):
    def test_url_new_user(self):
        # Verifique se a URL para cadastrar um novo usuário está acessível
        response = self.client.get(reverse('cadastro'))
        self.assertEqual(response.status_code, 302)

    def test_url_login(self):
        # Verifique se a URL para fazer login está acessível
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_url_logout(self):
        # Verifique se a URL para fazer logout redireciona corretamente
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Verifica se é redirecionamento
        self.assertIn('/login/', response.url)  # Verifica se redireciona para a página de login


class SecurityTests(TestCase):
    def test_csrf_protection(self):
        # Verifique se a proteção CSRF está ativada nas visualizações necessárias
        response = self.client.get(reverse('login'))
        self.assertIn('csrfmiddlewaretoken', response.content.decode('utf-8'))
