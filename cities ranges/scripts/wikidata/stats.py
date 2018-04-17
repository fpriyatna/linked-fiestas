import csv

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def clean_string(value):
    return value.replace(" ","").replace("-","").lower().strip()

def compare(value1, value2):
    return levenshtein(clean_string(value1), clean_string(value2))

ranged_cities = {}
with open('cities_ranges.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        ranged_cities[row[0]] = row[1].strip()

with open('wikidata-cities.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        added = 0
        for key in ranged_cities.keys():
            if compare(row[0],key) < 2:
                print row[0]+" "+key+" "+ranged_cities[key]
                added +=1
        if added == 0:
            for key in ranged_cities.keys():
                if compare(row[0],key) < 4:
                    print row[0]+" "+key+" "+ranged_cities[key]
                    added +=1
        if added == 0:
            print "....->"+str(row)

