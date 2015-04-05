# See https://developers.google.com/image-search/v1/jsondevguide for google's search API

import nltk.tag as tagger
import nltk
import urllib2
import simplejson
import numpy
import pdb

from skimage import io, color, feature, transform
import skimage

# partsOfSpeech = {'CC': 0.3, 'CD': 0.1, 'VB': 0.4, 'NN': 0.2}
partsOfSpeech = {'CC': 0,
                 'CD': 0,
                 'DT': 0,
                 'EX': 0,
                 'FW': 0,
                 'IN': 0,
                 'JJ': 0,
                 'JJR': 0,
                 'JJS': 0,
                 'LS': 0,
                 'MD': 0,
                 'NN': 0,
                 'NNS': 0,
                 'NNP': 0,
                 'NNPS': 0,
                 'PDT': 0,
                 'POS': 0,
                 'PRP': 0,
                 'PRP$': 0,
                 'RB': 0,
                 'RBR': 0,
                 'RBS': 0,
                 'RP': 0,
                 'SYM': 0,
                 'TO': 0,
                 'UH': 0,
                 'VB': 0,
                 'VBD': 0,
                 'VBG': 0,
                 'VBN': 0,
                 'VBP': 0,
                 'VBZ': 0,
                 'WDT': 0,
                 'WP': 0,
                 'WP$': 0,
                 'WRB': 0}

class Term:
    text = ""
    partOfSpeech = ""
    weight = 0.0
    urls = []
    imageData = None

    def __init__(self, text = "", partOfSpeech = "", weight = 0.0, imageData = None):
        self.text = text
        self.partOfSpeech = partOfSpeech
        self.weight = weight
        self.urls = []
        self.imageData = imageData

    def addUrl(self, url):
        self.urls.append(url)

    def addUrls(self, urls):
        self.urls = urls

    def addImageData(self, _imageData):
        if (_imageData != None):
            print "Adding image data to Term object"
            self.imageData = _imageData

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

    searchTerms = parseInputIntoSearchTerms('google sublime')

    if len(searchTerms) == 0:
        print "Unable to generate image.\n" + generateErrorMessage("The filter used to remove words from the sentence for the query is too restrictive - no words are left after the filter!")

    else:
        print "Looking up images for search terms: " + str(map(lambda x: x.text, searchTerms))

        imageShape = Shape(1000, 1000, 3)

        finalImage = generateFloatImageArray(imageShape.asTuple())

        # Do a search on Google for each of our search terms, and get the first four images.
        for searchTerm in searchTerms:

            try:

                handleSearchTerm(searchTerm)

                pdb.set_trace()

                print "Summing image data"
                for j in range(imageShape.height):
                    for i in range(imageShape.width):
                        finalImage[i][j] += searchTerm.imageData[i][j]

            except TypeError, typeError:

                print "**** Type Error ****\n" + str(typeError)

            except IOError, ioError:

                print "**** Encountered IOError ****\n" + str(ioError)

            except urllib2.HTTPError, httpError:

                print "**** Encountered HTTPError ****\n" + str(httpError)

            except RuntimeError, runtimeError:

                print "**** Runtime Error ****\n" + str(runtimeError)

        print "Averaging image data"
        for j in range(imageShape.height):
            for i in range(imageShape.width):
                finalImage[i][j] /= len(searchTerms)


        io.imshow(finalImage)
        io.show()




def generateErrorMessage(_errorMessageText):
    return "Error: " + str(_errorMessageText)


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

    currentImageDataSet = io.ImageCollection(imageUrls, conserve_memory=True, loadfunc=toGrayScale)
    finalImage = generateImageFromDataSet(currentImageDataSet, Shape(1000, 1000, 3))
    _searchTerm.addImageData(finalImage)

    # io.imshow(finalImage)
    # io.show()

    print "\n"

def generateFloatImageArray(_arrayDimensions):
    imageArray = numpy.ndarray( shape = _arrayDimensions,
                                dtype = float)
    imageArray.fill(0.0)
    return imageArray

def generateImageFromDataSet(_imageDataSet, _imageShape):

    print "Specified Size: " + str(_imageShape.asTuple())

    # Create a 2d array to store the data in.
    finalImage = generateFloatImageArray(_imageShape.asTuple())

    for imageData in _imageDataSet:

        workingData = []

        imageDataDimensions = _imageShape.asTuple()
        print "Resizing retrieved image from " + str(imageData.shape) + " to size " + str(imageDataDimensions)
        workingData = transform.resize(imageData, imageDataDimensions, order=1, mode='constant', cval=0, clip=True, preserve_range=False)
        # workingData =

        print "Summing image data"
        for j in range(_imageShape.height):
            for i in range(_imageShape.width):
                finalImage[i][j] += (workingData[i][j] * 0.5)

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

