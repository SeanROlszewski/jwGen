import nltk.tag as tagger
import nltk
import urllib2
import simplejson

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

    def __init__(self, text = "", partOfSpeech = "", weight = 0.0):
        self.text = text
        self.partOfSpeech = partOfSpeech
        self.weight = weight

def tokenizeText(inputText):
    inputText = inputText.translate(None, ',./<>?\'":;[{}]\\|+=-_)(*&^%$#@!~`') #Perhaps find a better way to include all non-alphabetical characters.
    inputText = inputText.split()
    return inputText

def parsePartOfSpeechToWeight(partOfSpeech):
    weight = partsOfSpeech[partOfSpeech]
    return weight

def getPublicIp():
    return '71.232.42.68'


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

    for searchTerm in searchTerms:
        userIp = getPublicIp()

        url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
       'v=1.0&q=' + searchTerm.text + '=&userip=' + userIp)

        request = urllib2.Request(url, None, {'Referer': 'http://www.whiteroom.audio'})
        response = urllib2.urlopen(request)

        print "Image Results:"

        results = simplejson.load(response)
        responseData = results['responseData']
        imageResults = responseData['results']
        # print imageResults

        for i in range(len(imageResults)):
            currentImageResult = imageResults[i]
            print currentImageResult['url']

        print '\n'



main()

