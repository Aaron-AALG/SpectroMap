SpectroMap
======================

![python-version](https://img.shields.io/badge/python->=3.8-blue.svg)
[![pypi-version](https://img.shields.io/pypi/v/spectromap.svg)](https://pypi.python.org/pypi/spectromap/)
![license](https://img.shields.io/pypi/l/spectromap.svg)
[![Downloads](https://static.pepy.tech/personalized-badge/spectromap?period=total&units=none&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/spectromap)
[![CodeFactor](https://www.codefactor.io/repository/github/aaron-aalg/spectromap/badge)](https://www.codefactor.io/repository/github/aaron-aalg/spectromap)
[![](https://img.shields.io/badge/doi-10.48550/ARXIV.2211.00982+-blue.svg)](https://arxiv.org/abs/2211.00982)



SpectroMap is a peak detection algorithm that computes the constellation map (or audio fingerprint) of a given signal.

![img](Images/peak_search.png)

An example of the SectroMap implementation can be found in our [research paper](https://doi.org/10.1007/978-3-031-07015-0_16):

López-García, A., Martínez-Rodríguez, B., Liern, V. (2022). *A Proposal to Compare the Similarity Between Musical Products. One More Step for Automated Plagiarism Detection?* In: Montiel, M., Agustín-Aquino, O.A., Gómez, F., Kastine, J., Lluis-Puebla, E., Milam, B. (eds) Mathematics and Computation in Music. MCM 2022. Lecture Notes in Computer Science(), vol 13267. Springer, Cham. https://doi.org/10.1007/978-3-031-07015-0_16


Installation
======================

You can install the SpectroMap library from GitHub:

```terminal
git clone https://github.com/Aaron-AALG/spectromap.git
python3 -m pip install -e spectromap
```

You can also install it directly from PyPI:

```terminal
pip install spectromap
```

Usage
======================

This packages contains the spectromap object that manages the full process of audio fingerprinting extraction. Given a signal Y, we just have to instantiate the class with Y and the corresponding kwargs (if needed).

spectrogram object
------------------

An example to apply SpectroMap over a signal is:

```python
import numpy as np
from spectromap.spectromap import *

y = np.random.rand(44100)
kwargs = {'fs': 22050, 'nfft': 512, 'noverlap':64}

# Instantiate the SpectroMap object
SMap = spectromap(y, **kwargs)

# Get the spectrogram representation plus its time and frequency bands
f, t, S = SMap.get_spectrogram()

# Extract the topological prominent elements from the spectrogram, known as "Peak detection".
# We get the coordinates (time, freq) of the peaks and the matrix with just these peaks.
fraction = 0.15 # Fraction of spectrogram to compute local comparisons
condition = 2   # Axis to analyze (0: Time, 1: Frequency, 2: Time+Frequency)
id_peaks, peaks = SMap.peak_matrix(fraction, condition)

# Get the peaks coordinates as as (s, Hz, dB)-array.
extraction_t_f_dB = SMap.from_peaks_to_array()
```

peak_search function
------------------

In case you desire to compute the spectrogram by yourself, then you can make use of the peak search function instead.

```python
from spectromap.spectromap import *

fraction = 0.05 # Fraction of spectrogram to compute local comparisons
condition = 2   # Axis to analyze (0: Time, 1: Frequency, 2: Time+Frequency)
id_peaks, peaks = peak_search(spectrogram, fraction, condition)
```

Cite this work
======================

If you use SpectroMap in your research I would appreciate a citation to the [following paper](https://arxiv.org/abs/2211.00982):

```bibtex
@misc{https://doi.org/10.48550/arxiv.2211.00982,
  doi = {10.48550/ARXIV.2211.00982},
  url = {https://arxiv.org/abs/2211.00982},
  author = {López-García, Aarón},
  title = {SpectroMap: Peak detection algorithm for audio fingerprinting},
  publisher = {arXiv},
  year = {2022},
  copyright = {Creative Commons Attribution 4.0 International}
}
```
