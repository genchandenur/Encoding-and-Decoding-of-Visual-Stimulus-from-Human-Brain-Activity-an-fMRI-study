"""

@author: Handenur

Dicom Mosaics to Nifti 3D
"""

import pydicom as dicom
#import matplotlib.pylab as plt
import numpy as np
import math
import os
import glob
import nibabel as nib
import shutil

directory = "dcm2nifti"
sess_dir=list()
parent_dir = glob.glob('/media/handenur/Seagate Expansion Drive/bold-unzip/*')
for i in parent_dir:
    if os.path.exists(i + "/BOLD_Raw"):
        sess_dir.append(glob.glob(i + "/BOLD_Raw/*"))
    else:
        sess_dir.append(glob.glob(i + "/*"))
subjects=list()
for s in sess_dir:
    for k in s:
        if os.path.exists(k+"/"+directory):
            shutil.rmtree(k + "/" + directory)
        subjects = os.listdir(k)
        path = os.path.join(k, directory)
        os.mkdir(path)
        for sub in subjects:
            image_path = k + "/" + sub
            image_path2 = k + "/"
            freesurfer_subject = "/usr/local/freesurfer/subjects/"
            subject_dir = "/usr/local/freesurfer/subjects/" + sub
            sub2 = sub[:-4]+".nii"
            subject_nii = "/usr/local/freesurfer/subjects/" + sub2
            shutil.copy2(image_path,subject_dir)
            os.chdir(freesurfer_subject)
      	    #os.popen("mri_convert"+" "+sub+" "+sub2)
            os.system("mri_convert"+" "+sub+" "+sub2)
            os.remove(subject_dir)
            shutil.move(subject_nii,path+"/"+sub2)
            
            

           
            
# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI1/surf$ mris_flatten -w 0 lh.occip.patch.mgh lh.occip.flat.mgh
# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI1/surf$ mris_flatten -w 0 rh.occip.patch.mgh rh.occip.flat.mgh

# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI2/surf$ mris_flatten -w 0 lh.occip.patch.mgh lh.occip.flat.mgh
# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI2/surf$ mris_flatten -w 0 rh.occip.patch.mgh rh.occip.flat.mgh

# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI3/surf$ mris_flatten -w 0 lh.occip.patch.mgh lh.occip.flat.mgh
# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI3/surf$ mris_flatten -w 0 rh.occip.patch.mgh rh.occip.flat.mgh

# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI4/surf$ mris_flatten -w 0 lh.occip.patch.mgh lh.occip.flat.mgh
# handenur@handenur-VirtualBox:/usr/local/freesurfer/subjects/CSI4/surf$ mris_flatten -w 0 rh.occip.patch.mgh rh.occip.flat.mgh




