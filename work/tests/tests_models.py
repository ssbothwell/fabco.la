from django.test import TestCase
from work.models import Client, ClientAddress, Project, LineItem
from django.utils import timezone
from django.core.urlresolvers import reverse
from work.forms import ClientForm, ClientAddressForm

class DBSetup():
    
    def create_client(self, first_name="foo", last_name="bar", email="foo@bar.com", phone_number=999999999):
        return Client.objects.create(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
    
    def create_project(self):
        return Project.objects.create(client=Client.objects.first(), due_date=timezone.now(), name='test project', status='QT', discount=0, deposit=0)
        
    def create_lineitem(self):
        return LineItem.objects.create(order='0', project=Project.objects.first(), name='test product', description='something that works', price=110.50, quantity=2, taxable=True)
        


class ClientTest(TestCase, DBSetup):

    def test_client_creation(self):
        c = self.create_client()
        self.assertTrue(isinstance(c, Client))
        self.assertEqual(str(c), c.first_name + c.last_name)

    def test_client_project_total(self):
        c = self.create_client()
        p = self.create_project()
        self.assertTrue(isinstance(p, Project))
        
        
class ProjectTest(TestCase, DBSetup):

    def test_client_project_total(self):
        c = self.create_client()
        p = self.create_project()
        l = self.create_lineitem()
        self.assertTrue(isinstance(p, Project))
        self.assertTrue(isinstance(l, LineItem))