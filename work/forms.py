from django.forms import ModelForm
from django import forms
from django.forms.models import inlineformset_factory
from django.forms import extras
from .models import Client, ClientAddress, Project, LineItem
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Hidden


class StrainerForm(forms.Form): #Note that it is not inheriting from forms.ModelForm

    xDim = forms.FloatField(
        label = "Horizontal Dimension (inches)",
        required = True,
    )

    yDim = forms.FloatField(
        label = "Vertical Dimension (inches)",
        required = True,
    )

    thickness = forms.FloatField(
        label = "Bar Thickness",
        required = True,
        initial = '1.25',
    )

    quantity = forms.IntegerField(
        label = "Strainer Quantity",
        required = True,
        initial = '1',
    )

    fourQuarter = forms.IntegerField(
        label = "4/4 Board Length",
        required = True,
        initial = '10',
    )

    nineQuarter = forms.IntegerField(
        label = "9/4 Board Length",
        required = True,
        initial = '10',
    )

    def __init__(self, *args, **kwargs):
        super(StrainerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_strainer'
        self.helper.add_input(Submit('submit', 'Submit'))

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'company_name', 'email', 'phone_number',]

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                'first_name',
                'last_name',
                'company_name',
                'phone_number',
                'email',
        )
        self.helper.form_id = 'id-ClientForm'
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_client'
        self.helper.form_tag = False

    def clean(self):
        cleaned_data = super(ClientForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        company_name = cleaned_data.get('company_name')

        if not company_name:
            if not first_name and not last_name and not company_name:
                msg = "You must enter First Name/Last Name or Company Name."
                self.add_error('first_name', '')
                self.add_error('last_name', '')
                self.add_error('company_name', msg)


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


class LineItemSelectorForm(forms.Form):
    CHOICES = [ x for x in LineItem.NameChoices ]
    empty = ('','')
    CHOICES.insert(0, empty)
    tuple(CHOICES)
    LineItemType = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={"onChange":'lineItemSelector(this)'}))


class StrainerItemForm(forms.Form):
    width = forms.CharField(widget=forms.TextInput(attrs={'size':'10'}))
    height = forms.CharField(widget=forms.TextInput(attrs={'size':'10'}))
    thickness = forms.CharField(widget=forms.TextInput(attrs={'size':'10'}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 2}))


class LineItemForm(ModelForm):
    class Meta:

        model = LineItem
        fields = ['order', 'name', 'description', 'price', 'quantity', 'taxable',]
        widgets = {
            'name': forms.Select(attrs={"onChange":'descriptionForm()'}),
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
            'price': forms.TextInput(attrs={'size':'10'}),
            'quantity': forms.TextInput(attrs={'size':'10'}),
        }

LineItemFormSet = inlineformset_factory(Project, LineItem, form=LineItemForm, can_order=True, can_delete=True, extra=0)
