"""
@author: Handenur

Volume to Surface Registration
"""

#import pydicom as dicom
#import matplotlib.pylab as plt
import numpy as np
import math
import os
import glob
import nibabel as nib
import shutil
from surfer import Brain
from mayavi import mlab 
mlab.init_notebook(backend='png')

print(__doc__)
fig = mlab.figure(size=(1000,550))

directory = 'dcm2nifti'
reg_file = 'registration'
sess_dir=list()
subjects=list()
parent_dir = glob.glob('/media/handenur/Seagate Expansion Drive1/CSI1/*')
for i in parent_dir:
    if os.path.exists(i + '/BOLD_Raw'):
        sess_dir.append(glob.glob(i + '/BOLD_Raw/*'))
    else:
        sess_dir.append(glob.glob(i + '/*'))
for s in sess_dir:
    for k in s:
        path = os.path.join(k, reg_file)
        if os.path.exists(path):
        	pass
        else:
            os.mkdir(path)
            vol_dir=(k+'/'+directory)
            subjects = os.listdir(vol_dir)
            for sub in subjects:
                image_path = vol_dir + '/' + sub                
                subjectnm = image_path[55:59]
                file_ex = 'mgh'
                image_path2 = vol_dir + '/'
                freesurfer_subject = '/usr/local/freesurfer/subjects/'
                subject_dir = '/usr/local/freesurfer/subjects/' + sub[:-3]
                shutil.copy2(image_path,freesurfer_subject + sub)

                os.chdir(freesurfer_subject)
                os.system('mri_vol2surf --src ' + sub + ' --hemi lh ' + '--o lh.' + sub[:-3] + file_ex + ' --out_type paint --float2int round --regheader CSI1')

    
                os.chdir(freesurfer_subject)
                os.system('mri_vol2surf --src ' + sub + ' --hemi rh ' + '--o rh.' + sub[:-3] + file_ex + ' --out_type paint --float2int round --regheader CSI1')

    		    
                shutil.move(freesurfer_subject + 'lh.' + sub[:-3] + file_ex,path + '/lh.' + sub[:-3] + file_ex)
                shutil.move(freesurfer_subject + 'rh.' + sub[:-3] + file_ex,path + '/rh.' + sub[:-3] + file_ex)
                os.remove(freesurfer_subject + sub)
                
                print(image_path)
