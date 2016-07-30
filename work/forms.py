from django.forms import ModelForm
from django import forms
from django.forms.models import inlineformset_factory
from django.forms import extras
from .models import Client, ClientAddress, Project, LineItem
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone_number']


    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                'first_name',
                'last_name',
                'phone_number',
                'email',
        )
        self.helper.form_id = 'id-ClientForm'
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_client'
        self.helper.form_tag = False
               

class ClientAddressForm(ModelForm):
    class Meta:
        model = ClientAddress
        fields = ['street', 'city', 'state', 'zip_code']

    def __init__(self, *args, **kwargs):
        super(ClientAddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-ClientForm'
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_client'
        self.helper.form_tag = False        
        self.helper.add_input(Submit('submit', 'Submit'))
        
        
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['client', 'due_date', 'name', 'status', 'discount','deposit']
    

class ProjectStatusForm(ModelForm):
    class Meta:
        model = Project
        fields = ['status']


class LineItemForm(ModelForm):
    class Meta:
        model = LineItem
        fields = ['order', 'name', 'description', 'price', 'quantity', 'taxable',]
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
            'price': forms.TextInput(attrs={'size':'10'}),
            'quantity': forms.TextInput(attrs={'size':'10'}),            
        }
        
   
LineItemFormSet = inlineformset_factory(Project, LineItem, form=LineItemForm, can_delete=True, extra=1)