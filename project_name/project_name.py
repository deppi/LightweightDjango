import sys
import os
from django.conf import settings

# template for projects. run django-admin.py startproject foo --template=project_name to make a new project with this as ur start code

DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', '{{ secret_key }}')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localost').split(',') # split by comma to allow multiple hosts

settings.configure(
        DEBUG=DEBUG,
        SECRET_KEY=SECRET_KEY,
        ALLOWED_HOSTS=ALLOWED_HOSTS,
        ROOT_URLCONF=__name__,
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ), 
)

from django.conf.urls import url
from django.http import HttpResponse
from django.core.wsgi import get_wsgi_application

def index(request):
    return HttpResponse('Hello World')

urlpatterns = (
        url(r'^$', index),
)

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
