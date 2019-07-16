#!/usr/bin/env python

import numpy as np
import itk
import simplebrainviewer as sbv
import nibabel as nib

T = lambda x: np.array([
    [1,0,0,0],
    [0,np.cos(np.pi*x/180),-np.sin(np.pi*x/180),0],
    [0,np.sin(np.pi*x/180),np.cos(np.pi*x/180),0],
    [0,0,0,1]
])

ImageType = itk.Image[itk.F,3]

angle=45
A = T(angle)[:3,:3]
b = T(angle)[:3,3]
gamma = np.concatenate((A.ravel(),b))

reader = itk.ImageFileReader[ImageType].New()
reader.SetFileName('MNI152.nii.gz')
reader.Update()
input_img = reader.GetOutput()

size = input_img.GetLargestPossibleRegion().GetSize()

resample = itk.ResampleImageFilter[ImageType,ImageType].New()
resample.SetInput(input_img)
resample.SetReferenceImage(input_img)
resample.UseReferenceImageOn()
resample.SetSize(size)
resample.SetDefaultPixelValue(0.0)
interpolator = itk.WindowedSincInterpolateImageFunction[ImageType,3,itk.HammingWindowFunction[3]].New()
resample.SetInterpolator(interpolator)

transform = itk.AffineTransform[itk.D,3].New()
transform.SetParameters(itk.OptimizerParameters[itk.D](gamma))

resample.SetTransform(transform)

output_img = resample.GetOutput()
np_input_img = itk.GetArrayViewFromImage(input_img).T
np_output_img = itk.GetArrayViewFromImage(output_img).T
sbv.plot_brain(np_output_img)

