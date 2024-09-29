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

    def __str__(self):
        [print(f'{x} : {getattr(self, x)}') for x in dir(self) if not str.startswith(x, '__')]
        return ''


session = ImageAlign('.', '.png')
print(session)