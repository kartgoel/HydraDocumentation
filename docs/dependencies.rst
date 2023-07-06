Dependencies
===================

Standard Libaries
--------------------

.. code-block:: python

    import argparse
    import ast
    import atexit
    import base64
    import ctypes
    import cv2
    import getpass
    import json
    import logging
    import math
    import matplotlib.cm as cm
    import matplotlib.pyplot as plt
    import MySQLdb
    import numpy as np
    import os
    import pandas as pd
    import pickle
    import platform
    import random
    import select
    import subprocess 
    import sys
    import tensorflow as tf
    import time
    import warnings 
    import zmq
    

Sub Libraries
---------------------

.. code-block:: python

    from datetime import datetime

    from multiprocessing import Process, Value, Array

    from shutil import copyfile
    from shutil import move

    from sklearn.metrics import classification_report
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelBinarizer
    from sklearn.utils import shuffle

    from tensorflow import keras
    from tensorflow.keras import backend as K
    from tensorflow.keras.applications.inception_v3 import InceptionV3
    from tensorflow.keras.callbacks import EarlyStopping
    from tensorflow.keras.models import load_model
    from tensorflow.keras.optimizers import SGD, Adadelta
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import BatchNormalization, Conv2D, MaxPooling2D, Activation, Flatten, Dropout, Dense, Input
    from tensorflow.keras.optimizers import SGD, Adadelta
    from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint

    from xml.etree.ElementTree import Element
    from xml.etree.ElementTree import tostring

Non-Standard Libraries
---------------------

.. code-block:: python

    import utils.ConnectToDB as connector
    import utils.Helpers as helpers

    from Entities.Model import Model
    from Entities.Plots import Plots

    from inference_engine import InferenceEngine

    from multiprocessing import Process

    from gradcam import GradCAM
    
    from utils import ConnectToDB
    from utils.AIReport import AIReport
    from utils.ConnectToDB import DBManager
    from utils.DataPreprocessing import DataPreparation
    from utils.Helpers import printVersions
    
    
    