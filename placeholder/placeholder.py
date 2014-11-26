import sys
import os
from django.conf import settings

DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', '$ovmryj*wtfjozsz64vs8-xh665(g=#02s506w!7zfkw(bj)jp')
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

from django import forms
from django.conf.urls import url
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.wsgi import get_wsgi_application
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.cache import cache

class ImageForm(forms.Form):
    """Form to validate requested placeholder image."""
    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)

    def generate(self, image_format='PNG'):
        """Generate an image of type image_format and return as raw bytes"""
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        key = '{0}.{1}.{2}'.format(width, height, image_format) # cache key for current image
        content = cache.get(key) # search for current image
        if content is None: # if not cached you have to build it
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            text = "{0} X {1}".format(width, height)
            textwidth, textheight = draw.textsize(text) # how much space will this take?
            if textwidth < width and textheight < height:
                texttop = (height - textheight) / 2
                textleft = (width - textwidth) / 2
                draw.text((textleft, texttop), text, fill=(200, 100, 0))
            content = BytesIO()
            image.save(content, image_format) # convert image to bytes
            content.seek(0) # start the stream on the beginning of the image
        return content

def placeholder(request, width, height):
    form = ImageForm({'height': height, 'width': width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponseBadRequest('Image size too big')

def index(request):
    return HttpResponse('Hello World')

urlpatterns = (
        url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$',
            placeholder, name='placeholder'),
        url(r'^$', index),
)

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
