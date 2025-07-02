"""
Man_Bkgrd_Scan_FFT
~~~~~~~~~~~~~~~~~~
This script takes binary files produced using USRP 'rx_samples_to_file' utility using the 'Man_Bkgrd_Scan.py' script, performs an FFT and saves an image of each spectrum.
Spectrums are produced for all 20 off receive channels (16 off main, 4 off interferometer) accross all 10 licenced bands.
It produces 200 FFT image files (png) which are saved to the /home/radar/UOL_scripts/Manual_Background_Scan/exported_images/BandX/ directory.
NOTE: The centre frequencies and sample rate *must* match those used to generate the binary files or the FFTs produced will be wrong!

:copyright: 2020-2025 University of Leicester
"""

import numpy as np
import matplotlib.pyplot as plt

# Declare constants
bands = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
centre_f = [9090e3, 9947.5e3, 11125e3, 11575e3, 13475e3, 13885e3, 16295e3, 18041e3, 19547.5e3, 19895e3] # Centre frequency of licenced bands, Hz
low_freq = [9040e3, 9900e3, 11075e3, 11550e3, 13440e3, 13870e3, 16210e3, 18030e3, 19415e3, 19800e3] # Start frequency of licenced bands, Hz
high_freq = [9140e3, 9995e3, 11175e3, 11600e3, 13510e3, 13900e3, 16380e3, 18052e3, 19680e3, 19990e3] # Stop frequency of licenced bands, Hz
sample_rate = 301205 # sample rate (samples per second)
IQ_format = 'short'
sample_per = 1/sample_rate # Sample period (seconds)
ADC_levels = 2**16 # Note LFRX ADC is 14 bit, but IQ occupies full 'int16' type.
ADC_full_scale = 2 # LFRX maximum input is 2Vpp
Z = 50 # System impedance (Ohms)

# Generate list of file names
filenames = []
for x in range (0,10):
    for y in range (0, 16):
        filenames.append("Clear_Scan_Main{}_Band{}".format(y, x))
    for y in range (0, 4):
        filenames.append("Clear_Scan_Intf{}_Band{}".format(y, x))

# For each IQ file, generate fft and save image file
filename_index = 0 # Index used to to extract filename from list for each 'rx_samples_to_file' call
for x in range (0,10): # loop through each TX band
    for y in range (0,20): # loop through all receive channels (16 off main, 4 off interferometer)
        # Read file
        IQ = np.fromfile('/home/radar/UOL_scripts/Manual_Background_Scan/dat_files/' + filenames[filename_index] + '.dat', dtype=np.int16)

        # Convert to volts
        LSB_volts = ADC_full_scale/ADC_levels;
        IQ = IQ*LSB_volts;

        # # Separate I & Q, then join to complex
        I = IQ[0::2]
        Q = IQ[1::2]
        IQ = I + Q*1j

        # Create time axis
        L = len(IQ);
        timeax = np.linspace(0, ((L-1)*sample_per), L)

        # Plot IQ in time domain
        #fig, ax1 = plt.subplots()
        #ax1.plot(timeax, I, label="I")
        #ax1.plot(timeax, Q, label="Q")
        #ax1.plot(timeax, np.sqrt(I**2 + Q**2), label="A")
        #ax1.legend(loc="upper right")
        #ax1.set_xlabel('Time (s)')
        #ax1.set_ylabel('Voltage (V)')
        #plt.savefig('/home/radar/UOL_scripts/Manual_Background_Scan/exported_images/Band' + str(x) + '/' + filenames[filename_index] + '.png', bbox_inches='tight')
        #plt.close

        # Perform complex FFT and normalise
        fftIQ = np.fft.fft(IQ)
        P = abs(fftIQ/L)
        P = np.fft.fftshift(P) # Shift the zero-freuqency component to the centre of the spectrum

        # Convert from V to dBm
        P = P * (1/(np.sqrt(2))) # From Vpeak to VRMS
        P = 10 * np.log10((P**2*1000/Z)) # From VRMS to dBm

        #% Create frequency axis (in MHz)
        freqax = np.linspace(-1*sample_rate/2, sample_rate/2, L)
        freqax = (freqax / 1e6) + (centre_f[x] / 1e6)

        # Plot FFT
        fig, ax2 = plt.subplots()
        ax2.plot(freqax, P, linewidth=0.5)
        ax2.set_xlabel('Frequency (MHz)')
        ax2.set_ylabel('Power (dBm)')
        plt.ylim(-130, 0)
        plt.title(filenames[filename_index])
        plt.axvspan(low_freq[x]*1e-6, high_freq[x]*1e-6, color='green', alpha=0.5)
        plt.savefig('/home/radar/UOL_scripts/Manual_Background_Scan/exported_images/Band' + str(x) + '/' + filenames[filename_index] + '.png', bbox_inches='tight')
        plt.close()
        filename_index += 1


