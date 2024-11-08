"""
A File designed only to import things for all the project.
"""
import math, os, random, sys, time, requests, platform, subprocess
try:
    import pygame as pg
    from pygame.locals import *
except ModuleNotFoundError:
    print('PyGame not installed, installing...')
    os.system('python -m pip install pygame')
    print('Installed.')
    import pygame as pg
    from pygame.locals import *
import inspect
from datetime import datetime
from .excptions import *