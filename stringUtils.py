import nltk
from classes import Term

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

'''


Input handling functions


'''

def filterInputStringIntoSearchTerms(_inputString):

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

def logSearchTermsInQuery(_searchTerms):

    searchTermList = map(lambda searchTerm: searchTerm.text, _searchTerms)
    print "Looking up images for search terms: " + str(searchTermList)
