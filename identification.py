import os
import numpy as np
import generate_hash as g


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
        occurences = {}
        for file in os.listdir(fingerprints):
            d = {}
            with open(os.path.join(fingerprints, file), 'r') as f:
                for line in f:
                    (key, val, songID) = line.split(',')
                    key = key.replace("(", "").replace("'", "")
                    val = val.replace(',', '')
                    songID = songID.replace(")", "")
                    d[str(key)] = int(val)

            items = []
            for k in h.keys() & d.keys():
                # retain the number of values for which d[k] - h[k]
                # is repeated most often
                # this gives number of number of true matches

                # add all time offset differences to a list
                items.append(d[k] - h[k])

            if len(items) > 0:
                iitems = np.asarray(items)
                hist, bin_edges = np.histogram(iitems, density=False)
                aa = hist.max()
                # put the name of fingerprint, and number of true matches
                # in a datastructure
                occurences[file] = aa

        # sort that datastructure and retain only three highest hits
        sorted_dict = {k: v for k, v in sorted(
            occurences.items(), key=lambda item: item[1])}

        # write to file
        with open(output, 'a+') as f:
            f.write(query_file)
            f.write('\t')
            for k in list(reversed(list(sorted_dict)))[0:1]:  # filter three best scoring results
                f.write(k)
                f.write('\t')
            f.write('\n')

        if i % 10 == 0:
            print('Identified snippets:', i)
        i += 1


audioIdentification('query_recordings',
                    'fingerprints30',
                    'output30.txt')
