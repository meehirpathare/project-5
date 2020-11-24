from datetime import datetime
import json
import requests
import urllib.request

def get_img(object_id, path, return_meta=False):
    filename = path + object_id + ".jpg"
    api_url = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/{}'.format(object_id)
    response = requests.get(api_url, allow_redirects=True)
    url = json.loads(response.text)['primaryImage']
    is_public = json.loads(response.text)['isPublicDomain']
    im = urllib.request.urlretrieve(url, filename)
    
    if return_meta == True:
        j = {
            'object_id': object_id,
             'api_url': api_url,
             'img_url': url,
             'is_public': is_public
            }
        return j