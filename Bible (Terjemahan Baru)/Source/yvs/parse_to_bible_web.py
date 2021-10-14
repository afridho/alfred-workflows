import sys

query = sys.argv[1].replace('+', '.').replace(':', ".")

url = 'https://www.bible.com/bible/306/'+query+'.TB'

print(url)



