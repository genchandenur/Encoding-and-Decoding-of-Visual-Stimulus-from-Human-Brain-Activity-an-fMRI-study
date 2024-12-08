"""
@author: Handenur

Concatenate each interpolated surface
"""

import glob
import numpy as np
import os
import cv2

BASE = input("Enter the base path (e.g., F:/): ")
SUBJECT_LIST = input("Enter the subject list (comma-separated, e.g., CSI1,CSI2,CSI3,CSI4): ").split(',')
DIRECTORY = input("Enter the name of the directory for concatenated files (e.g., concat_file): ")
CONCAT = input("Enter concatenation type ('h' for horizontal, 'v' for vertical, 'c' for channel): ")

def load_data(SUBJECT_LIST, DIRECTORY, CONCAT):
    sess_dir = [] 
    result = []    
    paths = []     

    for subject in SUBJECT_LIST:
        parent_dir = glob.glob(os.path.join(BASE, subject, '*'))
        #parent_dir = glob.glob(f'F:/{subject}/*')
        for i in parent_dir:
            sess_dir.extend(glob.glob(os.path.join(i, 'BOLD_Raw', '*')))
            result = sum(sess_dir, [])  

    for x in sess_dir:
        for y in x:
            path = os.path.join(y, DIRECTORY)
            os.makedirs(path, exist_ok=True)

    for path in result:
        if 'Run' in path or 'SceneLocal' in path:
            paths.append(os.path.join(path, DIRECTORY))
            path = os.path.join(path, 'interpolation')
        else:
            continue

    filtered_file = list(filter(lambda r: 'interpolation' in r, result))
    paths = sorted(paths)

    for file_idx, filtered_path in enumerate(filtered_file):
        target_path = paths[file_idx]
        if ('SceneLocal' in target_path and len(glob.glob(f"{target_path}/*")) == 141) or \
           (len(glob.glob(f"{target_path}/*")) == 194):
            continue

        for f in os.listdir(target_path):
            os.remove(os.path.join(target_path, f))

        npy_files = sorted(glob.glob(f"{filtered_path}/*"))
        middle_idx = len(npy_files) // 2
        lh_hem = npy_files[:middle_idx] 
        rh_hem = npy_files[middle_idx:]

        for idx in range(middle_idx):
            lh = np.load(lh_hem[idx], allow_pickle=True)
            rh = np.load(rh_hem[idx], allow_pickle=True)

            if lh.shape[0] != rh.shape[0]:
                print(f"Shape mismatch for files {lh_hem[idx]} and {rh_hem[idx]}")
                continue

            if CONCAT == 'h':
                conc = cv2.hconcat([lh, rh])
            elif CONCAT == 'v':
                conc = cv2.vconcat([lh, rh])
            elif CONCAT == 'c':
                conc = np.stack((lh, rh), axis=-1)
            else:
                raise ValueError("Invalid concatenation type. Use 'h', 'v', or 'c'.")            save_path = os.path.join(target_path, f"conc_{os.path.basename(lh_hem[idx])}")
            np.save(save_path, conc, allow_pickle=True)
            print(f"File saved: {save_path}")

load_data(subject_list)
