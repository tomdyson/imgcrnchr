from django.http import HttpResponse
from django.conf import settings
from PIL import Image
import urllib, StringIO, os

def crunch(request, crunch_factor, image_url):
    if not crunch_factor:
        crunch_factor = settings.IMG_CRNCH_QUALITY
    crunch_factor = int(crunch_factor)
    # ignore non-jpgs
    if image_url.endswith('.jpg'):
        image_name = image_url.split("/")[-1]
        image_cache_path = os.path.join(settings.IMG_CACHE_PATH, str(crunch_factor), image_name)
        # load from local fs if available
        if os.path.exists(image_cache_path):
            image_data = open(image_cache_path, "rb").read()
            return HttpResponse(image_data, mimetype="image/jpeg")
        # load the remote image into a file-like object
        imgf = urllib.urlopen(image_url)
        imgwr = StringIO.StringIO(imgf.read())
        try:
            im = Image.open(imgwr)
        except IOError:
            return HttpResponse("Sorry, we couldn't find an image at %s" % image_url)
        # cache compressed version
        try:
            im.save(image_cache_path, quality=crunch_factor)
        except IOError: # cache dir may not exist
            os.mkdir(os.path.join(settings.IMG_CACHE_PATH, str(crunch_factor)))
            im.save(image_cache_path, quality=crunch_factor)
        # serve up compressed version
        response = HttpResponse(mimetype="image/jpeg")
        im.save(response, quality=crunch_factor, format="jpeg")
        return response
    else:
        return HttpResponse("Sorry, this service only crunches JPGs.")