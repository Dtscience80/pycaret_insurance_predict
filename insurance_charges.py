# -*- coding: utf-8 -*-
"""Insurance Charges.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jJnbXrbURlZZuTe-9v1WwluK8EUit-VK
"""

!pip install --pre pycaret

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
import seaborn as sns
from pycaret.datasets import get_data
from pycaret.regression import *
mpl.rcParams['figure.dpi'] = 300

"""## Loading the data
Health Insurance Data where age, sex, bmi, children, smoker, and region are features and charges is a target.

charges are nothing but the billed charges for every individual based on features.

We will create a model that will predict the charges column.
"""

data = get_data('insurance')

data.shape

data.info()

numeric = ['age', 'bmi', 'charges', 'smoker']

sns.pairplot(data[numeric], hue='smoker')
plt.show()

"""## Data Viz
we use hue mapping to highlight the differences between smokers and non-smokers. As we can see, age is correlated with charges, i.e, people get higher charges as they grow older. In spite of that, being a non-smoker keeps the cost lower for most people, regardless of their age. Furthermore, overweight and obese people don't seem to get significantly higher charges, unless they are smokers.
"""

numeric = ['age', 'bmi', 'children', 'charges']
categorical = ['smoker', 'sex', 'region']

"""## Initialize the PyCaret"""

reg = setup(
    data = data,
    target= 'charges',
    train_size = 0.8,
    session_id = 7402,
    normalize = True
)

best = compare_models(sort='RMSE')

model = create_model('gbr', fold= 10)

"""## Fine Tuning the Model"""

params = {
    'learning_rate': [0.01, 0.02, 0.05],
    'max_depth': [1,2,3,4,5,6,7,8],
    'subsample': [0.4, 0.5, 0.6, 0.7, 0.8],
    'n_estimators': [100,200.300,400,500,600]
}

tuned_model = tune_model(
    model,
    optimize='RMSE',
    fold=10,
    custom_grid=params,
    n_iter= 30
)

"""## Making Predictions and Saving the Model"""

predict_model(model)

evaluate_model(model)

final_model = finalize_model(model)
save_model(final_model, 'insurance_model')
