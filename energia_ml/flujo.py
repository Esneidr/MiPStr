class FlujoModelo:
    # Une preprocesamiento + modelo. Recibe datos crudos.

    def __init__(self, preprocesador, modelo):
        self.preprocesador = preprocesador
        self.modelo = modelo

    def entrenar(self, X, y):
        self.preprocesador.fit(X)
        self.modelo.fit(self.preprocesador.transform(X), y)
        return self

    def predecir(self, X):
        return self.modelo.predict(self.preprocesador.transform(X))

    def evaluar(self, X, y):
        return self.modelo.score(self.preprocesador.transform(X), y)
