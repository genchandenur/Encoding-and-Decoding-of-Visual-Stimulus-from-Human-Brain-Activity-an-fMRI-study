"""
@author: Handenur

Convert DICOM Mosaics to Nifti 3D with FreeSurfer Integration
"""

import os
import glob
import shutil

PARENT_DIR = input("Enter the parent directory path: ")
DIRECTORY = input("Enter the name of the target folder to be created: ")
FREESURFER_SUBJECTS = input("Enter the FreeSurfer subjects directory (/usr/local/freesurfer/subjects/): ")
SUB_PATH = input("Enter the sub path: (BOLD_Raw)")
sess_dir = []

PARENT_DIRS = glob.glob(os.path.join(PARENT_DIR, '*'))
for i in PARENT_DIRS:
    if os.path.exists(os.path.join(i, SUB_PATH)):
        sess_dir.extend(glob.glob(os.path.join(i, SUB_PATH, "*")))
    else:
        sess_dir.extend(glob.glob(os.path.join(i, "*")))

for session in sess_dir:
    target_dir = os.path.join(session, DIRECTORY)
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    os.mkdir(target_dir)

    subjects = os.listdir(session)
    for subject in subjects:
        image_path = os.path.join(session, subject)
        subject_dir = os.path.join(FREESURFER_SUBJECTS, subject)
        subject_nii = os.path.join(FREESURFER_SUBJECTS, f"{subject[:-4]}.nii")

        shutil.copy2(image_path, subject_dir)

        os.chdir(FREESURFER_SUBJECTS)
        os.system(f"mri_convert {subject} {subject[:-4]}.nii")

        os.remove(subject_dir)

        shutil.move(subject_nii, os.path.join(target_dir, f"{subject[:-4]}.nii"))


           
            
# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI1/surf$ mris_flatten -w 0 lh.occip.patch.mgh lh.occip.flat.mgh
# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI1/surf$ mris_flatten -w 0 rh.occip.patch.mgh rh.occip.flat.mgh

# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI2/surf$ mris_flatten -w 0 lh.occip.patch.mgh lh.occip.flat.mgh
# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI2/surf$ mris_flatten -w 0 rh.occip.patch.mgh rh.occip.flat.mgh

# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI3/surf$ mris_flatten -w 0 lh.occip.patch.mgh lh.occip.flat.mgh
# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI3/surf$ mris_flatten -w 0 rh.occip.patch.mgh rh.occip.flat.mgh

# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI4/surf$ mris_flatten -w 0 lh.occip.patch.mgh lh.occip.flat.mgh
# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI4/surf$ mris_flatten -w 0 rh.occip.patch.mgh rh.occip.flat.mgh

