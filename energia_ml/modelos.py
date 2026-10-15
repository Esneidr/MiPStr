import numpy as np


class ModeloBase:
    # Clase madre de los modelos entrenados con descenso de gradiente

    def __init__(self, tasa=0.1, iteraciones=500):
        self.tasa = tasa
        self.iteraciones = iteraciones
        self.w = None
        self.b = 0.0
        self.historial = []

    def _activacion(self, z):
        raise NotImplementedError

    def _costo(self, y, y_hat):
        raise NotImplementedError

    def fit(self, X, y):
        n, d = X.shape
        self.w, self.b, self.historial = np.zeros(d), 0.0, []
        for _ in range(self.iteraciones):
            y_hat = self._activacion(X @ self.w + self.b)
            error = y_hat - y
            self.w -= self.tasa * (X.T @ error) / n
            self.b -= self.tasa * error.mean()
            self.historial.append(self._costo(y, y_hat))
        return self

    def __repr__(self):
        return f"{type(self).__name__}(tasa={self.tasa}, iteraciones={self.iteraciones})"


class RegresionLineal(ModeloBase):
    def _activacion(self, z):
        return z

    def _costo(self, y, y_hat):
        return np.mean((y - y_hat) ** 2)

    def predict(self, X):
        return X @ self.w + self.b

    def score(self, X, y):
        y_hat = self.predict(X)
        return 1 - np.sum((y - y_hat) ** 2) / np.sum((y - y.mean()) ** 2)


class RegresionLogistica(ModeloBase):
    def _activacion(self, z):
        return 1 / (1 + np.exp(-z))

    def _costo(self, y, y_hat):
        y_hat = np.clip(y_hat, 1e-9, 1 - 1e-9)
        return -np.mean(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat))

    def predict_proba(self, X):
        return self._activacion(X @ self.w + self.b)

    def predict(self, X):
        return (self.predict_proba(X) >= 0.5).astype(int)

    def score(self, X, y):
        return np.mean(self.predict(X) == y)
