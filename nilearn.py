# -*- coding: utf-8 -*-
"""nilearn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CLxXkzZ5fAZycaWa6CLR61vkvogU8Q28
"""

import pandas as pd

# read_csv can read in just about any plain-text tabular data
data = pd.read_csv('abide2.tsv', sep='\t')
data.head()

data.info()

data.info

!pip install nilearn

from nilearn import datasets

development_dataset = datasets.fetch_development_fmri(n_subjects=30)

"""**nilearn** enables approachable and versatile analyses of brain volumes. It provides statistical and machine-learning tools, with instructive documentation & open community.
It supports general linear model (GLM) based analysis and leverages the scikit-learn Python toolbox for multivariate statistics with applications such as predictive modelling, classification, decoding, or connectivity analysis.
"""

development_dataset.description

"""The movie watching based brain development dataset (fMRI)\n\n\nNotes\n-----\nThis functional MRI dataset is used for teaching how to use\nmachine learning to predict age from naturalistic stimuli (movie)\nwatching with Nilearn.\n\nThe dataset consists of 50 children (ages 3-13) and 33 young adults (ages\n18-39). This dataset can be used to try to predict who are adults and\nwho are children.\n\nThe data is downsampled to 4mm resolution for convenience. The original\ndata is downloaded from OpenNeuro.\n\nFor full information about pre-processing steps on raw-fMRI data, have a look\nat README at https://osf.io/wjtyq/\n\nFull pre-processed data: https://osf.io/5hju4/files/\n\nRaw data can be accessed from : https://openneuro.org/datasets/ds000228/versions/1.0.0\n\nContent\n-------\n    :'func': functional MRI Nifti images (4D) per subject\n    :'confounds': TSV file contain nuisance information per subject\n    :'phenotypic': Phenotypic informaton for each subject such as age,\n                   age group, gender, handedness.\n\n\nReferences\n----------\nPlease cite this paper if you are using this dataset:\nRichardson, H., Lisandrelli, G., Riobueno-Naylor, A., & Saxe, R. (2018).\nDevelopment of the social brain from age three to twelve years.\nNature communications, 9(1), 1027.\nhttps://www.nature.com/articles/s41467-018-03399-2\n\nLicence: usage is unrestricted for non-commercial research purposes."""

development_dataset.phenotypic

development_dataset.confounds

"""The process of removing motion-based artifacts from our data is called confound regression, which is essentially fitting a linear model using motion estimates as regressors then subtracting it out from the signal. Hopefully in this process we get a closer estimate of what the actual brain-induced BOLD signal looks like.

**Preprocess** usually involve: Motion correction; Normalization; Smoothing

**nibabel**: Read / write access to some common neuroimaging file formats
"""

import nibabel as nib

img = nib.load(development_dataset.func[0])
img.shape

img.instance_to_filename

img.files_types

import matplotlib.pyplot as plt
from nilearn import image
from nilearn import plotting

mean_image = image.mean_img(development_dataset.func[0])
plotting.view_img(mean_image, threshold=None)

"""####Extracting signal from fMRI volumes

MSDL(multi-subject dictionary learning): a probabilistic ROIs across the brain
"""

import numpy as np

msdl_atlas = datasets.fetch_atlas_msdl()

msdl_coords = msdl_atlas.region_coords
n_regions = len(msdl_coords)

print(f'MSDL has {n_regions} ROIs, parts of the following networks : \n{np.unique(msdl_atlas.networks)}.')

plotting.plot_prob_atlas(msdl_atlas.maps)

"""surface atlas vs volumetric atlas

How much, and Where questions
"""

from nilearn import input_data

masker = input_data.NiftiMapsMasker(msdl_atlas.maps, resampling_target="data", t_r=2, detrend=True, low_pass=0.1, high_pass=0.01).fit()

"""###Feature Selection and weights"""

roi_time_series = masker.transform(development_dataset.func[0])
roi_time_series.shape

"""weights: 168 recordings, 39 roi, but it transposed

Brain Synchrony: Connectome
"""

from nilearn.connectome import ConnectivityMeasure

correlation_measure = ConnectivityMeasure(kind='correlation')
correlation_matrix = correlation_measure.fit_transform([roi_time_series])[0]

np.fill_diagonal(correlation_matrix, 0)
plotting.plot_matrix(correlation_matrix, labels=msdl_atlas.labels,
                     vmax=0.8, vmin=-0.8, colorbar=True)

plotting.view_connectome(correlation_matrix, edge_threshold=0.2,
                         node_coords=msdl_atlas.region_coords)

"""###Noise sources"""

pd.read_table(development_dataset.confounds[0]).head()

corrected_roi_time_series = masker.transform(
    development_dataset.func[0], confounds=development_dataset.confounds[0])
corrected_correlation_matrix = correlation_measure.fit_transform(
    [corrected_roi_time_series])[0]
np.fill_diagonal(corrected_correlation_matrix, 0)
plotting.plot_matrix(corrected_correlation_matrix, labels=msdl_atlas.labels,
                     vmax=0.8, vmin=-0.8, colorbar=True)

plotting.view_connectome(corrected_correlation_matrix, edge_threshold=0.2,
                         node_coords=msdl_atlas.region_coords)