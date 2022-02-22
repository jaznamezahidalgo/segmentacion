import numpy as np
import pandas as pd
from sklearn.datasets import make_blobs

class Generate(object):
    def __init__(self, data_config, file_output="Generate.csv") :
        self.output = file_output
        self.configuracion = data_config

    def generate(self):
        archivo = open(self.output,"w")

        for item in range(1, self.items+1):
            self.header = self.header + ";I" + str(item);
        archivo.write(self.header + "\n")

        for index in range(1, self.observaciones+1):
            line = str(index)
            for item in range(1, self.items+1):
                logro = np.random.randint(5)
                line = line + ";" + str(self.escala[logro])
        
            archivo.write(line + "\n")
        archivo.close()

    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)

    def generate_data(self):
        """
        Genera la data completamente aleatorizada usando la librería sklearn
        """
        X, y = make_blobs(
            n_samples    = self.configuracion.observaciones, 
            n_features   = self.configuracion.items, 
            centers = self.configuracion.clusters,
            cluster_std = 0.6,
            shuffle      = True, 
            random_state = 0
        )
        self.X = X
        self.y = y

    def calculate_grade(self, puntaje):
        """
        Calcula la nota de acuerdo a la fórmula definida
        """
        PUNTAJE_CORTE = self.configuracion.puntaje_corte
        NOTA_MAXIMA = self.configuracion.nota_maxima
        NOTA_MINIMA = self.configuracion.nota_minima
        NOTA_APROBACION = self.configuracion.nota_aprobacion
        PUNTAJE_MAXIMO = self.configuracion.puntaje_maximo
        EXIGENCIA = self.configuracion.exigencia
        if puntaje >= PUNTAJE_CORTE:
            nota = round((NOTA_MAXIMA - NOTA_APROBACION)*(puntaje-PUNTAJE_CORTE)/(PUNTAJE_MAXIMO*(1-EXIGENCIA))+NOTA_APROBACION,1)
        else: 
            nota = round((NOTA_APROBACION - NOTA_MINIMA)*(puntaje/PUNTAJE_CORTE)+NOTA_MINIMA,1)
        return nota

    def calculate_category(self, nota):
        """
        Calcula la categoría de acuerdo a lo definido en los requerimientos
        """
        if nota >= 6.0: categoria = 1
        elif nota >= 5: categoria = 2
        elif nota >= 4: categoria = 3
        elif nota >= 3: categoria = 4
        else: categoria = 5
        return categoria

    def generate_headers_items(self):
        """
        Genera las cabeceras de los ítems de evaluación de acuerdo a lo que exige el modelo
        """
        n_items = self.configuracion.items
        items_features = []
        for n_item in range(1, n_items + 1):
            items_features.append('i' + str(n_item))
        self.items_features = items_features

    def generate_headers(self):
        """
        Genera las cabezeras que debe tener la data de acuerdo a lo que exige el modelo
        """
        n_items = self.configuracion.items
        all_features = ['id']
        items_features = self.generate_headers_items()
        for n_item in range(1, n_items + 1):
            all_features.append('i' + str(n_item))
        all_features = all_features + ['puntaje','nota','categoria']
        self.all_features = all_features

    def calculate_save_from_random(self):
        """
        Genera un archivo CSV con datos completamente aleatorios usando la librería de sklearn
        """
        n_observaciones = self.configuracion.observaciones
        n_items = self.configuracion.items
        n_clusters = self.configuracion.clusters
        MAX_ESCALA = self.configuracion.escala
        self.generate_data()
        self.generate_headers()
        self.data_frame = pd.DataFrame(self.X, columns=self.items_features)
        self.data_frame = self.data_frame.apply(lambda value : round(abs(value)), axis = 1)
        for column in self.data_frame.columns:
            self.data_frame[column] = self.data_frame[column].apply(lambda value : round(np.max([value, 1.0])))
            self.data_frame[column] = self.data_frame[column].apply(lambda value : round(np.min([value, MAX_ESCALA])))
        self.data_frame['puntaje'] = self.data_frame.sum(axis=1)
        self.data_frame['nota'] = self.data_frame['puntaje'].apply(lambda row : self.calculate_grade(row))
        self.data_frame['categoria'] = self.data_frame['nota'].apply(lambda row : self.calculate_category(row))
        self.data_frame['id'] = range(1, self.X.shape[0]+1)
        self.data_frame = self.data_frame.reindex(columns=self.all_features)
        self.data_frame.to_csv(self.output, index = False)
         
    def calculate_columns(self):
        """
        Calcula las columnas puntaje y nota de acuerdo a lo que exige el modelo
        """
        self.generate_headers()
        self.data_frame[self.items_features]
        self.data_frame = self.data_frame.apply(lambda value : round(abs(value)), axis = 1)
        MAX_ESCALA = self.configuracion.escala
        for column in self.data_frame.columns:
            self.data_frame[column] = self.data_frame[column].apply(lambda value : np.max([value, 1.0]))
            self.data_frame[column] = self.data_frame[column].apply(lambda value : np.min([value, MAX_ESCALA]))
            self.data_frame['puntaje'] = self.data_frame.sum(axis=1)
            self.data_frame['nota'] = self.data_frame['puntaje'].apply(lambda row : self.calculate_grade(row))
            self.data_frame['categoria'] = self.data_frame['nota'].apply(lambda row : self.calculate_category(row))
            self.data_frame['id'] = range(1, self.X.shape[0]+1)
            self.data_frame = self.data_frame.reindex(columns=self.all_features)