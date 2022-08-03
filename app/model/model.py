import numpy as np
from sklearn.linear_model import LinearRegression

def fit():
    rnstate = np.random.RandomState(1)
    x = 10 * rnstate.rand(50)
    y = 2 * x - 5 + rnstate.randn(50)

    model = LinearRegression(fit_intercept=True)
    model.fit(x[:, np.newaxis], y)
    xfit = np.linspace(0, 10, 1000)
    return model.predict(xfit[:, np.newaxis])
    