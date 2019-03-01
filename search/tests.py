from django.test import TestCase
from search.views import login
from django.http import HttpRequest
# Create your tests here.


def cidp(sid):
    if len(sid) == 8 and sid.startwith("180"):
        return True
    elif sid[2] == '5':
        return True
    else:
        return False