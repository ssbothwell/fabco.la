from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone
from django.core.validators import RegexValidator
from decimal import *


class Client(models.Model):
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    company_name = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15) # validators should be a list 
    
    def _projects_total(self):
        """returns sum of client's project totals"""
        p_total = 0
        for project in self.projects.all():
            if project.status == 'WO':
                p_total = p_total + project.total
        return p_total
    projects_total = property(_projects_total)
    
    def __str__(self):
            #return self.first_name + self.last_name
            if self.company_name:
                return self.company_name
            else:
                return u'{1} {0}'.format(self.last_name, self.first_name)
            
class Project(models.Model):
    QUOTE = 'QT'
    WORK_ORDER = 'WO'
    COMPLETE = 'CO'
    STATUS_CHOICES = (
        (QUOTE, 'Quote'),
        (WORK_ORDER, 'Work Order'),
        (COMPLETE, 'Complete'),
        )
        
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    project_id = models.AutoField(primary_key=True)
    create_date = models.DateField('date created', auto_now_add=True)
    due_date = models.DateField('due date', null=True, blank=True)
    completion_date = models.DateField('date completed', null=True, blank=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=QUOTE)
    confirmation_date = models.DateField('confirmation date', null=True, blank=True)
    deposit = models.IntegerField(default=50)
    discount = models.IntegerField(default=0)



    def _project_sub_total(self):
        """returns sum of lineitem totals"""
        p_sub_total = sum(item.tallys['total'] for item in self.line_item.all())
        
            
        return p_sub_total

    def _project_discount(self):
        """returns cash discount based on self.discount"""
        cash_discount = Decimal(0)
        if self.discount > 0:
            cash_discount = self.sub_total * ( Decimal(self.discount) / 100 ) 
        cash_discount = cash_discount.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        return cash_discount
           

    def _project_tax(self):
        """returns 9% tax on sub_total"""
        tax = Decimal(0.00)
        for item in self.line_item.all():
               tax = tax + Decimal(item.tallys['tax'])
        
        return tax


    def _project_total(self):
        """sum sub_total and tax"""
        total = self.tax + (self.sub_total - self.cash_discount)
        
        return total
        
    sub_total = property(_project_sub_total)
    cash_discount = property(_project_discount)
    tax = property(_project_tax)
    total = property(_project_total)

    def __str__(self):
            return self.name
                

NameChoices = (
('Strainer Bar', 'Strainer Bar'),
('Stretching Fee', 'Stretching Fee'),
('Panel', 'Panel'),
('Pedestal', 'Pedestal'),
('Framing', 'Framing'),
('Crating', 'Crating'),
('Welding', 'Welding'),
('Delivery', 'Delivery'),
('Custom', 'Custom'),
)                
                
class LineItem(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='line_item')
    name = models.CharField(max_length=15, choices=NameChoices)
    description = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.PositiveIntegerField(null=True)
    taxable = models.BooleanField(default=True)    
    order = models.IntegerField(blank = True, null = True)
    
    def _get_tallys(self):
        """returns lineitem total, discount, and tax in a dict"""
        item_total = Decimal((self.price * self.quantity))
        cash_discount = Decimal(0.00)     
        tax = Decimal(0.00)
           
        if self.project.discount > 0:
           cash_discount = item_total * ( Decimal(self.project.discount) / 100 )
        
        if self.taxable == True:
            total_post_discount = item_total - cash_discount
            tax = total_post_discount * Decimal(0.09)
            tax = tax.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    
        tallys = {
            'total': item_total,
            'discount': cash_discount,
            'tax': tax,
        }
        
        return tallys
    tallys = property(_get_tallys)
    
    def _get_total(self):
        """ Return just the lineitem total """
        item_total = Decimal((self.price * self.quantity))
        cash_discount = Decimal(0.00)
        
        if self.project.discount > 0:
           cash_discount = item_total * ( Decimal(self.project.discount) / 100 )    
        
        final_total = item_total - cash_discount
        
        return final_total
    total = property(_get_total)
    
    def __str__(self):
            return self.name
            
    class Meta:
        ordering = ('order',)
            
class ClientAddress(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='address')
    street = models.CharField(max_length=40, null=True)
    city = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=10, null=True)
    zip_code = models.CharField(max_length=10, null=True)