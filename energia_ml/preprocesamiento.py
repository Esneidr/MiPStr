class Estandarizador:
    # Aprende media y desviación en el entrenamiento y las reutiliza siempre

    def fit(self, X):
        self.media = X.mean(axis=0)
        self.desv = X.std(axis=0)
        return self

    def transform(self, X):
        return (X - self.media) / self.desv
