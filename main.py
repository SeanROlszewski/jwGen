# See https://developers.google.com/image-search/v1/jsondevguide for google's search API

import nltk.tag as tagger
import nltk
import urllib2
import simplejson
import numpy

from skimage import io, color, feature, transform

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

    def getAsTuple(self):
        return (self.width, self.height)

'''


main()


'''

def main():
    searchTerms = parseInputIntoSearchTerms('red dog got jumped last night d00d')

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


def handleSearchTerm(_searchTerm):
    url = getImageUrlForSearchQuery(_searchTerm)
    response = makeRequest(url)
    imageUrls = getImageURLS(response)

    _searchTerm.addUrls(imageUrls)   # I may not end up needing to do this.

    print "-----------------"
    print "Working with term '" + _searchTerm.text + "'"
    print "-----------------"

    currentImageDataSet = []
    for imageUrl in imageUrls:

        try:

            grayImageData = io.imread(imageUrl, as_grey=True)
            currentImageDataSet.append(grayImageData)
            print "Successfully loaded image at URL " + imageUrl


        except IOError:
            print "Unable to load image at URL " + imageUrl

    finalImage = generateImageForDataSet(currentImageDataSet)
    io.imshow(finalImage)
    io.show()

def generateImageForDataSet(_imageDataSet):

    # Get the smallest image width and height so we don't have to scale the image.
    # finalImageShape = generateImageShapeFromDataSet(_imageDataSet)
    finalImage = generateImageFromDataSet(_imageDataSet, Shape(1000, 1000, 2))

    return finalImage

def generateImageShapeFromDataSet(_imageDataSet):

    imageShape = Shape()
    for imageData in _imageDataSet:


        currentImageWidth = imageData.shape[0]
        currentImageHeight = imageData.shape[1]
        currentImageDimensionCount = imageData.ndim

        print "Image shape: " + str(imageData.shape)
        print "Number of dimensions: " + str(currentImageDimensionCount)

        # Only change our image shape if the current image shape or dimensions are smaller than any of the other image shapes or dimensions we've gone through.
        if imageShape.n == 0:
            imageShape.n = imageData.ndim
        elif currentImageDimensionCount < imageShape.n:
            imageShape.n = imageData.ndim

        if imageShape.width == 0:
            imageShape.width = currentImageWidth
        elif currentImageWidth < imageShape.width:
            imageShape.width = currentImageWidth

        if imageShape.height == 0:
            imageShape.height = currentImageHeight
        elif currentImageHeight < imageShape.height:
            imageShape.height = currentImageHeight

    print "Generated Image's Width: " + str(imageShape.width)
    print "Generated Image's Height: " + str(imageShape.height)

    return imageShape

def generateImageFromDataSet(_imageDataSet, _imageShape):

    print "Requested Image's Width: " + str(_imageShape.width)
    print "Requested Image's Height: " + str(_imageShape.height)

    # Create a 2d array to store the data in.
    finalImage = numpy.ndarray( shape = _imageShape.getAsTuple(),
                                dtype = float)

    for imageData in _imageDataSet:

        workingData = []

        if imageData.shape[0] != _imageShape.width or imageData.shape[1] != _imageShape.height:

            imageDataDimensions = _imageShape.getAsTuple()
            print "Resizing retrieved image to size " + str(imageDataDimensions)
            workingData = transform.resize(imageData, (1000, 1000), order=1, mode='constant', cval=0, clip=True, preserve_range=False)
            # workingData =


        print "Working data size: " + str(workingData.shape)

        print "Summing image data"
        for j in range(_imageShape.height):
            for i in range(_imageShape.width):
                finalImage[i][j] += workingData[i][j]

    print "Averaging image data"
    for j in range(_imageShape.height):
        for i in range(_imageShape.width):
            finalImage[i][j] /= len(_imageDataSet)

    print "Generated Image's Width: " + str(finalImage.shape[0])
    print "Generated Image's Height: " + str(finalImage.shape[1])

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

