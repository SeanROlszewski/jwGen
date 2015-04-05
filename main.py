# See https://developers.google.com/image-search/v1/jsondevguide for google's search API

import nltk.tag as tagger
import nltk
import urllib2
import simplejson
import numpy

from skimage import io, color, feature, transform
import skimage

# The tagger used in this iteration is from the Penn Treebank Project. See https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html for the list and explanation
# partsOfSpeech = ['CC',
#                  'CD',
#                  'DT',
#                  'EX',
#                  'FW',
#                  'IN',
#                  'JJ',
#                  'JJR',
#                  'JJS',
#                  'LS',
#                  'MD',
#                  'NN',
#                  'NNS',
#                  'NNP',
#                  'NNPS',
#                  'PDT',
#                  'POS',
#                  'PRP',
#                  'PRP$',
#                  'RB',
#                  'RBR',
#                  'RBS',
#                  'RP',
#                  'SYM',
#                  'TO',
#                  'UH',
#                  'VB',
#                  'VBD',
#                  'VBG',
#                  'VBN',
#                  'VBP',
#                  'VBZ',
#                  'WDT',
#                  'WP',
#                  'WP$',
#                  'WRB']

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

class Shape:
    width = 0
    height = 0
    n = 0

    def __init__(self, width = 0, height = 0, n = 0):
        self.width = width
        self.height = height
        self.n = n

    def asTuple(self):
        return (self.width, self.height, self.n)

'''


main()


'''

def main():
    searchTerms = parseInputIntoSearchTerms('hemp')

    if len(searchTerms) == 0:

        print "Unable to generate image.\n" + generateErrorMessage("The filter used to remove words from the sentence for the query is too restrictive - no words are left after the filter!")

    else:

        for searchTerm in searchTerms:

            # Do a search on Google for each of our search terms, and get the first four images.
            handleSearchTerm(searchTerm)


def generateErrorMessage(_errorMessageText):
    return "Error: " + _errorMessageText


'''


Input handling functions



'''

def parseInputIntoSearchTerms(_inputString):

    searchTerms = []

    tokenizedText = tokenizeText(_inputString)
    taggedText = nltk.pos_tag(tokenizedText)

    # Create a Term object for every search term we'll be looking up.
    for token in taggedText:
        termPartOfSpeech = token[1]

        # Filter out terms that aren't a part of speech we want to use.
        if termPartOfSpeech in partsOfSpeech.keys():

            termText = token[0]
            termWeight = parsePartOfSpeechToWeight(termPartOfSpeech)
            term = Term(termText, termPartOfSpeech, termWeight)
            searchTerms.append(term)

    return searchTerms


def tokenizeText(_inputText):
    _inputText = _inputText.translate(None, ',./<>?\'":;[{}]\\|+=-_)(*&^%$#@!~`') #Perhaps find a better way to include all non-alphabetical characters.
    _inputText = _inputText.split()
    return _inputText



def parsePartOfSpeechToWeight(_partOfspeech):
    weight = partsOfSpeech[_partOfspeech]
    return weight


'''


Image Generation Functions


'''

def toGrayScale(_imageData):

    return color.rgb2gray(_imageData)



def handleSearchTerm(_searchTerm):
    url = getImageUrlForSearchQuery(_searchTerm)
    response = makeRequest(url)
    imageUrls = getImageURLS(response)

    _searchTerm.addUrls(imageUrls)   # I may not end up needing to do this.

    print "-----------------"
    print "Working with term '" + _searchTerm.text + "'"
    print "-----------------"

    currentImageDataSet = io.ImageCollection(imageUrls, conserve_memory=False, loadfunc=toGrayScale)
    finalImage = generateImageFromDataSet(currentImageDataSet, Shape(1000, 1000, 3))

    io.imshow(finalImage)
    io.show()

def generateImageFromDataSet(_imageDataSet, _imageShape):

    print "Requested Image's Size: " + str(_imageShape.asTuple())

    # Create a 2d array to store the data in.
    finalImage = numpy.ndarray( shape = _imageShape.asTuple(),
                                dtype = float)

    for imageData in _imageDataSet:

        workingData = []

        if imageData.shape[0] != _imageShape.width or imageData.shape[1] != _imageShape.height:

            imageDataDimensions = _imageShape.asTuple()
            print "Resizing retrieved image from " + str(imageData.shape) + " to size " + str(imageDataDimensions)
            workingData = transform.resize(imageData, imageDataDimensions, order=1, mode='constant', cval=0, clip=True, preserve_range=False)

        print "Working data size: " + str(workingData.shape)

        # workingData =

        print "Summing image data"
        for j in range(_imageShape.height):
            for i in range(_imageShape.width):
                finalImage[i][j] += workingData[i][j]

    print "Averaging image data"
    for j in range(_imageShape.height):
        for i in range(_imageShape.width):
            finalImage[i][j] /= len(_imageDataSet)

    print "Generated Image's size: " + str(finalImage.shape)


    finalImage = color.gray2rgb(finalImage)

    return finalImage


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


if __name__ == '__main__':
    main()

