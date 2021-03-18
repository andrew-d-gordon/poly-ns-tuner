from librosa import load
from poly_note_detection import *

# SET CONSTANTS

num_pitches = 1
num_candidates = 5

# LOAD SAMPLE/PREP BUFFER
data, sr = load('samples/glocka52.wav')

# COMPUTE FOURIER TRANSFORM (VIA DFT)
yf, xf, audio_len = computeFT(data, sr)

# CONVERT MAGNITUDE
yf_mag_convert = convert_magnitude(yf, audio_len)
print("This is yf elem:", yf[2671], ", this is converted:", yf_mag_convert[2671])
print("This is yf elem:", yf[7222], ", this is converted:", yf_mag_convert[7222])

# CANDIDATE PEAK SELECTION
current_peaks, candidate_peak_freqs = collect_peaks(yf, xf, audio_len, num_candidates)

#PRINT CURRENT CANDIDATE PEAKS (FREQS AND KEYS)
print(current_peaks)
print(candidate_peak_freqs)

# CANDIDATE PEAK LIKELIHOOD AND PITCH SELECTION (magnitude, harmonics, duration?)

# DURATION/END AND START NOTE MONITORING













'''
L(f) is a non-negative likelihood function where f is frequency. The presence of peaks at or near multiples of f increases
L(f) in a way which depends on the peak's amplitude and frequency as shown:

L(f) = Summation(i=0,k){ai*ti*ni}
Where k is number of peaks in the spectrum, 
-ai is a factor depending on the amplitude of the ith peak,
-ti depends on how closely the ith peak is tuned to a multiple of fi
-ni depends on whether the peak is closest to a low or high multiple of f

For monophonic pitch estimation, we simply output the value of f whose "likelihood" is highest.
For polyphonic pitch estimation, we successively take the values of f of greatest likelihood which are neither multiples
nor sub-multiples of a previous one.  (loosen up on being sub multiple for octaves)

In all cases, last criteria to determine if there is pitch (as L(f) will always have a maximum even if no pitch).
Our criterion is that there either be at least four peaks present or else that the fundamental be present and the total 
power of contributing peaks be at least a hundredth of the signal power.
'''

# 5 peaks glocka2:

# [('A6', 1759.4416562107906),
# # ('D8', 4757.277289836888),
# # ('B8', 8031.116687578419),
# # ('D#9', 9788.58218318695),
# # ('A#6', 1812.1392722710164)]

'''
Notes/Pseudo:
Algo originally uses optimized discrete hartley transform, any reasonably fast dft algo should be fine.
Rob Mayer wrote traditionally used code for this algorithm, denoted "Fastest Fourier Transform in the West"

1) Fiddle~ computes a DFT of a block of input, zeropadded by a factor of four, three main steps:
    1.1) Initial Computation,
    1.2) Spectral interpolation, 
    1.3) and frequency domain windowing

1.1) Initial Computation
Suppose you have a real, length N signal x[n], and we modulate signal by complex exponential e^-j*(pi/2N)*n to obtain:
xmod[n] = x[n]*e^-j*(pi/2N)*n

We can compute DFT of this modulated signal as:

Xmod[k] = Summation(n=0, N-1){x[n]*(e^-j*(pi/2N)*n)*(e^-j*(2pi/N)*kn)} = Summation(n=0, N-1){x[n]*(e^-j*(pi/2N)*(4k+1)n)}
for k E [0, N-1].

Now suppose we take same signal x[n], and rather than modulate it, we zeropad it to length 4N to obtain a signal xzeropad[n].
DFT of this new signal is...
Xzeropad[k]=Summation(n=0, N-1){x[n]*(e^-j*(2pi/4N)*kn)}=Summation(n=0, N-1){x[n]*(e^-j*(pi/2N)*kn)}
for k E [0, 4N-1]. Note that...

Xmod[k] = Xzeropad[4k+1]

Guessing Fundamental Frequencies...

L(f) is a non-negative likelihood function where f is frequency. The presence of peaks at or near multiples of f increases
L(f) in a way which depends on the peak's amplitude and frequency as shown:

L(f) = Summation(i=0,k){ai*ti*ni}
Where k is number of peaks in the spectrum, 
-ai is a factor depending on the amplitude of the ith peak,
-ti depends on how closely the ith peak is tuned to a multiple of fi
-ni depends on whether the peak is closest to a low or high multiple of f

For monophonic pitch estimation, we simply output the value of f whose "likelihood" is highest.
For polyphonic pitch estimation, we successively take the values of f of greatest likelihood which are neither multiples
nor sub-multiples of a previous one.  (loosen up on being sub multiple for octaves)

In all cases, last criteria to determine if there is pitch (as L(f) will always have a maximum even if no pitch).
Our criterion is that there either be at least four peaks present or else that the fundamental be present and the total 
power of contributing peaks be at least a hundredth of the signal power.

'''