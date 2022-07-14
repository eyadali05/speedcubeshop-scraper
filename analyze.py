# TODO: perform feature to replace uncleaned price with clean price
import pandas as pd
from scrape import get_filename

# Get filename of csv
file_name = get_filename()
# Initialize dataframe
scs = pd.read_csv(file_name)
# Column to loop over
prices = scs["Cube Price"]

# column-item before cleaning: LE 14.99
# after cleaning: 14.99

for p in prices:
    print(f"Cleaning {p}")
    cleaned = ""
    for idx, character in enumerate(p):
        try:
            int(character)
            cleaned += str(character)
        except ValueError:
            continue
    cleaned = int(cleaned) / 100
    # اللي تحت ده مش شغال, does not replace
    # Not Working: scs["Cube Price"].replace(p, cleaned)
    print(f"Cleaned: {cleaned}")

# Items stay as it is without replacing
print(scs[["Cube Price"]])
