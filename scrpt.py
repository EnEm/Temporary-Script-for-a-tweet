import csv

ETHNICITY = 520 # V201549x
ETHNICITY_DIR = {
    '-9': 'Refused',
    '-8': 'Don’t know',
    '1': 'White',
    '2': 'Black',
    '3': 'Hispanic',
    '4': 'Asian or Hawaiian',
    '5': 'Native American/Alaska Native',
    '6': 'Multiple races'
}

RATINGS = [1306, 1307, 1308, 1310] # V202478 V202479 V202480 V202482
RATING_NAMES = ['ASIANS', 'HISPANICS', 'BLACKS', 'WHITES']
RATING_DIR = {
    '-9': 'Refused',
    '-7': 'No post-election data, deleted due to incomplete interview',
    '-6': 'No post-election interview',
    '-5': 'Interview breakoff (sufficient partial IW)',
    '-4': 'Technical error',
    '-1': 'Inapplicable'
}

v = None
with open('anes_timeseries_2020_csv_20220210.csv') as csvfile:
    v = list(csv.reader(csvfile, delimiter=','))
    dct = {}
    for i in range(1, len(v)):
        if v[i][ETHNICITY] not in dct:
            dct[v[i][ETHNICITY]] = {}
            for r in RATINGS:
                dct[v[i][ETHNICITY]][r] = {}
        for r in RATINGS:
            if v[i][r] not in dct[v[i][ETHNICITY]][r]:
                dct[v[i][ETHNICITY]][r][v[i][r]] = 0
            dct[v[i][ETHNICITY]][r][v[i][r]] += 1

    for e in ETHNICITY_DIR:
        tot = 0
        for x in dct[e]:
            for y in dct[e][x]:
                tot += dct[e][x][y]
        print(ETHNICITY_DIR[e] + ': ' + str(tot//4))
        for r in RATINGS:
            print('\t' + RATING_NAMES[RATINGS.index(r)] + ': ')
            avg = 0
            tot2 = 0
            for x in dct[e][r]:
                if x not in RATING_DIR:
                    avg += int(x)*dct[e][r][x]
                    tot2 += dct[e][r][x]
            avg /= tot2
            sd = 0
            for x in dct[e][r]:
                if x not in RATING_DIR:
                    sd += ((avg-int(x))**2)*dct[e][r][x]
            sd /= tot2
            sd = sd**0.5
            print('\t\tAverage : ' + str(avg))
            print('\t\tStandard Deviation : ' + str(sd))
        print()
