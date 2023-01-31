# Acme Support

Acme Support is a Python Django Web application that allows users to login and create tickets, and allows admins to create and manage users and departments. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Features

- Login page with basic username and password-based login
- Users can use Email address OR Mobile Number along with their Password to Sign in to the App
- Create, Update, and Delete Departments 
- Create New Tickets
- Manage Tickets


### Prerequisites

- Python 3.x
- Django 4.x
- Django REST framework
- bcrypt (or any other library for password encryption)
- Zendesk API (if you want to integrate with Zendesk)

### Installing

1. Clone the repository

https://github.com/kharishgit/peerxptassessment.git

2. Install the requirements
  - pip install -r requirements.txt


3. Run migrations
- python manage.py makemigrations
- python manage.py migrate


4. Run the development server
- python manage.py runserver
## Usage
- Go to http://127.0.0.1:8000/admin/ to access the admin panel
- To login as a User you need to use the endpoint "http://127.0.0.1:8000/support" .Providing your credentials properly you can login
- To create a new user, you need to login as admin and use the endpoint "http://127.0.0.1:8000/support/create_user" with a POST request.
- To create a new department, you need to login as admin and use the endpoint "http://127.0.0.1:8000/support/create_department" with a POST request.
- To update a department, you need to login as admin and use the endpoint "http://127.0.0.1:8000/support/update_department/<int:department_id>"  with department id respectively.
- To update a department, you need to login as admin and use the endpoint "http://127.0.0.1:8000/support/delete_department/<int:department_id>"  with department id respectively.
- To create a new ticket, you need to login as a user and use the endpoint "http://127.0.0.1:8000/support/create_ticket" with a POST request.
- To Manage  ticket, you need to login as user and use the endpoint "http://127.0.0.1:8000/support/manage_tickets/<id>" with ticket id respectively.
- To Delete  ticket, you need to login as Admin and use the endpoint "http://127.0.0.1:8000/support/delete_ticket/<id>" with ticket id request respectively.

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Django REST framework](https://www.django-rest-framework.org/) - Used to build the RESTful API
* [bcrypt](https://pypi.org/project/bcrypt/) - Used for password encryption
* [Zendesk API](https://developer.zendesk.com/rest_api/docs/support/introduction) - Used to integrate with Zendesk

## Authors

* **Harish.K** - [GitHub Profile](https://github.com/kharishgit)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
