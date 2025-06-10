import pandas as pd
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm

import numpy as np
from scipy.spatial.distance import cdist
from scipy.spatial.distance import euclidean
from itertools import permutations
from sklearn.cluster import KMeans

from k_means_constrained import KMeansConstrained

import requests
import heapq
import csv
import os

from sklearn.cluster import KMeans

from codecarbon import EmissionsTracker
import time

ox.settings.use_cache = True
ox.settings.log_console = True