import os
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib import messages
from .forms import UserCreateForm, DepartmentCreateForm,NewTicketForm
from .models import User,Department,UserManager
import requests
import json
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from dotenv import load_dotenv


load_dotenv()
# Create your views here.
def signin(request):
    if request.method == 'POST':
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get('password')
        user = UserManager().authenticate(email_or_phone = email_or_phone, password = password)
        if user is not None:
            login(request,user)
            return redirect('create_ticket')
        else:
            messages.error(request,'Invalid credentials')

    return render(request,'support/signin.html')

# @login_required('sigin')
def signout(request):
    logout(request)
    return redirect('signin')

def create_user(request):
    if request.user.is_staff:

        if request.method == 'POST':
            form = UserCreateForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.created_by = request.user
                user.is_staff = False
                user.save()
                messages.success(request,'User is created successfully.')
        else:
            form = UserCreateForm()
        context = {'form':form}
        return render(request,'support/create_user.html',context)
    else:
        messages.error(request,'You are not authorized to create User')
        return redirect('signin')

def departments(request):
    context = {'departments':Department.objects.all()}
    return render(request,'support/departments.html',context)


# @permission_classes([IsAdminUser])
def create_department(request):
    if request.user.is_staff:

        if request.method == 'POST':
            form = DepartmentCreateForm(request.POST)
            if form.is_valid():
                dep = form.save()
                dep.created_by = request.user
                messages.success(request,'Department is created successfully.')
                return redirect('create_department')
        else:
            form = DepartmentCreateForm()
        context = {'form':form}
        return render(request,'support/create_department.html',context)
    else:
        messages.error(request,'You are not authorized to create department')
        return redirect('signin')

def update_department(request, department_id):
    if request.user.is_staff:
        department = get_object_or_404(Department, pk=department_id)
        if request.method == 'POST':
            form = DepartmentCreateForm(request.POST, instance=department)
            if form.is_valid():
                form.save()
                messages.success(request,'Department is Updated.')
                return redirect('departments')
        else:
            form = DepartmentCreateForm(instance=department)
        return render(request, 'support/create_department.html', {'form': form})
    else:
        messages.error(request,'You are not authorized to Update department')
        return redirect('signin')

def delete_department(request, department_id):
    if request.user.is_staff:
        department = get_object_or_404(Department, pk=department_id)
        if department.user_set.count() == 0:
            department.delete()
            return redirect('departments')
        else:
            messages.error(request,'Department is associated with some user, it cannot be deleted.')
            return redirect('departments')
    else:
        messages.error(request,'You are not authorized to Delete department')
        return redirect('signin')


def create_ticket(request):
    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            priority = form.cleaned_data['priority']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']

            data = {
                'ticket': {
                    'subject': subject, 
                    'comment': {'body': body},
                    'priority': priority,
                    'requester': {'name':email.split('@')[0],'email':email, "phone": phone_number },
                    }}

            payload = json.dumps(data)

            # Set the request parameters
            print("djcekjf")
            url = 'https://brototype1521.zendesk.com/api/v2/tickets.json'
            print('qqqqqqqq')
            user = 'mmt7025@gmail.com'
            
            pwd = 'mufli@123'

            headers = {'content-type': 'application/json'}

            response = requests.post(url, data=payload, auth=(user, pwd), headers=headers)


            if response.status_code == 201:
                messages.success(request, 'Ticket created successfully')
                return redirect('create_ticket')
            else:
                messages.error(request, 'Failed to create ticket')
                return redirect('create_ticket')
    else:
        form = NewTicketForm(initial={
            'email': request.user.email,
            'phone_number': request.user.phone
        })
    return render(request, 'support/create_ticket.html', {'form': form})


def manage_tickets(request):
    # Fetch list of all tickets within organization
    if request.user.is_staff:
        # Set the request parameters
        url = 'https://brototype1521.zendesk.com/api/v2/tickets.json'
        user = 'mmt7025@gmail.com'
        pwd = 'mufli@123'

        response = requests.get(url, auth=(user,pwd))
        tickets = response.json()['tickets']
    else:
        email = request.user.email
        url = f'https://brototype1521.zendesk.com/api/v2/search.json?query=type:ticket requester:{email}'
        user = 'mmt7025@gmail.com'
        pwd = 'mufli@123'
        response = requests.get(url, auth=(user,pwd))
        tickets = response.json()['results']

    return render(request, 'support/manage_tickets.html', {'tickets': tickets})

def delete_ticket(request, ticket_id):
    if request.user.is_staff:
        # Set the request parameters
        url = f'https://brototype1521.zendesk.com/api/v2/tickets/{ticket_id}.json'
        user = 'mmt7025@gmail.com'
        pwd = 'mufli@123'
        response = requests.delete(url, auth=(user,pwd))


        if response.status_code == 200 or response.status_code == 204:
            messages.success(request, 'Ticket deleted successfully')
            return redirect('manage_tickets')
        else:
            messages.error(request, 'Failed to delete ticket')
            return redirect('manage_tickets')
    else:
        messages.error(request,'You are not authorized to Delete Tickets')
        return redirect('signin')