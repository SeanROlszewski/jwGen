import nltk.tag as tagger
import nltk
import sys

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

partsOfSpeechFullText = {'CC': 'Coordinating conjunctions',
                         'CD': 'Cardinal numbers',
                         'DT': 'Determiner',
                         'EX': 'Existential there',
                         'FW': 'Foreign word',
                         'IN': 'Preposition or subordinating conjunction',
                         'JJ': 'Adjective',
                         'JJR': 'Adjective, comparative',
                         'JJS': 'Adjective, superlative',
                         'LS': 'List item marker',
                         'MD': 'Modal',
                         'NN': 'Noun, singular or mass',
                         'NNS': 'Noun, plural',
                         'NNP': 'Proper noun, singular',
                         'NNPS': 'Proper noun, plural',
                         'PDT': 'Predeterminer',
                         'POS': 'Possessive ending',
                         'PRP': 'Personal pronoun',
                         'PRP$': 'Possessive pronoun',
                         'RB': 'Adverb',
                         'RBR': 'Adverb, comparative',
                         'RBS': 'Adverb, superlative',
                         'RP': 'Particle',
                         'SYM': 'Symbol',
                         'TO': 'to',
                         'UH': 'Interjection',
                         'VB': 'Verb, base form',
                         'VBD': 'Verb, past tense',
                         'VBG': 'Verb, gerund or present participle',
                         'VBN': 'Verb, past participle',
                         'VBP': 'Verb, non-3rd person singular present',
                         'VBZ': 'Verb, 3rd person singular present',
                         'WDT': 'Wh-determiner',
                         'WP': 'Wh-pronoun',
                         'WP$': 'Possessive wh-pronoun',
                         'WRB': 'Wh-adverb'}

def tokenizeText(inputText):
    inputText = inputText.translate(None, ',./<>?\'":;[{}]\\|+=-_)(*&^%$#@!~`') #Perhaps find a better way to include all non-alphabetical characters.
    inputText = inputText.split()
    return inputText


def main():

    if len(sys.argv) != 2:
        print "You used it wrong. Use python posCounter.py \"The sentence to generate an image for.\""
        return 1

    stringToProcess = sys.argv[1]
    tokenizedText = tokenizeText(stringToProcess)
    taggedText = nltk.pos_tag(tokenizedText)

    for tag in taggedText:
        partOfSpeech  = tag[1]
        partsOfSpeech[partOfSpeech] += 1

    for partOfSpeech in partsOfSpeech:
        partOfSpeechCount = partsOfSpeech[partOfSpeech]

        if partOfSpeechCount > 0:
            print "You used a " + partsOfSpeechFullText[partOfSpeech] + " (" + partOfSpeech + ") " + str(partOfSpeechCount) + " times."

main()
