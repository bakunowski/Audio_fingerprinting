import numpy as np
import librosa
import hashlib
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                      binary_erosion, iterate_structure)


def calculate_spectrogram(audio_file):
    '''
    Calculates a spectrogram (2D numpy array) of a given audio file
    '''
    samples, sr = librosa.load(audio_file, sr=22050)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(samples)), ref=np.max)

    return D


# find peaks in spectrogram
# https://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array
def detect_peaks(arr2D, amp_min=-50, plot=False):
    """
    Takes a spectrogram and detects the peaks using the local maximum filter
    Parameters:
        amp_min - minimum aplitude of the frequency value
                    to be considered a peak (in dB)

    Returns a list of (n, k) coordinates of the peaks, where
    n is the frequency and k is the time index
    """
    # define an 8-connected neighborhood
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, 20)

    # apply the local maximum filter; all pixels of maximal value
    # in their neighborhood are set to 1
    local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
    background = (arr2D == 0)
    eroded_background = binary_erosion(background,
                                       structure=neighborhood,
                                       border_value=1)
    # final mask
    detected_peaks = local_max ^ eroded_background

    # extract peaks
    amps = arr2D[detected_peaks]
    j, i = np.where(detected_peaks)

    # filter peaks
    amps = amps.flatten()
    peaks = zip(i, j, amps)
    frequency_idx = []
    time_idx = []
    for stamp in [x for x in peaks if x[2] > amp_min]:
        frequency_idx.append(stamp[1])
        time_idx.append(stamp[0])

    if plot:
        # scatter of the peaks
        fig, ax = plt.subplots()
        ax.imshow(arr2D)
        ax.scatter(time_idx, frequency_idx, c='red', marker='x')
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        ax.set_title("Spectrogram")
        plt.gca().invert_yaxis()
        plt.show()

    return list(zip(frequency_idx, time_idx))


# create hash
# this is not the anchor - target zone implementation
# here we just use pairs of points to create hashes
def generate_hashes(peaks, fan_value=15):
    """
    Hash list structure:
       sha1_hash[0:20]    time_offset
    [(e05b341a9b77a51fd26, 32), ... ]
    """
    # if True:
    #     peaks.sort(key=itemgetter(1))

    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks):

                freq1 = peaks[i][0]
                freq2 = peaks[i + j][0]
                t1 = peaks[i][1]
                t2 = peaks[i + j][1]
                t_delta = t2 - t1

# TODO: we can concatenate hashes into 32bit uint
                if t_delta >= 0 and t_delta <= 200:
                    h = hashlib.sha1(
                        ("%s|%s|%s" % (str(freq1),
                                       str(freq2),
                                       str(t_delta))).encode('utf-8'))
                    yield (h.hexdigest()[0:20], t1)
