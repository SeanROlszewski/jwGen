# See https://developers.google.com/image-search/v1/jsondevguide for google's search API

import numpy
from classes import Term
from internetUtils import *
from stringUtils import *

from skimage import io, color, feature, transform
import skimage

BRIGHTNESS_SETTING = 1.0
class jwGen:

    def __init__(self, _string):
        self.__generateImageForString(_string)
        # init


    def __generateImageForString(self, _string):

        searchTerms = filterInputStringIntoSearchTerms(_string) # the string here would be provided from a UI element.

        if len(searchTerms) == 0:

            self.handleNoSearchTerms()

        else:

            self.handleSearchTerms(searchTerms)


    '''

    Event Handling


    '''

    def handleNoSearchTerms(self):
        print "Unable to generate image.\n" + "Error: The filter used to remove words from the sentence for the query is too restrictive - no words are left after the filter!"

    def handleSearchTerms(self, _searchTerms):

        imageShape = (1000, 1000, 3)
        finalImage = self.generateFloatArray(imageShape)

        # Do a search on Google for each of our search terms, and get the first four images.

        for searchTerm in _searchTerms:

            try:

                self.handleSearchTerm(searchTerm)

                print "Adding image data to final image"
                for j in range(imageShape[0]):
                    for i in range(imageShape[1]):
                        finalImage[i][j] += searchTerm.imageData[i][j] # / len(_searchTerms)

            except TypeError, typeError:

                print "\n\t**** Type Error ****\n\t" + str(typeError) + "\n"

            except IOError, ioError:

                print "\n\t**** Encountered IOError ****\n\t" + str(ioError) + "\n"

            except RuntimeError, runtimeError:

                print "\n\t**** Runtime Error ****\n\t" + str(runtimeError) + "\n"

        print "Averaging image data"
        for j in range(imageShape[0]):
            for i in range(imageShape[1]):
                finalImage[i][j] /= len(_searchTerms)


        io.imshow(finalImage)
        io.show()

    def handleSearchTerm(self, _searchTerm):

        url = getImageUrlForSearchQuery(_searchTerm)
        response = makeRequest(url)
        imageUrls = getImageURLS(response)

        _searchTerm.addUrls(imageUrls)   # I may not end up needing to do this.

        print "-----------------"
        print "Working with term '" + _searchTerm.text + "'"
        print "-----------------"

        currentImageDataSet = io.ImageCollection(imageUrls, conserve_memory=True, loadfunc=self.convertToGrayScale)
        finalImage = self.generateImageFromImageSetWithShape(currentImageDataSet, (1000, 1000, 3))
        _searchTerm.addImageData(finalImage)

        # io.imshow(finalImage)
        # io.show()

        print "\n"


    '''


    Image Generation Functions


    '''

    def convertToGrayScale(self, _imageData):
        return color.rgb2gray(_imageData)

    def convertToRGB(self, _image):
        return color.gray2rgb(_image)

    def resizeImage(self, _data, _destinationShape):
        return transform.resize(_data, _destinationShape, order=1, mode='constant', cval=0, clip=True, preserve_range=False)


    '''
    I'm going to be using this function a lot. It takes an array of image data and combines them all.
    '''

    def generateImageFromImageSetWithShape(self, _sourceImageSet, _imageSize):

        print "Specified Size: " + str(_imageSize)

        # Create a 2d array to store the data in.
        finalImage = self.generateFloatArray(_imageSize)

        for sourceImageData in _sourceImageSet:

            print "Resizing Source Image"
            workingData = self.resizeImage(sourceImageData, _imageSize)

            print "Adding image's data to return buffer and applying brightness setting"
            for j in range(_imageSize[0]):
                for i in range(_imageSize[1]):
                    finalImage[i][j] += workingData[i][j]

        print "Averaging generated image's data"
        for j in range(_imageSize[0]):
            for i in range(_imageSize[1]):
                finalImage[i][j] /= len(_sourceImageSet)

        print "Converting image from grayscale to rgb"
        finalImage = self.convertToRGB(finalImage)

        print "Generated Image's size: " + str(finalImage.shape)
        return finalImage



    def generateFloatArray(self, _arrayDimensions):
        floatArray = numpy.ndarray( shape=_arrayDimensions,
                                    dtype=float )
        floatArray.fill(0.0)
        return floatArray
