"""
A File designed only to import things for all the project.
"""
import math, os, random,json , sys, time, platform, subprocess, inspect, threading, colorsys
import urllib.request
from typing import Literal
try:
    import pygame as pg
    from pygame.locals import *
    from pygame import joystick as pg_joystick
except ModuleNotFoundError:
    print('PyGame not installed, installing...')
    os.system('python -m pip install pygame')
    print('Installed.')
    import pygame as pg
    from pygame.locals import *
import inspect
from datetime import datetime, timedelta
from .excptions import *

# try:
#     import requests
# except ModuleNotFoundError:
#     print('Requests not installed, installing...')
#     os.system('python -m pip install requests')
#     print('Installed.')