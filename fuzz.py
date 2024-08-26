from fuzzywuzzy import fuzz
from fuzzywuzzy import process

z = fuzz.ratio("Catherine M Gitau","Catherine Gitau")
print(type(z))
