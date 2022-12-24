"""
@author: Handenur

Concatenate each interpolated surface
"""

import glob
import numpy as np
import os 
import cv2

subject_list = ['CSI1','CSI2','CSI3','CSI4']

directory = 'concat_file'
def load_data(subject_list):
    sess_dir = []
    result =[]
    paths = []
    txt = 0
    for subject in subject_list:
        parent_dir = glob.glob('F:/' + subject + '/*')
        for i in parent_dir:
            sess_dir.append(glob.glob(i + '/BOLD_Raw/*'))
            result = sum(sess_dir, [])
    for x in sess_dir:
        for y in x:
            path = os.path.join(y, directory)
            if os.path.exists(path):
                pass
            else:
                os.mkdir(path)
    while txt < (len(result)):
        if 'Run' in result[txt]:
            paths.append(os.path.join(result[txt], directory))
            result[txt] = result[txt] + '/interpolation/'
        elif 'SceneLocal' in result[txt]:
            paths.append(os.path.join(result[txt], directory))
            result[txt] = result[txt] + '/interpolation/'
        else:
            result[txt] = " "
        txt+=1
        filtered_file = list(filter(lambda r: r != " ", result))
    paths = sorted(paths)    
    for file in range(len(filtered_file)):
        if len(glob.glob(paths[file] + '/*')) == 194:
            pass
        elif 'SceneLocal' in paths[file] and len(glob.glob(paths[file] + '/*')) == 141:
            pass
        else:
            for f in os.listdir(paths[file]):
                os.remove(os.path.join(paths[file], f))
            npy = sorted(glob.glob(filtered_file[file] + "/*"))
            middle_idx = len(npy)//2
            lh_hem = npy[:middle_idx]
            rh_hem = npy[middle_idx:]        
            for idn in range(middle_idx):
                lh = np.load(lh_hem[idn], allow_pickle=True)
                rh = np.load(rh_hem[idn], allow_pickle=True)
                conc = cv2.hconcat([lh,rh])
                np.save(paths[file] + '/conc' + lh_hem[idn][-19:],conc, allow_pickle=True)
                print('File saved: ' + paths[file] ,'/conc' + lh_hem[idn][-19:])

          
load_data(subject_list)
            