# -*- coding: utf-8 -*-
"""Copia de 3.1 RandomForestRegressor.ipynb

# **3. Creation of the predictive model**

**Imports**
"""

import pandas as pd
import numpy as np
from IPython.display import Image, display
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split,cross_val_score,GridSearchCV
import matplotlib.pyplot as plt
import warnings

"""# **3.1 RandomForestRegressor**

**Why RandomForestRegressor?** It is a regression model that uses multiple decision trees to make predictions. Each tree is trained on a random subset of data and features, which reduces the dependency between them and improves the efficiency of the model. When making a prediction, each tree provides its result, and the model calculates the average of these predictions.

This model is very suitable for our case because it avoids overfitting, can handle non-linear relationships, performs well with noisy data or outliers, and additionally, we can determine the importance of each feature for subsequent modeling.
"""

df_cleaned = pd.read_csv("dataframe_final.csv",sep=",")
column_translation = {
    'Any': 'Year',
    'Mes': 'Month',
    'Dia': 'Day',
    'Tram_Horari': 'Time_Slot',
    'Codi_Postal': 'Postal_Code',
    'Valor': 'Value',
    'temperature_2m': 'Temperature_2m',
    'apparent_temperature': 'Apparent_Temperature',
    'wind_speed_10m': 'Wind_Speed_10m',
    'sunshine_duration': 'Sunshine_Duration',
    'direct_radiation': 'Direct_Radiation',
    'Dia_Setmana': 'Weekday',
    'Tasa interanual del IPI': 'Yearly_IPI_Rate',
    'dew_point_2m': 'Dew_Point_2m'
}

df_cleaned.rename(columns=column_translation, inplace=True)
df_cleaned.describe()

"""**Significance** of each independent variable with respect to the dependent variable"""

X = df_cleaned[['Any', 'Mes', 'Dia','Tram_Horari','Codi_Postal', 'temperature_2m',
                  'apparent_temperature','rain','wind_speed_10m','is_day',
                  'sunshine_duration','direct_radiation','Dia_Setmana',
                  'Festiu','Tasa interanual del IPI','dew_point_2m']]

y = df_cleaned['Valor']

model = RandomForestRegressor()
model.fit(X, y)
importances = model.feature_importances_
feature_importance_df = pd.DataFrame({'Variable': X.columns, 'Importance': importances})
print(feature_importance_df.sort_values(by='Importance', ascending=False))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse= mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"R² Score: {r2}")
print('Mean Absolute Percentage Error (MAPE): ',mae*100/(y_test.max()-y_test.min()))

"""Eliminate the features that do not add value, creating new models and testing their performance to find the best combination of independent variables that explain the target variable, in our case 'Valor,' the energy demand."""

X_reduced = X.drop(columns=[ 'rain', 'wind_speed_10m','dew_point_2m','Tasa interanual del IPI'])
X_train, X_test, y_train, y_test = train_test_split(X_reduced, y, test_size=0.2, random_state=42)

model_reduced = RandomForestRegressor()
model_reduced.fit(X_train, y_train)
y_pred = model_reduced.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse= mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"R² Score: {r2}")
print('Mean Absolute Percentage Error (MAPE): ',mae*100/(y_test.max()-y_test.min()))

X_reduced2 = X.drop(columns=['rain', 'is_day', 'sunshine_duration','Festiu', 'wind_speed_10m','temperature_2m','dew_point_2m'])

X_train, X_test, y_train, y_test = train_test_split(X_reduced2, y, test_size=0.2, random_state=42)

model_reduced2 = RandomForestRegressor()
model_reduced2.fit(X_train, y_train)
y_pred = model_reduced2.predict(X_test)

# Calcular el MAE y el MSE
mae = mean_absolute_error(y_test, y_pred)
mse= mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"R² Score: {r2}")
print('Mean Absolute Percentage Error (MAPE): ',mae*100/(y_test.max()-y_test.min()))

"""We will try a less restrictive model with feature importance and compare it with the previous one."""

X_reduced3 = X.drop(columns=['rain', 'is_day', 'sunshine_duration','Festiu', 'wind_speed_10m','temperature_2m','dew_point_2m',"Tasa interanual del IPI"])

X_train, X_test, y_train, y_test = train_test_split(X_reduced3, y, test_size=0.2, random_state=42)

model_reduced3 = RandomForestRegressor()
model_reduced3.fit(X_train, y_train)
y_pred = model_reduced3.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse= mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"R² Score: {r2}")
print('Mean Absolute Percentage Error (MAPE): ',mae*100/(y_test.max()-y_test.min()))

X_reduced4 = X.drop(columns=[ 'wind_speed_10m','temperature_2m','dew_point_2m',"Tasa interanual del IPI"])

X_train, X_test, y_train, y_test = train_test_split(X_reduced4, y, test_size=0.2, random_state=42)

model_reduced4 = RandomForestRegressor()
model_reduced4.fit(X_train, y_train)
y_pred = model_reduced4.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse= mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"R² Score: {r2}")
print('Mean Absolute Percentage Error (MAPE): ',mae*100/(y_test.max()-y_test.min()))

"""**GridSearchCV** with the selected features"""

X_reduced4 = X.drop(columns=['wind_speed_10m', 'temperature_2m', 'dew_point_2m', "Tasa interanual del IPI"])

X_train, X_test, y_train, y_test = train_test_split(X_reduced4, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(random_state=42)

param_grid = {
    'n_estimators': [300, 400],
    'min_samples_split': [2, 3, 5],
    'min_samples_leaf': [1, 2, 4],
    'ccp_alpha': [0.0, 0.01, 0.05]  # L2 reg.
}

grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, scoring='neg_mean_absolute_error', n_jobs=1, verbose=1)
grid_search.fit(X_train, y_train)

print("Best hyperparametres:", grid_search.best_params_)

best_model = grid_search.best_estimator_
best_model.fit(X_train, y_train)

y_pred = best_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"R² Score: {r2}")
print('Mean Absolute Error (MAE) en %: ', mae * 100 / (y_test.max() - y_test.min()))

X_reduced4 = X.drop(columns=['wind_speed_10m', 'temperature_2m', 'dew_point_2m', "Tasa interanual del IPI"])

X_train, X_test, y_train, y_test = train_test_split(X_reduced4, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(n_estimators=300,random_state=42,n_jobs=-1)
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"R² Score: {r2}")
print('Mean Absolute Error (MAE) en %: ', mae * 100 / (y_test.max() - y_test.min()))

"""We will graph the results of our predictions against the actual values."""

plt.figure(figsize=(6, 4))
plt.scatter(y_test, y_pred, alpha=0.2, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2, color='red')  # Línea ideal
plt.title("Prediccions vs Valors Reals")
plt.xlabel("Valors Reals")
plt.ylabel("Prediccions")
plt.grid()
plt.show()

"""# **3.1.2 Quantifying the associated uncertainty**

The uncertainty that we calculate with the standard deviation (std) of the predictions from each of the trees is a measure of the variability or dispersion of the model’s tree predictions, for each value of the target variable, in our case, energy demand.

*   68% of the data is within a range of ±1 standard deviation.
*   95% of the data is within ±2 standard deviations.
*   99.7% of the data is within ±3 standard deviations.
"""

warnings.filterwarnings('ignore') #X has feature names, but DecisionTreeRegressor was fitted without feature names

# Obtenir les prediccions dels diferents arbres
all_tree_preds = np.array([tree.predict(X_test) for tree in rf_model.estimators_])

# Mitjana de les prediccions (predicció final)
final_prediction = np.mean(all_tree_preds, axis=0)

# Incertesa (per exemple, desviació estàndard de les prediccions)
prediction_uncertainty = np.std(all_tree_preds, axis=0)

# Crear el DataFrame amb les dues columnes
df_predictions = pd.DataFrame({
    'Predicció': final_prediction,
    'Incertesa': prediction_uncertainty
})

# Mostrar el DataFrame
print(df_predictions.head())

print('Incertesa mitjana: ',df_predictions['Incertesa'].median(),'/','Respecte el total: ',(df_predictions['Incertesa'].median()/(y_test.max()-y_test.min()))*100,'%')
print('Incertesa mitjana aritmética: ',df_predictions['Incertesa'].mean(),'/','Respecte el total: ',(df_predictions['Incertesa'].mean()/(y_test.max()-y_test.min()))*100,'%')

# Graficar les prediccions contra la incertesa
plt.figure(figsize=(10, 3))
plt.scatter(final_prediction, prediction_uncertainty, alpha=0.07)
plt.title("Predicció vs Incertesa")
plt.xlabel("Predicció Final")
plt.ylabel("Incertesa (Desviació Estàndard)")
plt.show()

df = pd.DataFrame(X_test, columns=['Any', 'Mes', 'Dia','Tram_Horari','Codi_Postal',
                  'apparent_temperature','sunshine_duration','direct_radiation','Dia_Setmana',
                  'Festiu','Tasa interanual del IPI'])

# Afegir les prediccions al DataFrame
df['Predicció'] = final_prediction
df['Incertesa'] = prediction_uncertainty
df['Valor'] = y_test

# Agrupar per 'Any' i 'Mes' i calcular la mitjana
df_grouped = df.groupby(['Any', 'Mes']).agg({
    'Predicció': 'mean',       # Mitjana de les prediccions
    'Valor': 'mean',           # Mitjana dels valors reals
    'Incertesa': 'mean'        # Mitjana de la incertesa
}).reset_index()

# Calcular l'error absolut
df_grouped['Error'] = abs(df_grouped['Valor'] - df_grouped['Predicció'])

# Definir els intervals per l'error
bins = [0, 500, 2000, 5000, np.inf]  # Definir intervals d'error
labels = ['Baix Error', 'Mitjà Error', 'Alt Error', 'Molt Alt Error']  # Etiquetes per cada interval

# Assignar la categoria d'error segons l'interval
df_grouped['Error_Category'] = pd.cut(df_grouped['Error'], bins=bins, labels=labels)

# Crear el gràfic
plt.figure(figsize=(12, 6))

# Assignar colors per cada categoria d'error
color_map = {'Baix Error': 'green', 'Mitjà Error': 'yellow', 'Alt Error': 'orange', 'Molt Alt Error': 'red'}

# Crear el gràfic de dispersió amb colors categòrics per error
for category, color in color_map.items():
    category_data = df_grouped[df_grouped['Error_Category'] == category]
    plt.scatter(category_data.index, category_data['Predicció'],
                c=color, label=category, marker='o', edgecolors='k', s=100)  # S = size per controlar la mida dels punts

# Afegir la línia que uneix els punts de les prediccions
plt.plot(df_grouped.index, df_grouped['Predicció'], color='blue', linestyle='-', alpha=0.8, label='Línia Predicció')

# Afegir les "bales d'error" per mostrar la incertesa
plt.errorbar(df_grouped.index, df_grouped['Predicció'], yerr=df_grouped['Incertesa'], fmt='o', color='black', alpha=0.5, label='Incertesa')

# Afegir títols i etiquetes
plt.title('Predicció per Any i Mes amb Error Categòric i Incertesa')
plt.xlabel('Índex (Any-Mes)')
plt.ylabel('Valor Predicció')
plt.xticks(df_grouped.index, [f"{int(row['Any'])}-{int(row['Mes'])}" for _, row in df_grouped.iterrows()], rotation=90)

# Afegir llegenda
plt.legend()

# Mostrar el gràfic
plt.tight_layout()  # Per ajustar l'espai entre les etiquetes i el gràfic
plt.show()
