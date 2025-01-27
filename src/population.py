import csv
from collections import OrderedDict

INPUT_PATH = './input/censustract-00-10.csv'
OUTPUT_PATH = './output/report.csv'


def read_file():
    contents = []
    csv_headings = []
    with open(INPUT_PATH, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        csv_headings = next(reader)
        csv_headings = {k: v for v, k in enumerate(csv_headings)}

        for r in reader:
            contents.append(r)
    return csv_headings, contents


def write_file(result):
    with open(OUTPUT_PATH, 'w') as f:
        csv_writer = csv.writer(f, delimiter=',')
        for CBSA, values in result.items():
            csv_writer.writerow([CBSA, values['title'], values['num_tract10'], values['pop00'], values['pop10'],
                                 round(values['ppchg'] / (values['num_tract10'] - values['not_num_tract10']), 2)])


def print_dict(dic):
    not_tract = 0
    for k,v in dic.items():
        print(k, v)
        not_tract += v['not_num_tract10']
    print(not_tract)


def make_data(heading, contents):
    CBSA_dict = {}
    CBSA_code = heading['CBSA09']
    CBSA_title = heading['CBSA_T']
    census_tracts = heading['TRACT10']
    pop00 = heading['POP00']
    pop10 = heading['POP10']
    ppchg = heading['PPCHG']

    for row in contents:
        code = row[CBSA_code]
        if code == '':
            continue
        not_num_ct = 0  # used for denominator used for calculating avg population change
        title = row[CBSA_title]
        ct = row[census_tracts]
        p00 = row[pop00]
        p10 = row[pop10]
        p_ch = (row[ppchg].replace(',', ''))

        # check population in 2000 can be converted to integer
        try:
            p00 = int(row[pop00])
        except:
            p00 = 0

        # check population in 2010 can be converted to integer
        try:
            p10 = int(row[pop10])
        except:
            p10 = 0

        # check population change can be converted to float
        try:
            p_ch = float(p_ch)
        except:
            not_num_ct = 1
            p_ch = 0

        if code not in CBSA_dict:
            CBSA_dict[code] = {'title': title,
                               'tract10': set([ct]),
                               'num_tract10': 1,
                               'pop00': p00,
                               'pop10': p10,
                               'ppchg': p_ch,
                               'not_num_tract10': not_num_ct
                               }
        else:
            if CBSA_dict[code]['title'] == '':
                CBSA_dict[code]['title'] = title
            if ct not in CBSA_dict[code]['tract10']:
                CBSA_dict[code]['tract10'].add(ct)
                CBSA_dict[code]['num_tract10'] += 1
            CBSA_dict[code]['pop00'] += p00
            CBSA_dict[code]['pop10'] += p10
            CBSA_dict[code]['ppchg'] += p_ch
            CBSA_dict[code]['not_num_tract10'] += not_num_ct

    return OrderedDict(sorted(CBSA_dict.items()))

if __name__ == '__main__':
    heading, contents = read_file()
    result = make_data(heading, contents)
    write_file(result)