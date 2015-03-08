# See https://developers.google.com/image-search/v1/jsondevguide for google's search API

import nltk.tag as tagger
import nltk
import urllib2
import simplejson
from skimage import io as imageHandler

# The tagger used in this iteration is from the Penn Treebank Project. See https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html for the list and explanation
partsOfSpeech = ['CC',
                 'CD',
                 'DT',
                 'EX',
                 'FW',
                 'IN',
                 'JJ',
                 'JJR',
                 'JJS',
                 'LS',
                 'MD',
                 'NN',
                 'NNS',
                 'NNP',
                 'NNPS',
                 'PDT',
                 'POS',
                 'PRP',
                 'PRP$',
                 'RB',
                 'RBR',
                 'RBS',
                 'RP',
                 'SYM',
                 'TO',
                 'UH',
                 'VB',
                 'VBD',
                 'VBG',
                 'VBN',
                 'VBP',
                 'VBZ',
                 'WDT',
                 'WP',
                 'WP$',
                 'WRB']

partsOfSpeech = {'CC': 0.3, 'CD': 0.1, 'VB': 0.4, 'NN': 0.2}


class Term:
    text = ""
    partOfSpeech = ""
    weight = 0.0
    urls = []

    def __init__(self, text = "", partOfSpeech = "", weight = 0.0):
        self.text = text
        self.partOfSpeech = partOfSpeech
        self.weight = weight
        self.urls = []

    def addUrl(self, url):
        self.urls.append(url)

    def addUrls(self, urls):
        self.urls = urls


def tokenizeText(inputText):
    inputText = inputText.translate(None, ',./<>?\'":;[{}]\\|+=-_)(*&^%$#@!~`') #Perhaps find a better way to include all non-alphabetical characters.
    inputText = inputText.split()
    return inputText


def parsePartOfSpeechToWeight(partOfSpeech):
    weight = partsOfSpeech[partOfSpeech]
    return weight


def getPublicIp():
    results = makeRequest('http://httpbin.org/ip')
    return results['origin']


def getImageUrlForSearchQuery(searchTerm):
    userIp = getPublicIp()
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q=' + searchTerm.text + '=&userip=' + userIp + '=&as_filetype=jpg')
    return url


def getImageURLS(jsonResponse):

    imageUrls = []
    responseData = jsonResponse['responseData']
    imageResults = responseData['results']

    for i in range(len(imageResults)):
        currentImageResult = imageResults[i]
        imageUrls.append(currentImageResult['url'])

    return imageUrls

# Returns a JSON payload of the request as a string.
def makeRequest(url, referer = 'http://www.whiteroom.audio'):
    request = urllib2.Request(url, None, {'Referer': referer})
    remoteResponse = urllib2.urlopen(request)
    return simplejson.load(remoteResponse)


def main():

    tokenizedText = tokenizeText('This :is a test sent?ence < with # the color brown.')
    taggedText = nltk.pos_tag(tokenizedText)

    searchTerms = []

    # Create a Term object for every search term we'll be looking up.
    for token in taggedText:
        termPartOfSpeech = token[1]

        # Filter out terms that aren't a part of speech we want to use.
        if termPartOfSpeech in partsOfSpeech.keys():

            termText = token[0]
            termWeight = parsePartOfSpeechToWeight(termPartOfSpeech)
            term = Term(termText, termPartOfSpeech, termWeight)
            searchTerms.append(term)

    searchTermImageUrlSets = []

    # Do a search on Google for each of our search terms, and get the first four images.
    for searchTerm in searchTerms:

        url = getImageUrlForSearchQuery(searchTerm)
        response = makeRequest(url)
        imageUrls = getImageURLS(response)

        searchTerm.addUrls(imageUrls)   # I may not end up needing to do this.

        currentImageDataSet = []
        for imageUrl in imageUrls:

            try:
                imageData = imageHandler.imread(imageUrl)
                print "Successfully loaded image at URL " + imageUrl
                currentImageDataSet.append(imageData)

            except IOError:
                print "Unable to load image at URL " + imageUrl

main()

