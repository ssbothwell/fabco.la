from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from io import BytesIO

from work.printing import MyPrint
from .models import Client, Project, LineItem, ClientAddress
from .forms import *


@login_required(login_url='/login/')
def ProjectIndexView(request, status):
    """ Display an Index of Projects"""
    projects_list = Project.objects.filter(status=status)
    status = status
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
    return render(request, 'work/project_form.html', {
        'project_form': project_form,
        'lineitem_formset': lineitem_formset,
     })


@login_required(login_url='/login/')
def ProjectUpdateView(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project_form = ProjectForm(request.POST or None, instance=project)
    lineitem_formset = LineItemFormSet(request.POST or None, instance=project)
    
    if project_form.is_valid():
        obj1 = project_form.save(commit=False)
        if lineitem_formset.is_valid():
            obj1.save()
            lineitem_formset.save()
        return redirect('work:project_detail', project.pk)
    else:
        obj1 = ProjectForm(instance=project)
        
    return render(request, 'work/project_form.html', {
            'project_form': project_form,
            'lineitem_formset': lineitem_formset,
        })

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
    clients_list = Client.objects.all()
    context = { 
    'clients_list': clients_list,
    }
    return render(request, 'work/client_index.html', context)


@login_required(login_url='/login/')
def ClientDetailView(request, pk):
    try:
        client = Client.objects.get(pk=pk)
        projects = client.projects.all()
    except Client.DoesNotExist:
        raise Http404("Client does not exist")
    context = {
        'client': client,
        'projects': projects,
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
    return render(request, 'work/client_form.html', {
        'client_form': client_form,
        'address_form': address_form,
    })


@login_required(login_url='/login/')
def ClientUpdateView(request, pk):
    client = Client.objects.get(pk=pk)
    client_form = ClientForm(request.POST or None, instance=client)
    address_form = ClientAddressForm(request.POST or None, instance=client.address)
    if all([client_form.is_valid(), address_form.is_valid()]):
        obj1 = client_form.save()
        obj2 = address_form.save(commit=False)
        obj2.client = obj1
        obj2.save()
        return redirect('work:client_index')
    else:
        form = ClientForm(initial={'first_name': client.first_name, 'last_name': client.last_name})

    return render(request, 'work/client_form.html', {
            'client_form': client_form,
            'address_form': address_form,
        })
                            

@login_required(login_url='/login/')    
def ClientDeleteView(request, pk):
    client = Client.objects.get(pk=pk)
    client.delete()

    return redirect('work:client_index')

    
