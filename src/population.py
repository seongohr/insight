import csv
from collections import OrderedDict

INPUT_PATH = '../input/censustract-00-10.csv'
OUTPUT_PATH = '../output/report.csv'


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
                                 round(values['ppchg'] / values['num_tract10'], 2)])


def print_dict(dic):
    for k,v in dic.items():
        print(k, v)


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
        # title = '"{}"'.format(row[CBSA_title])
        title = row[CBSA_title]
        ct = row[census_tracts]
        p00 = int(row[pop00])
        p10 = int(row[pop10])
        p_ch = (row[ppchg].replace(',', ''))

        if row[ppchg] == '(X)':
            if p00 == 0:
                try:
                    p_ch = float((((p10 + 1.0) - (p00 + 1.0)) * 100) / (p00 + 1) )
                except:
                    print('N/A', count, p00, p10, row[ppchg])
        else:
            try:
                p_ch = float(p_ch)
            except:
                print('not a number', count, row[ppchg])

        if code not in CBSA_dict:
            CBSA_dict[code] = {'title': title,
                               'tract10': set([ct]),
                               'num_tract10': 1,
                               'pop00': p00,
                               'pop10': p10,
                               'ppchg': p_ch
                               }
        else:
            CBSA_dict[code]['title'] = title
            if ct not in CBSA_dict[code]['tract10']:
                CBSA_dict[code]['tract10'].add(ct)
                CBSA_dict[code]['num_tract10'] += 1
            CBSA_dict[code]['pop00'] += int(p00)
            CBSA_dict[code]['pop10'] += int(p10)
            CBSA_dict[code]['ppchg'] += p_ch
        count += 1

    return OrderedDict(sorted(CBSA_dict.items()))

if __name__ == '__main__':
    heading, contents = read_file()
    result = make_data(heading, contents)
    write_file(result)