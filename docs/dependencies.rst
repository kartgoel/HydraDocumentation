Dependencies
===================

Standard Libaries
--------------------

.. code-block:: python

    import argparse
    import ast
    import base64
    import ctypes
    import cv2
    import json
    import logging
    import math
    import matplotlib.cm as cm
    import MySQLdb
    import numpy as np
    import os
    import pandas as pd
    import platform
    import random
    import sys
    import tensorflow as tf
    import time
    import zmq
    

Sub Libraries
---------------------

.. code-block:: python

    from datetime import datetime
    from multiprocessing import Process, Value, Array
    from sklearn.metrics import classification_report
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelBinarizer
    from sklearn.utils import shuffle
    from shutil import move
    from tensorflow import keras
    from tensorflow.keras.applications.inception_v3 import InceptionV3
    from tensorflow.keras.callbacks import EarlyStopping
    from tensorflow.keras.models import load_model
    from tensorflow.keras.optimizers import SGD, Adadelta
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras import backend as K 
    from xml.etree.ElementTree import Element
    from xml.etree.ElementTree import tostring
    


Non-Standard Libraries
---------------------

.. code-block:: python

    import utils.ConnectToDB as connector

    from Entities.Model import Model
    from Entities.Plots import Plots
    