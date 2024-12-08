"""
@author: Handenur

Volume to Surface Registration
CSI1 - A subject directory in the SUBJECT_NAME path. Edit the filename to try different subjects.
"""

#import pydicom as dicom
#import matplotlib.pylab as plt
import os
import glob
import shutil
from surfer import Brain
from mayavi import mlab

mlab.init_notebook(backend='png')

PARENT_DIR = input("Please enter the path to the parent directory (e.g., /media/handenur/Seagate Expansion Drive1/CSI1/): ").strip()
FREESURFER_SUBJECTS = input("Please enter the path to the FreeSurfer 'subjects' directory (e.g., /usr/local/freesurfer/subjects/): ").strip()
DIRECTORY = input("Please enter the name of the subdirectory containing the files to be processed (e.g., dcm2nifti): ").strip()
REG_FILE = input("Please enter the name of the registration directory (e.g., registration): ").strip()
SUBJECT_NAME = input("Please enter the subject name (e.g., CSI1): ")

fig = mlab.figure(size=(1000, 550))

sess_dirs = []
parent_dirs = glob.glob(os.path.join(PARENT_DIR, '*'))
for parent in parent_dirs:
    bold_dir = os.path.join(parent, 'BOLD_Raw')
    if os.path.exists(bold_dir):
        sess_dirs.extend(glob.glob(os.path.join(bold_dir, '*')))
    else:
        sess_dirs.extend(glob.glob(os.path.join(parent, '*')))

for session in sess_dirs:
    reg_path = os.path.join(session, REG_FILE)
    if not os.path.exists(reg_path):
        os.mkdir(reg_path)
        vol_dir = os.path.join(session, DIRECTORY)
        subjects = os.listdir(vol_dir)
        
        for subject_file in subjects:
            src_path = os.path.join(vol_dir, subject_file)
            dest_path = os.path.join(FREESURFER_SUBJECTS, subject_file)
            subject_name = subject_file[:-3] 
            
            shutil.copy2(src_path, dest_path)

            for hemi in ['lh', 'rh']:
                output_file = f'{hemi}.{subject_name}mgh'
                cmd = (
                    f"mri_vol2surf --src {subject} --hemi {hemi} "
                    f"--o {hemi}.{subject_name}.mgh --out_type paint "
                    f"--float2int round --regheader {SUBJECT_NAME}"
                )
                print(f"Running command: {cmd}")
                os.chdir(FREESURFER_SUBJECTS)
                os.system(cmd)

                shutil.move(
                    os.path.join(FREESURFER_SUBJECTS, output_file),
                    os.path.join(reg_path, output_file)
                )
            
            os.remove(dest_path)
            print(f'processed: {src_path}')

