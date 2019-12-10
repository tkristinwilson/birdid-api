#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 17:51:45 2019

@author: KristinWilson
"""

import requests

#resp = requests.post("http://localhost:5000/predict", files={"file": open('cat.jpg','rb')})
#resp = requests.post("http://localhost:5000/predict", files={"file": open('content/prediction/0000001.jpg','rb')})
resp = requests.post("http://localhost:5000/predict", files={"file": open('bellbird2.jpg','rb')})

print(resp.content)