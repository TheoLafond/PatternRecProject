# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:21:56 2023

@author: Théo
"""

from os import listdir
from os.path import isfile, join

same_melodys = [f for f in listdir("./data/train/voyage") if isfile(join("./data/train/voyage/", f))]