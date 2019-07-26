# Class defined to couple words and search criterion
import re
class resultSearched():
    def __init__(self, words, symbol, function='default'):
        self.words = words
        self.symbol = symbol
        if type(function) == str:
            self.function = self.default
        else:
            self.function = function

    def default(self,array):
        '''''
        Function default to search word coincidences
            input:
                array: list type with paragraph words
            output:
                boolean: True if the searched word is in paragraph
                         False if isn't
        '''''
        paragraph = ' '.join(array)
        for word in self.words:
            aux = re.findall(word + r'.*', paragraph, re.IGNORECASE)
            if len(aux) > 0:
                return True
        return False

