from django.urls import path
from . import views

urlpatterns = [
    path('',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    path('create_user',views.create_user,name='create_user'),
    path('create_department',views.create_department,name='create_department'),
    path('departments',views.departments,name='departments'),
    path('update_department/<int:department_id>',views.update_department,name='update_department'),
    path('delete_department/<int:department_id>',views.delete_department,name='delete_department'),
    path('create_ticket',views.create_ticket,name='create_ticket'),
    path('manage_tickets',views.manage_tickets,name='manage_tickets'),
    path('delete_ticket/<int:ticket_id>',views.delete_ticket,name='delete_ticket'),
]