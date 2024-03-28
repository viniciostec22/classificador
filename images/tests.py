from django.test import SimpleTestCase
from django.urls import reverse, resolve
from . import views
from django.test import TestCase
from .models import Imagem, Doenca, Analise
from django.contrib.auth.models import User
from django.utils import timezone

class UrlsTest(SimpleTestCase):
    def test_new_images_url_resolves(self):
        url = reverse('new_images')
        self.assertEqual(resolve(url).func, views.images)
    
    def test_galeria_url_resolves(self):
        url = reverse('galeria')
        self.assertEqual(resolve(url).func, views.galeria)
    
    def test_dashboard_url_resolves(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func, views.dashboard)
    
    def test_download_url_resolves(self):
        url = reverse('download')
        self.assertEqual(resolve(url).func, views.download)
class ImagemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Configuração de objetos de teste
        user = User.objects.create_user(username='testuser', password='12345')
        Imagem.objects.create(image='example.jpg', usuario=user)

    def test_image_field(self):
        imagem = Imagem.objects.get(id=1)
        self.assertEqual(imagem.image.name.split('/')[-1], 'example.jpg')


    def test_data_criacao_auto_now_add(self):
        imagem = Imagem.objects.get(id=1)
        self.assertIsNotNone(imagem.data_criacao)
        self.assertLess(imagem.data_criacao, timezone.now())

    def test_classe_default_value(self):
        imagem = Imagem.objects.get(id=1)
        self.assertFalse(imagem.classe)

    def test_usuario_foreign_key(self):
        imagem = Imagem.objects.get(id=1)
        self.assertEqual(imagem.usuario.username, 'testuser')

class DoencaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Configuração de objetos de teste
        Doenca.objects.create(nome='Teste Doenca')

    def test_str_method(self):
        doenca = Doenca.objects.get(id=1)
        self.assertEqual(str(doenca), 'Teste Doenca')

class AnaliseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Configuração de objetos de teste
        user = User.objects.create_user(username='testuser', password='12345')
        doenca = Doenca.objects.create(nome='Teste Doenca')
        imagem = Imagem.objects.create(image='example.jpg', usuario=user)
        Analise.objects.create(imagem=imagem, doenca=doenca, especialista=user)

    def test_data_analise_auto_now_add(self):
        analise = Analise.objects.get(id=1)
        self.assertIsNotNone(analise.data_analise)
        self.assertLess(analise.data_analise, timezone.now())
