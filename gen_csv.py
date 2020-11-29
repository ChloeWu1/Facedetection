import glob
import os.path
from subprocess import call
import subprocess
import csv
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
def get_video_parts(video_path):
    """Given a full path to a video, return its parts."""
    parts = video_path.split(os.path.sep)
    filename = parts[1]
    filename_no_ext = filename.split('.')[0]
    train_or_test = parts[0]

    return train_or_test, filename_no_ext, filename

data_global=[]
folders = ['test', 'train']
for folder in folders:

    files = [f for f in listdir(folder) if not isfile(join(folder, f))]
    count = 0
    max=0
    for video_path in files:
        video_path = os.path.join(folder,video_path)
        count_frame=0
        data_file = []
        percentage = (count*100)/len(files)
        print(folder+")"+str(percentage)+"% "+str(count)+" of "+str(len(files)))
        
        video_parts = get_video_parts(video_path)
        train_or_test, filename_no_ext, filename = video_parts

        file_arousal = os.path.join('annotations','arousal', filename_no_ext+'_arousal.txt')
        lines_arousal = [line.rstrip('\n') for line in open(file_arousal)]

        file_valence = os.path.join('annotations','valence', filename_no_ext+'_valence.txt')
        lines_valence = [line.rstrip('\n') for line in open(file_valence)]
        n_frames = len(lines_arousal)

        dst_folder = os.path.join(train_or_test, filename_no_ext)

        for n in range(n_frames):
            aro = str(lines_arousal[n])
            val = str(lines_valence[n])
            dest = os.path.join(train_or_test, filename_no_ext, filename_no_ext + '-'+str(n)+'.jpg')
            if os.path.isfile(dest):
                data_file.append([n,  1])
                count_frame=count_frame+1
            else:
                data_file.append([n,  0])

        data_global.append([train_or_test, filename_no_ext, n_frames,  count_frame])
        print(filename_no_ext)
        if count_frame>=max:
            max=count_frame
        csvfile = os.path.join('csv', filename_no_ext + '.csv')
        with open(csvfile, 'w') as fout:
            writer = csv.writer(fout)
            writer.writerows(data_file)

        
        count = count +1


    print("MAX frame:"+str(max))
csvfile = os.path.join('csv', 'global.csv')
with open(csvfile, 'w') as fout:
    writer = csv.writer(fout)
    writer.writerows(data_global)