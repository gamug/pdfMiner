from pdfMiner.toolBox.booleanClass import resultSearched
from geotext import GeoText

# This functions are defined to introduce parameters into main function
# for english parameters
def searchNumb(array):
    '''''
    This function check every char in paragraph searching for numbers
        Input:
            array: it's an array containing all paragraph words splited by " "
        Output:
            return: True if there are numbers, False if not.
    '''''
    for word in array:
        for char in word:
            try:
                int(char)
                return True
            except:
                pass
    return False


def searchGeo(array):
    paragraph = ' '.join(array)
    if len(GeoText(paragraph).cities) > 0 or len(GeoText(paragraph).countries) > 0:
        return True
    else:
        return False


def searchCurrency(array):
    '''''
    Function defined to check paragraph agains currency presence.
        Input:
            array: it's an array containing all paragraph words splited by " "
        Output:
            return: True if there are currencies, False if not.
    '''''
    for value in array:
        for char in value:
            if char == '$' or char == '€' or char == '£':
                return True
    return False


project = resultSearched(
    ['project'], 'project'
)
invest = resultSearched(
    ['cost','capex', 'investmen'],
    'investmen (cost, capex)'
)
economic = resultSearched(
    ['npv', 'lifting', 'development', 'irr'],
    'economic indicators (npv, irr, lifting, development, irr)'
)
number = resultSearched(
    ['number'], 'number values', function=searchNumb
)
geograph = resultSearched(
    ['geography'], 'places (countries, cities)', function=searchGeo
)
currency = resultSearched(
    ['currency'], 'currency symbols ($, €, £)', function=searchCurrency
)
numGeneral = resultSearched(
    ['Million', 'billion', 'miles'],
    'number generalization (miles, million, billion)'
)
# filter structure:
                     #  [project or invest or economic or geograph or numGeneral] and [currency] and [number]
structureEnglish = [[project, invest, economic, geograph, numGeneral], [currency], [number]]



# This functions are defined to introduce parameters into main function
# for spanish parameters
project = resultSearched(
    ['proyecto'], 'project'
)
invest = resultSearched(
    ['costo', 'capex', 'inversión', 'inversion'],
    'investmen (cost, capex)'
)
economic = resultSearched(
    ['npv', 'lifting', 'development', 'irr','levantamiento', 'desarrollo'],
    'economic indicators (npv, irr, lifting, development, irr)'
)
number = resultSearched(
    ['number'], 'number values', function=searchNumb
)
geograph = resultSearched(
    ['geography'], 'places (countries, cities)', function=searchGeo
)
currency = resultSearched(
    ['currency'], 'currency symbols ($, €, £)', function=searchCurrency
)
numGeneral = resultSearched(
    ['millón', 'millon', 'billón', 'billon', 'miles'],
    'number generalization (miles, million, billion)'
)
# filter structure:
                     #  [project or invest or economic or geograph or numGeneral] and [currency] and [number]
structureSpanish = [[project, invest, economic, geograph, numGeneral], [currency], [number]]