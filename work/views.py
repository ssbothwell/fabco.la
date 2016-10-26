from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from io import BytesIO
from datetime import date

from lib.printing import MyPrint
from lib.strainerCalc import Strainer
from .models import Client, Project, LineItem, ClientAddress
from .forms import *


@login_required(login_url='/login/')
def StrainerCalc(request):
    if request.method == 'POST':
        strainer_form = StrainerForm(request.POST)
        
        if strainer_form.is_valid():
            strainerData = strainer_form.cleaned_data
            
            strainer = Strainer(strainerData['xDim'], strainerData['yDim'], strainerData['thickness'], strainerData['quantity'], strainerData['fourQuarter'], strainerData['nineQuarter'])
                        
            return render(request, 'work/strainer_form.html', {
                'strainer_form': strainer_form,
                'strainer': strainer, 
                 })
    else:
        strainer_form = StrainerForm()
    
    context = {
        'strainer_form': strainer_form,
     }
    return render(request, 'work/strainer_form.html', context)


@login_required(login_url='/login/')
def ProjectIndexView(request, status):
    """ Display an Index of Projects"""
    projects_list = Project.objects.filter(status=status).order_by('due_date')
    
    context = { 
    'projects_list': projects_list,
    'status': status,
    }
    return render(request, 'work/project_index.html', context)
        
        
@login_required(login_url='/login/')
def ProjectDetailView(request, pk):    
    project = get_object_or_404(Project, pk=pk)
    lineitems = project.line_item.all()
    status_form = ProjectStatusForm(request.POST or None, instance=project)
    
    if status_form.is_valid():
        if project.status == 'WO':
            project.status = 'CO'
            project.completion_date = date.today()
        elif project.status == 'QT':
            project.status = 'WO'
        elif project.status == 'CO':
            project.status = 'WO'
        project.save()
        return redirect('work:project_detail', project.pk)

    context = {
        'project': project,
        'lineitems': lineitems,
        'status_form': status_form,
    }
    return render(request, 'work/project_detail.html', context)


@login_required(login_url='/login/')            
def ProjectCreateView(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            obj1 = project_form.save(commit=False)
            lineitem_formset = LineItemFormSet(request.POST, instance=obj1)
            if lineitem_formset.is_valid():
                obj1.save()
                lineitem_formset.save()
                return redirect ('work:project_detail', obj1.project_id)
    else:
        project_form = ProjectForm()
        lineitem_formset = LineItemFormSet(instance=Project())
    
    
    context = {
        'project_form': project_form,
        'lineitem_formset': lineitem_formset,
    }
    return render(request, 'work/project_form.html', context)


@login_required(login_url='/login/')
def ProjectUpdateView(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project_form = ProjectForm(request.POST or None, instance=project)
    lineitem_formset = LineItemFormSet(request.POST or None, instance=project)
    
    if project_form.is_valid():
        project_object = project_form.save(commit=False)
        if lineitem_formset.is_valid():
            project_object.save()
            lineitem_formset.save()
        return redirect('work:project_detail', project.pk)
    else:
        project_object = ProjectForm(instance=project)
    
    context = {
            'project_form': project_form,
            'lineitem_formset': lineitem_formset,
        }    
    return render(request, 'work/project_form.html', context)

@login_required(login_url='/login/')    
def PrintPdfView(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
 
    buffer = BytesIO()
 
    report = MyPrint(buffer, 'Letter', pk)
    if project.status == 'QT':
        response['Content-Disposition'] = 'inline; filename="%s-Quote-%s.pdf"' % (project.client, project.project_id)
        pdf = report.print_quote()
    else:
        response['Content-Disposition'] = 'inline; filename="%s-WorkOrder-%s.pdf"' % (project.client, project.project_id)
        pdf = report.print_work_order()    
        
    
    response.write(pdf)
    return response


@login_required(login_url='/login/')    
def ProjectDeleteView(request, pk):
    project = Project.objects.get(pk=pk)
    status = str(project.status)
    index_dict = {
        'QT': 'work:quote_index',
        'WO': 'work:work_order_index',
        'CO': 'work:complete_index',
    }
    
    project.delete()
    return redirect(index_dict[status])


@login_required(login_url='/login/')
def ClientIndex(request):
    clients_list = Client.objects.all().order_by('first_name')
    
    context = { 
    'clients_list': clients_list,
    }
    return render(request, 'work/client_index.html', context)


@login_required(login_url='/login/')
def ClientDetailView(request, pk):
    try:
        client = Client.objects.get(pk=pk)
        completed = client.projects.filter(status='CO')
        quotes = client.projects.filter(status='QT')
        work_order = client.projects.filter(status='WO')
    except Client.DoesNotExist:
        raise Http404("Client does not exist")
        
    context = {
        'client': client,
        'quotes': quotes,
        'work_order': work_order,
        'completed': completed,
    }
    return render(request, 'work/client_detail.html', context)


@login_required(login_url='/login/')
def ClientCreateView(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        address_form = ClientAddressForm(request.POST)
        if all([client_form.is_valid(), address_form.is_valid()]):
            obj1 = client_form.save()
            obj2 = address_form.save(commit=False)
            obj2.client = obj1
            obj2.save()
            return redirect('work:client_index')
            
    else:
        client_form = ClientForm()
        address_form = ClientAddressForm()
        
    context = {
        'client_form': client_form,
        'address_form': address_form,
    }
    return render(request, 'work/client_form.html', context)


@login_required(login_url='/login/')
def ClientUpdateView(request, pk):
    client = Client.objects.get(pk=pk)
    client_form = ClientForm(request.POST or None, instance=client)
    address_form = ClientAddressForm(request.POST or None, instance=client.address)
    if all([client_form.is_valid(), address_form.is_valid()]):
        client_object = client_form.save()
        address_object = address_form.save(commit=False)
        address_object.client = client_object
        address_object.save()
        return redirect('work:client_index')
    else:
        form = ClientForm(initial={'first_name': client.first_name, 'last_name': client.last_name})
    
    context = {
            'client_form': client_form,
            'address_form': address_form,
    }
    return render(request, 'work/client_form.html', context)
                            

@login_required(login_url='/login/')    
def ClientDeleteView(request, pk):
    client = Client.objects.get(pk=pk)
    client.delete()

    return redirect('work:client_index')

   
@login_required(login_url='/login/')
def ReportView(request):
    projects = Project.objects.filter(status='CO')
    
    p1 = Project.objects.filter(completion_date__range=["2016-01-01", "2016-12-31"])
    
    quarterOne = 0
    quarterTwo = 0
    quarterThree = 0
    quarterFour = 0
    
    for p in projects: 
        if date(2016,01,01) <= p.completion_date <= date(2016,3,31):
            quarterOne += p.tax
        if date(2016,04,01) <= p.completion_date <= date(2016,6,30):
            quarterTwo += p.tax
        if date(2016,07,01) <= p.completion_date <= date(2016,9,30):
            quarterThree += p.tax        
        if date(2016,10,01) <= p.completion_date <= date(2016,12,31):
            quarterFour += p.tax
 
    Quarterlies = {
                    "quarterOne": quarterOne,
                    "quarterTwo": quarterTwo,
                    "quarterThree": quarterThree,
                    "quarterFour": quarterFour,
                }

    # These month strings are just filler, shouldn't be necessary but idk a better way
    months = [ 'null', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ]
    
    # Replace filler month strings with lineItem type dict for each month
    for int in range(1, 13):
        months[int] = { 
                    'strainerBars': 0,
                    'panels': 0,
                    'stretchingFee': 0,
                    'pedestals': 0,
                    'framing': 0,
                    'crating': 0,
                    'welding': 0,
                    'custom': 0,
                    }
    
    # Loop through months and for each month loop through lineItems completed in that month and aggregate them into the months list
    for month in range (1, 13):
        lineItems = LineItem.objects.filter(project__completion_date__year=2016, project__completion_date__month=month)
        for item in lineItems:
            if item.name == "Strainer Bar":
                months[month]['strainerBars'] += (item.tallys['total'] -  item.tallys['discount'])
            if item.name == "Panel":
                months[month]['panels'] += item.tallys['total'] -  item.tallys['discount']
            if item.name == "Stretching Fee":
                months[month]['stretchingFee'] += item.tallys['total'] -  item.tallys['discount']
            if item.name == "Pedestal":
                months[month]['pedestals'] += item.tallys['total'] -  item.tallys['discount']
            if item.name == "Framing":
                months[month]['framing'] += item.tallys['total'] -  item.tallys['discount']
            if item.name == "crating":
                months[month]['crating'] += item.tallys['total'] -  item.tallys['discount']  
            if item.name == "welding":
                months[month]['welding'] += item.tallys['total'] -  item.tallys['discount']
            if item.name == "custom":
                months[month]['custom'] += item.tallys['total'] -  item.tallys['discount']
            
    # Kinda dumb but it works way of naming the nested dicts in the month list
    MonthlyStats = {
            "January": months[1],
            "February": months[2],
            "March": months[3],
            "April": months[4],
            "May": months[5],
            "June": months[6],
            "July": months[7],
            "August": months[8],
            "September": months[9],
            "October": months[10],
            "November": months[11],
            "December": months[12],
    }
    
    context = {
             'projects': projects,
             'Quarterlies': Quarterlies,
             'MonthlyStats': MonthlyStats,
    }
    return render(request, 'work/report_detail.html', context)