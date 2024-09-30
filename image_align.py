import matplotlib 
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import Button
import pandas as pd
import os
import tkinter as tk
import glob

matplotlib.use('Qt5Agg')

class ImageAlign():

    def __init__(self, working_dir, image_ext = '.png'):

        self.working_dir = working_dir
        self.image_ext = image_ext
        self.df_images = self.get_image_status()


    def __str__(self):
        #[print(f'{x} : {getattr(self, x)}') for x in dir(self) if not str.startswith(x, '__')]
        print('\n\n____________________________________________________________')
        for key, value in self.__dict__.items():
            if type(value) == pd.DataFrame:
                print(f' * {key} :\n{value}\n')
            else:
                print(f' * {key} : {value}')
        print('____________________________________________________________')
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
    

    def initialize_plot(self):
        
        fig = matplotlib.pyplot.figure() 
        ax_image = fig.add_subplot()
        ax_image.set_xlabel('[left click] to add point, [right click] to remove point')
        
        self.fig = fig
        self.ax_image = ax_image
        fig.canvas.draw()

        return self
    def plot_points(self):
        hpoints = self.ax_image.plot(self.df_xy['x'], self.df_xy['y'],  marker = 'o', markersize = 20, c = 'r', fillstyle = 'none', linestyle = '--')
        self.hpoints = hpoints

    def plot_image(self, idx):

        fullpath = self.df_images.loc[idx, 'fullpath']
        csv_fn = f'{fullpath}.csv'
        img = cv2.imread(fullpath)

        self.fig.suptitle(fullpath)

        if os.path.isfile(csv_fn):
            df_xy = pd.read_csv(csv_fn, header = 0, index_col = 0)
        else:
            df_xy = pd.DataFrame(columns = ['x', 'y', 'user', 'datetime', 'filename'])

        self.df_xy = df_xy
        self.ax_image.imshow(img)
        self.plot_points()
        self.update_message(fullpath)
        #print(f'loaded {file}')

        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        self.fig.canvas.draw()


    def update_message(self, msg):
        print(msg)
        self.ax_image.set_title(msg)


    def onclick(self, event):

        print(event)
        ix, iy = event.xdata, event.ydata

        if event.inaxes != self.ax_image:
            return None

        if (ix ==None) or (iy ==None):
            return None

        if event.button ==1: # left click, add point
            ix = int(ix)
            iy = int(iy)

            msg = f'add point: x = {ix}, y = {iy}'
            self.update_message(msg)

            self.df_xy = self.df_xy._append( {'x':ix, 'y':iy} , ignore_index=True)

        if event.button ==3 and len(self.df_xy)>0: # right click, remove point
            d = (ix-self.df_xy['x'])**2 + (iy-self.df_xy['y'])**2
            idx = d.idxmin()
            self.df_xy = self.df_xy.drop(idx)
            msg = f'remove point: index = {idx}'
            self.update_message(msg)

        # sort points and redraw
        self.df_xy=self.df_xy.sort_values('x').reset_index(drop = True)
        try:
            self.hpoints.pop(0).remove()
        except:
            pass
        self.plot_points()
        print(self.df_xy)
        self.fig.canvas.draw()
        return self



session = ImageAlign(r'.\images', r'.png')

session.initialize_plot()
session.plot_image(0)
print(session)
plt.show()