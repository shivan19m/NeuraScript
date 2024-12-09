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
os.system('pip install numpy pandas matplotlib scikit-learn seaborn')

model = LinearRegression()
d1 = pd.read_csv("data.csv")
l1 = pd.read_csv("labels.csv")["Yearly Amount Spent"]
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
X_train, X_test, y_train, y_test = train_test_split(d1, l1, test_size=0.4, random_state=101)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
plt.scatter(y_test, predictions)
plt.xlabel("Actual Values")
plt.ylabel("Predictions")
plt.show()