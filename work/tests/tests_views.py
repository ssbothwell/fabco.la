from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from work.models import Client as WorkClient


class ClientViewsTestCase(TestCase):
    
    def setUp(self):
      self.client = Client()
      self.username = 'test_user'
      self.email = 'test@test.com'
      self.password = 'test'        
      self.test_user = User.objects.create_user(self.username, self.email, self.password)
      login = self.client.login(username=self.username, password=self.password)
      self.assertEqual(login, True)
   
    
    def test_call_view_denies_anonymous(self):
        self.client.logout()
        response = self.client.get('/work/clients/')
        self.assertRedirects(response, '/login/?next=/work/clients/')

        
    def test_client_index_loads(self):
        self.client.login(username='test_user', password='test')
        resp = self.client.get('/work/clients/')
        self.assertEqual(resp.status_code, 200)


class ProjectViewsTestCaste(TestCase):
    
    def setUp(self):
      self.client = Client()
      self.username = 'test_user'
      self.email = 'test@test.com'
      self.password = 'test'        
      self.test_user = User.objects.create_user(self.username, self.email, self.password)
      login = self.client.login(username=self.username, password=self.password)
      self.assertEqual(login, True)
      
     
    def test_call_view_denies_anonymous(self):
        self.client.logout()
        response = self.client.get('/work/clients/')
        self.assertRedirects(response, '/login/?next=/work/clients/')

       
    def test_project_index_loads(self):
        self.client.login(username='test_user', password='test')
        resp = self.client.get('/work/projects/quotes')
        self.assertEqual(resp.status_code, 200)