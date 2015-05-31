import urllib2
import simplejson

'''


Internet/URL/IP Functions


'''

def getImageUrlForSearchQuery(_searchTerm):

    userIp = getPublicIp()
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q=' + _searchTerm.text + '&userip=' + userIp + '&as_filetype=jpg&imgsz=xxlarge')

    return url

def getPublicIp():

    results = makeRequest('http://httpbin.org/ip')

    return results['origin']

# Returns a JSON payload of the request as a string.
def makeRequest(_url, _referer = 'http://www.whiteroom.audio'):
    # TODO: SIDE EFFECT!!!!
    request = urllib2.Request(_url, None, {'Referer': _referer})
    remoteResponse = urllib2.urlopen(request)

    return simplejson.load(remoteResponse)

def getImageURLS(_jsonReponse):

    imageUrls = []
    responseData = _jsonReponse['responseData']
    imageResults = responseData['results']

    for i in range(len(imageResults)):
        currentImageResult = imageResults[i]
        imageUrls.append(currentImageResult['url'])

    return imageUrls
