class Term:
    text = ""
    partOfSpeech = ""
    weight = 0.0
    urls = []
    imageData = None

    def __init__(self, _text="", _partOfSpeech="", _weight=0.0, _imageData=None):

        self.text = _text
        self.partOfSpeech = _partOfSpeech
        self.weight = _weight
        self.urls = []
        self.imageData = _imageData

    def addUrl(self, _url):
        self.urls.append(_url)

    def addUrls(self, urls):
        self.urls = urls

    def addImageData(self, _imageData):

        if (_imageData != None):

            print "Adding image data to Term object"
            self.imageData = _imageData
