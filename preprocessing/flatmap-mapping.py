"""
@author: Handenur

In this script, volume-to-surface mapping takes place for each subject. Then it's saved on the occipital flat patches.

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
            image_png = image_path2 + '/lh_' + sub[:-3] + 'png'
            png_dir = '/usr/local/freesurfer/subjects/lh_' + sub[:-3] + 'png'
            os.chdir(freesurfer_subject)
            os.system('mri_vol2surf --src ' + sub + ' --hemi lh ' + '--o lh.' + sub[:-3] + file_ex + ' --out_type paint --float2int round --regheader CSI1')
            brain = Brain('CSI1','lh','patch',figure=fig,background= 'black')
            overlay_file = freesurfer_subject + 'lh.' + sub[:-3] + file_ex
            brain.add_overlay(overlay_file,hemi='lh',sign='pos',min='actual_min',max='actual_max')
            brain._colorbar_visibility(False,0,0)
            mlab.savefig(freesurfer_subject + 'lh_' + sub[:-3] + 'png', figure = fig,magnification = 5)
            shutil.move(png_dir,image_png)

            image_png = image_path2 + '/rh_' + sub[:-3] + 'png'
            png_dir = '/usr/local/freesurfer/subjects/rh_' + sub[:-3] + 'png'
            os.system('mri_vol2surf --src ' + sub + ' --hemi rh ' + '--o rh.' + sub[:-3] + file_ex + ' --out_type paint --float2int round --regheader CSI1')
            brain = Brain('CSI1','rh','patch',figure=fig,background= 'black')
            overlay_file = freesurfer_subject + 'rh.' + sub[:-3] + file_ex
            brain.add_overlay(overlay_file,hemi='rh',sign='pos',min='actual_min',max='actual_max')
            brain._colorbar_visibility(False,0,0)
            mlab.savefig(freesurfer_subject + 'rh_' + sub[:-3] + 'png', figure = fig,magnification = 5)
            shutil.move(png_dir,image_png)
            
            os.remove(freesurfer_subject + 'lh.' + sub[:-3] + file_ex)
            os.remove(freesurfer_subject + 'rh.' + sub[:-3] + file_ex)
            os.remove(freesurfer_subject + sub)

            print(image_path)


