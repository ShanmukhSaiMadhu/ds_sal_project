# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 18:57:23 2024

@author: madhu
"""

import glassdoor_scraper as gs
import pandas as pd

path = 'D:/DA/Projects/Data Science Salary Prediction/ds_sal_project/chromedriver.exe'

df = gs.get_jobs('data_scientist', 15, False, path, 15)
