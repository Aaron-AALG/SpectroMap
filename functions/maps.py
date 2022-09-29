import numpy as np
from scipy import signal

class spectromap(object):
    '''
    SpectroMap is a peak detection algorithm that computes the constellation map (audio fingerprint) of a given signal.

    It makes use of the `scipy.signal` module to conduct the spectrogram and the peak detection by bands.

    To instantiate the object, it just needs the signal `y`, but you can also add some `kwargs`.
    '''
    def __init__(self, y, **kwargs):
        self.y = y
        self.kwargs = kwargs

    def get_spectrogram(self, log_scale = False):
        '''
        Compute the spectrogram of a given signal by using the `signal.spectrogram` function.
        
        Parameters
        ----------
            y:         time series of the signal amplitude.
            log_scale: Boolean to transform to logaritmic scale.

        kwArguments: Arguments for the `signal.spectrogram` function.
            fs:              Sample rate of the signal.
            window:          Window as `signal.windows` function.
            nfft:            Number of FFT to compute.
            noverlap:        Number of elements to overlap between sequences.
            nperseg:         Sequence length.
            Among others: ...

        Returns
        ----------
            f: Frequency-band.
            t: Time-band.
            S: Spectrogram.
        '''
        f, t, S = signal.spectrogram(self.y, **self.kwargs)
        
        # Transform to log10-scale
        if log_scale:
            S = 20 * np.log10(S / S.min())
        
        # Add variables to self
        self.f = f
        self.t = t
        self.spectrogram = S
        
        return f, t, S
    
    def peak_matrix(self, fraction=0.1, condition=2):
        '''
        Function that spots significant peaks in a given spectrogram.

        Parameters
        ----------
            fraction (float) : Fraction of spectrogram band to compute local comparisons, value between 0 and 1. By default `fraction=0.1`.
            condition (int)  : Axis in which we search the peaks. By default `condition=2`.
                axis=0: Time-based search (By rows).
                axis=0: Frequency-based search (By columns).
                axis=2: Time-Frequency-based search (Row+Columns).
        
        Returns
        ----------
            id_peaks (np.array): Array with the position (t,f) in which the peaks appear.
            peaks    (np.array): Array spectrogram-shaped just with the peaks in the same position.
        '''
        # Get Frenquency-Time-Spectrogram representations
        spectromap.get_spectrogram(self)
        
        # Time based
        if condition == 0:
            # Transpose and flat the spectrogram
            x = self.spectrogram.T
            x = x.flatten()
            # Find peaks according to the set length
            d = int(fraction*self.spectrogram.shape[condition])
            idx, _ = signal.find_peaks(x, distance=d)
            # Get matrix with the position of the peaks
            id_peaks = np.zeros(x.shape)
            id_peaks[idx] = True
            id_peaks = np.reshape(id_peaks, self.spectrogram.T.shape).T.astype('bool')

        # Frequency based
        elif condition == 1:
            x = self.spectrogram.flatten()
            # Find peaks according to the set length
            d = int(fraction*self.spectrogram.shape[condition])
            idx, _ = signal.find_peaks(x, distance=d)
            # Get matrix with the position of the peaks
            id_peaks = np.zeros(x.shape)
            id_peaks[idx] = True
            id_peaks = np.reshape(id_peaks, self.spectrogram.shape).astype('bool')

        # Time-Frequency based
        elif condition == 2:
            # Find peaks for both axis
            id_peaks0, _ = spectromap.peak_matrix(self, fraction, condition=0)
            id_peaks1, _ = spectromap.peak_matrix(self, fraction, condition=1)
            # Get just the points that are considered peaks in both axis
            id_peaks = (id_peaks0.astype('int32') + id_peaks1.astype('int32')) == 2
        
        # Return just the peaks of the spectrogram
        peaks = np.zeros(self.spectrogram.shape)
        peaks[id_peaks] = self.spectrogram[id_peaks]

        return id_peaks, peaks

    def from_peaks_to_array(self):
        '''
        By means of the peak_matrix, it reshapes the coordinates (t,f) to return the N detected peaks.
        Returns the positional prominent elements of the spectrogram as (s,Hz,dB)-array.
        '''
        # Compute local search
        id_peaks, peaks = spectromap.peak_matrix(self)

        # Extract the Time-Frequency-Amplitude components
        time_band = np.tile(self.t, (self.spectrogram.shape[0], 1)).flatten()[id_peaks.flatten()]
        freq_band = np.tile(self.f, (self.spectrogram.shape[1], 1)).flatten()[id_peaks.flatten()]
        bels_band = self.spectrogram.flatten()[id_peaks.flatten()]

        return np.array([time_band, freq_band, bels_band]).T


def peak_search(spectrogram, fraction=0.1, condition=2):
    '''
    Function that spots significant peaks in data. It makes use of the SciPy modules to detect and fetch such values.

    Parameters
    -----
        spectrogram (np.array)  : Array with the spectrogram to analyze.
        fraction        (float) : Fraction of spectrogram to compute local comparisons, value between 0 and 1. By default `fraction=0.1`.
        condition         (int) : Axis in which we search peaks. By default `condition=0`.
            The axes for detection are:
                0: Time (columns).
                1: Frequency (rows).
                2: Time-Frequecy (Both, more restrictive).

    Returns
    -----
        idx (np.array)    : Array with the position (t,f) in which the peaks appear.
        values (np.array) : Array spectrogram-shaped just with the peaks in the same position.
    '''
    # Get where are the peaks and their values
    # Time based
    if condition == 0:
        # Transpose and flat the spectrogram
        x = spectrogram.T
        x = x.flatten()
        # Find peaks according to the set length
        d = int(fraction*spectrogram.shape[condition])
        idx, _ = signal.find_peaks(x, distance=d)
        # Get matrix with the position of the peaks
        id_peaks = np.zeros(x.shape)
        id_peaks[idx] = True
        id_peaks = np.reshape(id_peaks, spectrogram.T.shape).T.astype('bool')

    # Frequency based
    elif condition == 1:
        x = spectrogram.flatten()
        # Find peaks according to the set length
        d = int(fraction*spectrogram.shape[condition])
        idx, _ = signal.find_peaks(x, distance=d)
        # Get matrix with the position of the peaks
        id_peaks = np.zeros(x.shape)
        id_peaks[idx] = True
        id_peaks = np.reshape(id_peaks, spectrogram.shape).astype('bool')

    # Time-Frequency based
    elif condition == 2:
        # Find peaks for both axis
        id_peaks0, _ = peak_search(spectrogram, fraction, condition=0)
        id_peaks1, _ = peak_search(spectrogram, fraction, condition=1)
        # Get just the points that are considered peaks in both axis
        id_peaks = (id_peaks0.astype('int32') + id_peaks1.astype('int32')) == 2
    
    # Return just the peaks of the spectrogram
    peaks = np.zeros(spectrogram.shape)
    peaks[id_peaks] = spectrogram[id_peaks]
    return id_peaks, peaks
