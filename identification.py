import os
import generate_hash as g
from collections import Counter


def audioIdentification(query, fingerprints, output):
    i = 0
    for query_file in os.listdir(query):

        # build fingerprint for current query file
        spec_array = g.calculate_spectrogram(os.path.join(query, query_file))
        stamps = g.detect_peaks(spec_array)
        hashes = g.generate_hashes(stamps, fan_value=15)

        h = {}  # initialise dictionary containing all hashes and offsets
        for x in hashes:
            h[str(x[0])] = x[1]

        # compare hashes dict with all the fingerprints in database
        amount = {}
        occurences = {}
        items2 = []
        for file in os.listdir(fingerprints):
            d = {}
            with open(os.path.join(fingerprints, file), 'r') as f:
                for line in f:
                    (key, val) = line.split()
                    key = key.replace("(", "").replace(
                        ",", "").replace("'", "")
                    val = val.replace(")", "")
                    d[str(key)] = int(val)

            items = []
            for k in h.keys() & d.keys():
                # retain the number of values for which d[k] - h[k]
                # is repeated most often
                # this gives number of number of true matches
                if (d[k] - h[k]):
                    items.append(d[k] - h[k])
            if len(items) > 1:
                c = Counter(items).most_common(5)
                # print(len(items))
                # print(c)
                # print('In File:', file, query_file)
                items2.append(len(items))
                # a, b = c[0]
                occurences[file] = len(items)
        # print(items2)
        # print(sorted(items2))

        # put the name of fingerprint, and number of true matches
        # in a datastructure

        # sort that datastructure and retain only three highest hits
        # ex = compare_hashes('temporary_hashes_file',
        #                     os.path.join(fingerprints, file))
        # d[file] = ex

        # sort the output
        sorted_dict = {k: v for k, v in sorted(
            occurences.items(), key=lambda item: item[1])}
        # print(sorted_dict)

        # filter three best scoring results
        a = {k for k in list(reversed(list(sorted_dict)))[0:3]}

        # write to file
        with open(output, 'a+') as f:
            f.write(query_file)
            f.write('\t')
            for k in list(reversed(list(sorted_dict)))[0:3]:
                f.write(k)
                f.write('\t')
            f.write('\n')

        if i % 9:
            print(i)
        i += 1


def compare_hashes(hash1, hash2):
    with open(hash1, 'r') as file1:
        with open(hash2, 'r') as file2:
            same = set(file1).intersection(file2)
            same.discard('\n')
            i = 0
            for line in same:
                i += 1
            return i


audioIdentification('test_query',
                    'fingerprints_50',
                    'output_50.txt')
