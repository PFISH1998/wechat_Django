from django.test import TestCase
from search.views import login
from django.http import HttpRequest
# Create your tests here.


# class LoginTest(TestCase):
#     request = HttpRequest()
#     request.method = 'POST'
#     request['sid'] = '12345'
#     request['pwd'] = 'qwer'
#     response = login(request)
#     print(response)