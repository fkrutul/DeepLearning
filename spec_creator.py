# -*- coding: utf-8 -*-
"""
Created on Mon Apr 5 14:23:52 2021

The way this was intended was to import a single song as type ".wav".

Prefered image size should be changed in the "my_img_size" variable.
We are attempting to use VGG which accepts 244x244 image sizes.
DPI Variable may also be changed, however most computers have a DPI of 96.

While this was intended to create 30 second slices, 
that value may be changed with the "num_seconds" variable.
"""

import sys
import numpy as np
from math import floor
import matplotlib.pyplot as plt
from scipy.io.wavfile import read as w_read



wav_path = str(sys.argv[1])

#CHANGE ME

#wav_path = "./test_song.wav"
save_path = "./test_song_imgs"
num_seconds = 30

#Initialize variables for VGG Sized Images (244x244)
my_dpi      = 96
my_img_size = 224
time_bins   = my_img_size

resize_img = my_img_size + 66  #DO NOT CHANGE, Due to matplotlib borders, we must adjust
my_img_size = resize_img

#Initialize variables to catch largest and smallest spectrogram ranges
min_spec_range = [99999, 99999]
max_spec_range = [    0,     0]


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Initialize Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def BinnedFFT(data, time_bins, time_bin_len):
    Spectrogram2D = np.zeros((int(time_bin_len*0.5)+1, time_bins))
    
    for j in range(time_bins):
        Binned_FFT = np.abs(np.fft.rfft(data[j*time_bin_len : (j+1)*time_bin_len]))
        Spectrogram2D[:len(Binned_FFT), j] = Binned_FFT[::-1]
        
    return Spectrogram2D


def Normalize(data, bitrate, samples):
    norm_data = np.zeros(samples)
    maxi = np.max(data)
      
    #Scale Data Points where Max = 1
    norm_data = ((1 - 1/(2^bitrate))/maxi) * data
       
    return norm_data


#~~~~~~~~~~~~~~~~~~~~~~Walk Folders and Generate Spectrograms~~~~~~~~~~~~~~~~~~

#Read file and create important variables

rate, data = w_read(wav_path)

try:
    data = data.sum(axis=1) / 2                  #create mono track from average of Left and Right channels
except:
    print("file already mono track")

num_samples = len(data)                          #determine number of samples in full file
seconds = num_samples / rate                     #determine its length in seconds
num_images = int(floor(seconds/num_seconds))     #determine number of 30 second images that can exist
samps30s = num_seconds * rate                    #determine number of samples inside of the 30 second clip
data = Normalize(data, rate, num_samples)        #normalize full file (maybe should normalize sections?)
freq_bins = np.fft.rfftfreq(samps30s, d=1./rate) #determine number of frequency bins for Binned FFT
time_bin_len = int(samps30s/time_bins)           #determine length of time bins for 30 second slices


#Iterate over 30 second slices, omitting first and last slice as intro and outro are outliers
for i in range(1, num_images-1):    

    img_save_name = str(save_path + "/" + "test_song_" + str(i) + ".png")
    
    #Create Spectrogram using numpy's Fast Fourier Transform in a Binned Application
    spectrogram = BinnedFFT(data[i*samps30s:(i+1)*samps30s], time_bins, time_bin_len)
    
    #The Ultra high frequency information is not so useful to us.
    #Audio is recorded at very high sampling rates for clarity
    #The most important audio information, though exists in the lower area
    spec_size = spectrogram.shape
    half_height = floor(spec_size[0] / 2)
    spectrogram = spectrogram[half_height:] 
    


    
    #Create and save plot of spectrogram
    plt.clf()
    plt.figure(figsize = (my_img_size/my_dpi, (my_img_size+8)/my_dpi))
    fig = plt.imshow(spectrogram, aspect='auto', vmax=25, cmap="brg")
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.axis("off")
    plt.savefig(img_save_name, dpi=my_dpi, bbox_inches='tight', pad_inches=0)
    plt.close()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("Spectrogram Creation Complete!\n\n")

                
