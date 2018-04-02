import collections
import pprint
from django.http import HttpResponse
from django.utils.encoding import smart_str
import django_tqdm
import os
import requests
from bson.objectid import ObjectId
from rest_framework import filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import ViewSet
import pandas as pd
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.stem.snowball import EnglishStemmer
import time
import networkx as nx
from networkx.readwrite import json_graph
from .serializers import *
from collections import *
from sklearn.externals import joblib
from pymongo import MongoClient

from scipy import stats

DATESTARTH2020 = 1388534400
DATEENDH2020 = 1577836800


def outliers_iqr(df, row):
    quartile_1 = df.iloc[1][row]
    quartile_3 = df.iloc[2][row]
    iqr = np.abs(quartile_3 - quartile_1)

    lower_bound = quartile_1 - (iqr * 1.5)
    upper_bound = quartile_3 + (iqr * 1.5)

    return {"lower": lower_bound, "min": df.iloc[0][row], "upper": upper_bound, "max": df.iloc[4][row]}


def checkifAccepted(data, df):
    presupuesto = data['presupuesto']
    subvencion = data['subvencion']
    country = data['country']
    startdate = data['startdate']

    presupuesto_ok = (presupuesto <= outliers_iqr(df, 'presupuesto')['upper']) and (presupuesto > 0)
    subvencion_ok = (subvencion <= outliers_iqr(df, 'subvencion')['upper']) and (subvencion > 0)
    country_ok = (country <= outliers_iqr(df, 'country')['max']) and (country > 0)
    startdate_ok = (startdate <= DATEENDH2020) and (startdate >= DATESTARTH2020)

    data = {
        "presupuesto": presupuesto_ok,
        "subvencion": subvencion_ok,
        "country": country_ok,
        "startdate": startdate_ok,
        "all": presupuesto_ok and subvencion_ok and country_ok and startdate_ok
    }

    return (data)
