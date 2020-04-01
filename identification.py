import os
import generate_hash as g


def audioIdentification(query, fingerprints, output):
    i = 0
    for query_file in os.listdir(query):

        # build fingerprint for current query file
        spec_array = g.calculate_spectrogram(os.path.join(query, query_file))
        stamps = g.detect_peaks(spec_array, -10, plot=False)
        hashes = g.generate_hashes(stamps, fan_value=15)

        # write all hashes to a temporary file
        with open('temporary_hashes_file', 'a+') as f:
            for x in hashes:
                x = str(x)
                f.write(x)
                f.write('\n')

        # compare file with all the others
        d = {}
        for file in os.listdir(fingerprints):
            ex = compare_hashes('temporary_hashes_file',
                                os.path.join(fingerprints, file))
            d[file] = ex

        # sort the output
        sorted_dict = {k: v for k, v in sorted(
            d.items(), key=lambda item: item[1])}

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

        os.remove('temporary_hashes_file')
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


audioIdentification('query_recordings',
                    'fingerprints',
                    'output.txt')
