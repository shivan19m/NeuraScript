from sklearn import datasets, linear_model, metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

# Install necessary dependencies
import os
os.system('pip install numpy pandas matplotlib scikit-learn')

model = LinearRegression()
d1 = pd.read_csv("data.csv")
l1 = pd.read_csv("labels.csv")
print(d1)
print(l1)