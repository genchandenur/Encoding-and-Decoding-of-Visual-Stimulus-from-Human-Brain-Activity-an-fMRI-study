"""
@author: Handenur


In this script, volume-to-surface mapping takes place for each subject. Then it's saved on the occipital flat patches as npy file.
CSI1 - A subject directory in the SUBJECT_DIR path. Edit the filename to try different subjects.

"""

import numpy as np
import math
import os
import glob
import nibabel as nib
import shutil
from surfer import Brain
from mayavi import mlab 
from surfer import io
from scipy.interpolate import LinearNDInterpolator
import numpy as np
import matplotlib.pyplot as plt
from numpy import save ,load


data_dir = 'interpolation'
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
        path = os.path.join(k, data_dir)
        if os.path.exists(path):
        	pass
        else:
            os.mkdir(path)
            vol_dir=(k+'/'+reg_file)
            subjects = os.listdir(vol_dir)
            for sub in subjects:
                image_path = vol_dir + '/' + sub            
                subjectnm = image_path[55:59]
                file_ex = 'npy'
                image_path2 = vol_dir + '/'
                freesurfer_subject = '/usr/local/freesurfer/subjects/'
                subject_dir = '/usr/local/freesurfer/subjects/' + sub[:-3]
                overlay_file = freesurfer_subject + sub
                shutil.copy2(image_path,overlay_file)

                os.chdir(freesurfer_subject)
                if sub[0:2] == 'lh':
                    #os.system('mri_vol2surf --src ' + sub + ' --hemi lh ' + '--o lh.' + sub[:-3] + file_ex + ' --out_type paint --float2int round --regheader CSI1')
                    fig = mlab.figure(size=(1000,550))
                    brain = Brain("CSI1", "lh", "patch",figure=fig,background='black',cortex='Greys')
    
                    sig1 = io.read_scalar_data(overlay_file)
                    #brain.add_overlay(sig1,hemi='lh',sign="pos",min='actual_min',max='actual_max')
                    im = brain.add_data(sig1,min=0,max=1500,colorbar=True,colormap='Spectral',smoothing_steps='nearest',alpha=1,transparent=False)
                    brain._colorbar_visibility(False,0,0) 
                    values = brain.data['array']
                    t = brain.brain_matrix[0,0]
                    mesh = t.data[0]['mesh']
                    mdata = mesh.get_output_dataset()
                    polys = mdata.polys.to_array()
                    points = mdata.points.to_array()
                    # convex hull                
                    X = np.linspace(min(points[:,0]),max(points[:,0]),num=500)
                    Y = np.linspace(min(points[:,1]),max(points[:,1]),num=500)
                    X,Y = np.meshgrid(X,Y)
                    fig = LinearNDInterpolator(points[:,0:2],values,fill_value=0)
                    mesh = fig(X,Y)
                    save(sub[:-3] + file_ex, mesh)
                    mlab.close()
                else:
                    fig = mlab.figure(size=(1000,550))
                    brain = Brain("CSI1", "rh", "patch",figure=fig,background='black',cortex='Greys')
    
                    sig1 = io.read_scalar_data(overlay_file)
                    im = brain.add_data(sig1,min=0,max=1500,colorbar=True,colormap='Spectral',smoothing_steps='nearest',alpha=1,transparent=False)
                    brain._colorbar_visibility(False,0,0) 
                    values = brain.data['array']
                    t = brain.brain_matrix[0,0]
                    mesh = t.data[0]['mesh']
                    mdata = mesh.get_output_dataset()
                    polys = mdata.polys.to_array()
                    points = mdata.points.to_array()
                    # convex hull                
                    X = np.linspace(min(points[:,0]),max(points[:,0]),num=500)
                    Y = np.linspace(min(points[:,1]),max(points[:,1]),num=500)
                    X,Y = np.meshgrid(X,Y)
                    fig = LinearNDInterpolator(points[:,0:2],values,fill_value=0)
                    mesh = fig(X,Y)

                    save(sub[:-3] + file_ex, mesh)
                    mlab.close()

                
                shutil.move(freesurfer_subject + sub[:-3] + file_ex,path + '/' + sub[:-3] + file_ex)
                os.remove(freesurfer_subject + sub)
                
                print(image_path)

            
