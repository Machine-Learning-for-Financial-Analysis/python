import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load the datasets
df = pd.read_csv('All_variables.csv', dtype=float, delimiter=',')

# choose the features data and targets data
features = df.drop(['RV'], axis = 1)
targets = df['RV']

linear_features=sm.add_constant(features)  #the first 200 are NA values because of moving average
train_size=int(0.85*targets.shape[0])
train_features=linear_features[:train_size]
train_targets=targets[:train_size]
test_features=linear_features[train_size:]
test_targets=targets[train_size:]
features.head()

# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(linear_features, targets, test_size = 1/3, random_state = 42)
# Fitting Simple Linear Regression to the Training set
regressorA = LinearRegression()
regressorA.fit(X_train[['SPXrv10d','SPXrv10w','SPXrv10m']], y_train)
# Predicting the Test set results
y_train_predA = regressorA.predict(X_train[['SPXrv10d','SPXrv10w','SPXrv10m']])
y_test_predA = regressorA.predict(X_test[['SPXrv10d','SPXrv10w','SPXrv10m']])

print('Coefficients: \n', regressorA.coef_)
# The mean squared error
print("Mean squared error: %.2f" % np.mean((regressorA.predict(X_test[['SPXrv10d','SPXrv10w','SPXrv10m']]) - y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regressorA.score(X_test[['SPXrv10d','SPXrv10w','SPXrv10m']], y_test))

#calculate R^2 score
print(r2_score(y_train, y_train_predA))
print(r2_score(y_test, y_test_predA))

# Show the plot
plt.scatter(y_train_predA, y_train, label='Train')
plt.scatter(y_test_predA, y_test, label='Test')
x = np.linspace(-0.5,17,100)
plt.plot(x, x, '-r', label='Actual=Prediction',linewidth=1.5)
plt.axhline(y=10, color='#838B8B', linewidth=1, linestyle='--')
plt.legend(fontsize=20, loc=2)
plt.xlabel('Predictions',fontsize=15)
plt.ylabel('Actual',fontsize=15)
plt.show()