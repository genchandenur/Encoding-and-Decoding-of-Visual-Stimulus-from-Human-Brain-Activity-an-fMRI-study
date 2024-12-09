"""
@author: Handenur

In this script, volume-to-surface mapping takes place for each subject. Then it's saved on the occipital flat patches as npy file.
CSI1 - A subject directory in the SUBJECT_DIR path. Edit the filename to try different subjects.

"""
import os
import glob
import shutil
import numpy as np
from surfer import Brain
from mayavi import mlab
from surfer import io
from scipy.interpolate import LinearNDInterpolator
from numpy import save

PARENT_DIR = input("Enter the parent directory path (e.g., /media/handenur/Seagate Expansion Drive1/CSI1/): ").strip()
FREESURFER_SUBJECTS = input("Enter the FreeSurfer 'subjects' directory path (e.g., /usr/local/freesurfer/subjects/): ").strip()
DATA_DIR = input("Enter the name of the output data directory (e.g., interpolation): ").strip()
REG_FILE = input("Enter the name of the registration directory (e.g., registration): ").strip()
SUBJECT_NAME = input("Enter the CSI1 subject name (e.g., CSI1): ").strip()
FILE_EXTENSION = input("Enter the extension you want to save with dot: (e.g. npy").strip() 
sess_dirs = []
parent_dirs = glob.glob(os.path.join(PARENT_DIR, "*"))
for parent in parent_dirs:
    bold_path = os.path.join(parent, "BOLD_Raw")
    sess_dirs.extend(glob.glob(os.path.join(bold_path, "*") if os.path.exists(bold_path) else os.path.join(parent, "*")))

def process_hemisphere(hemi, overlay_file, output_file, subject_name):
    print(f"Processing {hemi} hemisphere for subject: {subject_name}")

    fig = mlab.figure(size=(1000, 550))
    brain = Brain(SUBJECT_NAME, hemi, "patch", figure=fig, background="black", cortex="Greys")

    sig1 = io.read_scalar_data(overlay_file)
    brain.add_data(sig1, min=0, max=1500, colorbar=True, colormap="Spectral", smoothing_steps="nearest", alpha=1, transparent=False)
    brain._colorbar_visibility(False, 0, 0)

    values = brain.data["array"]
    t = brain.brain_matrix[0, 0]
    mesh = t.data[0]["mesh"]
    mdata = mesh.get_output_dataset()
    points = mdata.points.to_array()

    X = np.linspace(points[:, 0].min(), points[:, 0].max(), num=500)
    Y = np.linspace(points[:, 1].min(), points[:, 1].max(), num=500)
    X, Y = np.meshgrid(X, Y)
    interpolator = LinearNDInterpolator(points[:, :2], values, fill_value=0)
    interpolated_mesh = interpolator(X, Y)

    save(output_file, interpolated_mesh)
    mlab.close()
    print(f"Saved mesh to: {output_file}")

for session in sess_dirs:
    output_path = os.path.join(session, DATA_DIR)
    os.makedirs(output_path, exist_ok=True)

    vol_dir = os.path.join(session, REG_FILE)
    subjects = os.listdir(vol_dir)
    for subject in subjects:
        image_path = os.path.join(vol_dir, subject)
        subject_name, _ = os.path.splitext(subject)
        overlay_file = os.path.join(FREESURFER_SUBJECTS, subject)
        output_file = os.path.join(output_path, f"{subject_name}.{FILE_EXTENSION}")

        shutil.copy2(image_path, overlay_file)

        hemi = "lh" if subject.startswith("lh") else "rh"
        process_hemisphere(hemi, overlay_file, output_file, subject_name)

        os.remove(overlay_file)
        print(f"Processed and cleaned up: {image_path}")

