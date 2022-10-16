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

EDUCATION = 471 # V201510
EDUCATION_DIR = {
    '-9': 'Refused',
    '-8': 'Don’t know',
    '1': 'Less than high school credential',
    '2': 'High school graduate - High school diploma or equivalent (e.g. GED)',
    '3': 'Some college but no degree',
    '4': 'Associate degree in college - occupational/vocational',
    '5': 'Associate degree in college - academic',
    '6': 'Bachelor’s degree (e.g. BA, AB, BS)',
    '7': 'Master’s degree (e.g. MA, MS, MEng, MEd, MSW, MBA)',
    '8': 'Professional school degree (e.g. MD, DDS, DVM, LLB, JD)/Doctoral degree (e.g. PHD, EDD)',
    '9': 'Other/refused',
    '10': 'High school graduate or less',
    '11': 'More than High school BUT less than bachelor\'s degree',
    '12': 'Bachelor\'s, Master\'s, Doctoral\Professional',
    '95': 'Other \{SPECIFY\}'
}
EDUCATION_TRNSFRM = {
    '-9': '9',
    '-8': '9',
    '1': '10',
    '2': '10',
    '3': '11',
    '4': '11',
    '5': '11',
    '6': '12',
    '7': '12',
    '8': '12',
    '95': '9'
}

def f(education_number):
    # return education_number
    return EDUCATION_TRNSFRM[education_number]


v = None
with open('anes_timeseries_2020_csv_20220210.csv') as csvfile:
    v = list(csv.reader(csvfile, delimiter=','))
    dct = {}
    print(v[0][471])
    for i in range(1, len(v)):
        if v[i][ETHNICITY] not in dct:
            dct[v[i][ETHNICITY]] = {}
        if f(v[i][EDUCATION]) not in dct[v[i][ETHNICITY]]:
            dct[v[i][ETHNICITY]][f(v[i][EDUCATION])] = {}
            for r in RATINGS:
                dct[v[i][ETHNICITY]][f(v[i][EDUCATION])][r] = {}
        for r in RATINGS:
            if v[i][r] not in dct[v[i][ETHNICITY]][f(v[i][EDUCATION])][r]:
                dct[v[i][ETHNICITY]][f(v[i][EDUCATION])][r][v[i][r]] = 0
            dct[v[i][ETHNICITY]][f(v[i][EDUCATION])][r][v[i][r]] += 1

    for e in ETHNICITY_DIR:
        tot = 0
        for x in dct[e]:
            for y in dct[e][x]:
                for z in dct[e][x][y]:
                    tot += dct[e][x][y][z]
        print(ETHNICITY_DIR[e] + ': ' + str(tot/4))
        for ee in EDUCATION_DIR:
            if ee not in dct[e]:
                continue
            tot1 = 0
            for x in dct[e][ee]:
                for y in dct[e][ee][x]:
                    tot1 += dct[e][ee][x][y]
            print('\t' + EDUCATION_DIR[ee] + ': ' + str(tot1/4))
            for r in RATINGS:
                if r not in dct[e][ee]:
                    continue
                print('\t\t' + RATING_NAMES[RATINGS.index(r)] + ': ')
                avg = 0
                tot2 = 0
                for x in dct[e][ee][r]:
                    if x not in RATING_DIR:
                        avg += int(x)*dct[e][ee][r][x]
                        tot2 += dct[e][ee][r][x]
                if tot2 == 0:
                    continue
                avg /= tot2
                sd = 0
                for x in dct[e][ee][r]:
                    if x not in RATING_DIR:
                        sd += ((avg-int(x))**2)*dct[e][ee][r][x]
                sd /= tot2
                sd = sd**0.5
                print('\t\t\tAverage : ' + str(avg))
                print('\t\t\tStandard Deviation : ' + str(sd))
            print()
