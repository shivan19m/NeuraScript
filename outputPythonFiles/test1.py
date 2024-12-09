from sklearn import datasets, linear_model, metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Install necessary dependencies
import os
os.system('pip install numpy pandas matplotlib scikit-learn seaborn')

model = LinearRegression()
d1 = pd.read_csv("data.csv")
l1 = pd.read_csv("labels.csv")["Yearly Amount Spent"]
print(d1)
print(l1)
x_train, x_test, y_train, y_test = train_test_split(d1, l1, test_size=0.4, random_state=101)
print(x_train)
print(x_test)
print(y_train)
print(y_test)