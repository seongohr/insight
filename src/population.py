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
    #     not_tract += v['not_num_tract10']
    # print(not_tract)


def make_data(heading, contents):
    CBSA_dict = {}
    CBSA_code = heading['CBSA09']
    CBSA_title = heading['CBSA_T']
    census_tracts = heading['TRACT10']
    pop00 = heading['POP00']
    pop10 = heading['POP10']
    ppchg = heading['PPCHG']
    count = 2

    for row in contents:
        code = row[CBSA_code]
        if code == '':
            count += 1
            continue
        not_num_ct = 0
        title = row[CBSA_title]
        ct = row[census_tracts]
        p00 = int(row[pop00])
        p10 = int(row[pop10])
        p_ch = (row[ppchg].replace(',', ''))

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
            CBSA_dict[code]['title'] = title
            if ct not in CBSA_dict[code]['tract10']:
                CBSA_dict[code]['tract10'].add(ct)
                CBSA_dict[code]['num_tract10'] += 1
            CBSA_dict[code]['pop00'] += int(p00)
            CBSA_dict[code]['pop10'] += int(p10)
            CBSA_dict[code]['ppchg'] += p_ch
            CBSA_dict[code]['not_num_tract10'] += not_num_ct
        count += 1

    return OrderedDict(sorted(CBSA_dict.items()))

if __name__ == '__main__':
    heading, contents = read_file()
    result = make_data(heading, contents)
    write_file(result)