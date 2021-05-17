# Genre Recognition with VGG16

We have implemented an audio recognition transfer of VGG16 trained on different musical genres in a jupyter notebook (.ipynb). Our latest model reaches 85% accuracy on 10 genres: ['Classical',
 'EDM',
 'Folk',
 'Funk',
 'HipHop',
 'Jazz',
 'Latin',
 'LoFi',
 'Punk',
 'Rock']. 
We wanted to start with our own raw audio instead of downloading a precompiled dataset. 

There are a series of steps taken to produce a model capable of predicting a genre classification for audio files. The first step is implementing binned FFT to create spectrograms of the songs. We chose to cut the songs into 30-second slices and train with the resulting spectrograms, omitting the upper-frequency register and also the first and last slices. Included also is a pre-trained network weight .h5 file.

If you just want to run our implementation, you may skip the model.train cell in the notebook and instead upload the [latest .h5](https://drive.google.com/file/d/19oqKUd85FCipYzG2ev2K7PB4OMrAU0J1/view?usp=sharing) in the model.load cell.
```python
model = models.load_model("<latest h5 file>.h5")
```
 

## Dataset Creation

We have created our own [precompiled spectrogram dataset](https://drive.google.com/file/d/1CL6pn51hBdyqzJmRe89--YmcErdqEVXA/view?usp=sharing) consisting of 500 spectrograms of 10 genres, but if you choose to recreate this project yourself, you may follow these steps. We do not accept liability for your implementation of downloading music from youtube for this project. In order to comply with copyright claims on the songs, original audio files are deleted upon spectrogram creation in a later step, though it is advised for you to use a VPN while completing this step.

Using the CMD tool [youtube-dl](https://github.com/ytdl-org/youtube-dl):

```bash
pip install youtube-dl
```

Create a master folder in your directory with subfolders of the genre type you wish to use in this project. Open your terminal and navigate to the first genre folder. Find a playlist on youtube that you believe encapsulates that genre and copy the playlist link.

```bash
youtube-dl -x -i --audio-format “wav” <INSERT YOUTUBE PLAYLIST LINK>
```
This will take time, repeat for each genre/playlist. Some songs are not downloaded as wav for some reason, you may want to search the directories and remove such files.

Once you have all of the nested directories filled with wav files, create a similarly named nested directory to hold the spectrograms, then you may run 'Create 30 sec specs by genre.py' which will create spectrograms and delete the original audio files.

Inside of this python file are some global variables you should change first.
```python
#CHANGE ME
high_path = "Path-to-master-wav-folder"
save_path = "Path-to-master-spectrogram-folder"
num_seconds = 30
cut_upper_freq_range = True
```

We chose 30 seconds as our base length, you may find better results using a different length. We also cut out the upper-frequency range of the images, you may wish to leave this information in. It may also be necessary to look through the data set and remove images that you feel are inconsistent with the rest of the genre, some playlists include songs that are slightly out of the bounds of your desired set, and some songs include sections which are out of bounds as well. We chose to omit the first and last spectrogram of each song to eliminate intros and outros which may not be indicative of the overall genre.



## Usage
In order to train the model on your own spectrogram data, follow the above process for dataset creation. Afterwards, ensure that your main data folder is named "raw", and contains a list of folders named after your desired genres. Once this directory is placed in the same folder as the notebook, you can go through all of the cells in order to go from data ingestion to full prediction.



## Testing Individual Songs After VGG Implementation
We have included a stripped version of the spectrogram creator specific for filling one folder named 'test song imgs' with spectrograms from one song. This program takes in one CMD line argument which is the path to the wav file you would like to create spectrograms with. At the end of the Jupyter Notebook, this program is imported and called; to test your own audio files, the argument should be changed to reflect your file which resides in the same directory as the notebook.
```python
#Change both of these to your audio file
song_title = "Michael Jackson - Billie Jean.wav"
%run spec_creator "Michael Jackson - Billie Jean.wav"
```

Running the final cells will generate a series of images with the corresponding genre as titles and the most common genre as the master title of the output. Our model is not trained on Pop or Country music, so it is interesting to drop in songs of one of those classes.
 
** NOTE: The chord graph does not display in the jupyter notebook unless the kernel is running, but images can be found within our report **
