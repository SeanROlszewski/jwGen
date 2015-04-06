def tokenizeText(_inputText):
    _inputText = _inputText.translate(None, ',./<>?\'":;[{}]\\|+=-_)(*&^%$#@!~`') #Perhaps find a better way to include all non-alphabetical characters.
    _inputText = _inputText.split()
    return _inputText



def parsePartOfSpeechToWeight(_partOfspeech):
    weight = partsOfSpeech[_partOfspeech]
    return weight
