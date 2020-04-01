import numpy as np
import os
import generate_hash as g


def fingerprintBuilder(database, fingerprints):
    i = 0
    for file in os.listdir(database):
        # calculate hashes for each file
        spec_array = g.calculate_spectrogram(os.path.join(database, file))
        stamps = g.detect_peaks(spec_array, -20, plot=False)
        a = g.generate_hashes(stamps, fan_value=15)

        # write the peak values to a file, with identical name as the original
        with open(os.path.join(fingerprints, file), 'a+') as f:
            for x in a:
                x = str(x)
                f.write(x)
                f.write('\n')

        if i % 10:
            print('Files fingerprinted:', i)

        i += 1


fingerprintBuilder('database_recordings', 'fingerprints')