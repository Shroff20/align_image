import matplotlib 
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import Button
import pandas as pd
import os
import tkinter as tk
import glob

class ImageAlign():

    def __init__(self, working_dir, image_ext = '.png'):

        self.working_dir = working_dir
        self.image_ext = image_ext
        self.df_images = self.get_image_status()

    def __str__(self):
        [print(f'{x} : {getattr(self, x)}') for x in dir(self) if not str.startswith(x, '__')]
        return ''
    
        
    def get_image_status(self):

        image_dir = self.working_dir
        image_ext = self.image_ext

        image_glob = os.path.join(image_dir, f'*{image_ext}')
        images = glob.glob(image_glob, recursive=True)
        print(f'{len(images)} {image_ext} images found')

        csv_glob = os.path.join(image_dir, f'*.csv')
        csvs = glob.glob(csv_glob, recursive=True)
        print(f'{len(csvs)} annotation .csv files found')

        def process_images(fullpath):
            basename = os.path.basename(fullpath)
            has_annotations =  os.path.isfile(f'{fullpath}.csv')
            d = {'fullpath':fullpath, 'basename': basename, 'has_annotations': has_annotations}
            return d

        d = [process_images(x) for x in images]
        df_images = pd.DataFrame(d)

        return df_images


session = ImageAlign('.\images', '.png')
print(session)