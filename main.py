"""
@auhor - Jazna Meza Hidalgo
Uso para cargar datos, generar modelo y ver resultados
    $ python3 main.py -config=config/model.config -mode=load -file=data/Simulated_data_bad.csv
"""
import pathlib
import sys
from modelo.pca import PCA_Work
sys.path.append(str(pathlib.Path().absolute()))

from utiles.configuration import ConfigurationFile
from utiles.generate import Generate
from utiles.data import Data
from utiles.calculos import evaluate_with_silhoutte, display_variants, generate_descarted
from modelo.search import SearchOptimusK
from modelo.model import SegmentationModel
from modelo.result import SegmentationResult

import pandas as pd
import numpy as np
import random
import argparse
import os

if __name__ == '__main__' :   
    parser = argparse.ArgumentParser(description = "Clustering model")
    parser.add_argument("-config", type = str, help = "<str> configuration file", required = True)
    parser.add_argument("-name", type=str, help=" name of section in the configuration file", required = False, default="CONFIG")
    parser.add_argument("-mode", type=str, choices=['generate', 'load', 'descarted'],  help=" generate or load or descarted", required = False, default = 'generate')
    parser.add_argument("-file", type=str,  help="name of file", required = False, default = 'Simulated_data.csv')    
    pargs = parser.parse_args()  

    configurationFile = ConfigurationFile(pargs.config, pargs.name)   
    print("Configuración cargada ...")
    print("\tNOTA MÁXIMA : {}".format(configurationFile.nota_maxima))
    print("\tNOTA MÍNIMA : {}".format(configurationFile.nota_minima))
    print("\tCLUSTERS : {}".format(configurationFile.clusters))
    print("\tESCALA : {}".format(configurationFile.escala))
    print("\tEXIGENCIA : {}".format(configurationFile.exigencia))
    print("\tITEMS : {}".format(configurationFile.items))
    print("\tOBSERVACIONES : {}".format(configurationFile.observaciones))
    print("\tNOTA APROBACIÓN : {}".format(configurationFile.nota_aprobacion))
    print("\tPUNTAJE CORTE : {}".format(configurationFile.puntaje_corte))
    print("\tPUNTAJE MÁXIMO : {}".format(configurationFile.puntaje_maximo))  
    print("\tPUNTAJE MÁXIMO : {}".format(configurationFile.puntaje_maximo)) 
    if pargs.mode == 'generate':
        output_file = pargs.file
        print("Genera data aleatoria en {}".format(output_file))
        
        data_generate = Generate(configurationFile,file_output=output_file)
        data_generate.calculate_save_from_random()
        print("Datos generados en el archivo {}".format(output_file))

    if pargs.mode == 'descarted':
        input_file = pargs.file
        print("Carga de datos desde {} ...".format(input_file))
        data_load = Data(configurationFile, input_file, sep=",")
        output_file = "Descartados_" + str(random.randrange(100)) + ".csv"
        total, descartados, data_other_model = generate_descarted(data_load.data_frame, 
                        out_file = output_file)
        print(data_other_model)
        
        print("{0} registros descartados de un total de {1} registos en el archivo {2}".format(descartados, total, output_file))        

    if pargs.mode == 'load':   
        input_file = pargs.file
        print("Carga de datos desde {} ...".format(input_file))
        data_load = Data(configurationFile, input_file, sep=",")
        data_frame = data_load.data_frame        
        print("Datos cargados desde {0} con {1} registros".format(input_file, data_frame.shape[0]))
        data_load.create_selected('data/Descartados_42.csv','categoria', 4)
        data_frame = data_load.selected
        print("Datos cargados finales {}".format(data_frame.shape[0]))
        #print(data_frame)

        # Escalado de datos
        x_scaled = data_load.scale_data(configurationFile.items)
        #print(x_scaled)
        
        # Obtiene estadísticas
        # print(data_load.get_metrics_by_columns(['puntaje', 'nota', 'i1']))
        # print(data_load.get_metrics_by_columns(['puntaje', 'nota', 'i1'], include="all"))
        
        # Reducción de dimensionalidad
        pca_work = PCA_Work(x_scaled)
        # Gráfico de las varianzas
        # print(pca_work.plotting_variances())
        # Determina el valor de PCA
        """
        lst_num_features = range(2, configurationFile.items+1)
        for x_init in ['k-means++', 'random']:
            for num_features in lst_num_features:
                pca_work.num_pca = num_features
                print(pca_work.cluster_by_PCA(max_clusters = 10, kmeans_init = x_init))        
        """
        # Con lo anterior se fijan los valores de la reducción de dimensionalidad
        pca_work.num_pca = 2
        optimus = SearchOptimusK(pca_work, algorithm = 'auto')
        # Comprueba usando la curva de elbow
        """
        for alg in ['auto', 'elkan']:
            print("Algoritmo {}".format(alg))
            optimus.get_cluster_elbow()
        """
        optimus.elbow = 7
        # Comprueba usando silhoutte
        ideal_number, values, rc = optimus.get_cluster_silhoutte()
        print("Cluster ideal, usando índices silhouette con algoritmo {0} es {1}".format('random', ideal_number))
        optimus.graphic_view()
        optimus.silhoutte = ideal_number        
        
        # Comprueba usando estadústico GAP
        #x_optimus = SearchOptimusK(pca_work, algorithm = 'random')
        score_g, df, ideal_cluster_GAP = optimus.get_cluster_GAP(nrefs=5, maxClusters=10)
        optimus.view_result_GAP()
        #print(df)
        print(optimus)

        # Variante 1, usa el número de cluster que arroja el análisis anterior
        model_kx = SegmentationModel(pca_work, 7)
        model_kx.view_graphic()
        df_summary = pd.DataFrame(model_kx.dict_summary).T
        #print(df_summary)        
        # Variante 2 - Modifica el número de elementos de PCA
        model_ky = SegmentationModel(pca_work, 7, name="KMeans-1", 
                        num_pca = pca_work.num_pca+1)
        model_ky.view_graphic()
        #df_summary = df_summary.append(pd.DataFrame(model_ky.dict_summary).T)
        df_summary = pd.concat([df_summary, pd.DataFrame(model_ky.dict_summary).T])
        # Variante 3 - Modifica en 2 el valor de componentes PCA
        model_kz = SegmentationModel(pca_work, 7, name="KMeans-2", num_pca = pca_work.num_pca+2)
        model_kz.view_graphic()
        #df_summary = df_summary.append(pd.DataFrame(model_kz.dict_summary).T)  
             
        df_summary = pd.concat([df_summary, pd.DataFrame(model_kz.dict_summary).T])
        # Variante 4 - Mantiene configuración de PCA y modifica el valor de clusters
        model_kw = SegmentationModel(pca_work, 2, name="KMeans-3")

        model_kw.view_graphic()
        #df_summary = df_summary.append(pd.DataFrame(model_kw.dict_summary).T)        
        df_summary = pd.concat([df_summary, pd.DataFrame(model_kw.dict_summary).T])
        # Imprime las insercias de cada variante
        print(df_summary[['inertia']])    

        # Evaluación de los modelos usando el coeficiente de silhoutte
        evaluate_with_silhoutte(pca_work, model_kx)
        print("*"*50)
        evaluate_with_silhoutte(pca_work, model_ky)
        print("*"*50)
        evaluate_with_silhoutte(pca_work, model_kz)
        print("*"*50)
        evaluate_with_silhoutte(pca_work, model_kw)  

        # Comparación de variantes, alternando el número de clusters
        display_variants(pca_work, 10, kmeans_init='random')      

        # Análisis de clusters
        # Se debe entregar el modelo que ha sido seleccionado
        result = SegmentationResult(data_frame, model_kx.y_predict)
        data_final = result.data_final        

        # Muestra cantidad de estudiantes por grupo
        print(result.get_total_by_cluster())
        # Estatdísticas de cada grupo
        lst_metrics = [np.mean, np.median, np.max, np.min]
        lst_include = ['nota', 'puntaje']
        print(result.get_metrics_by_cluster(lst_include, lst_metrics))  

        # Genera la lista de ítems de acuerdo a la configuración
        lst_include = []
        for i in range(1, configurationFile.items+1):
            name_item = "i" + str(i)
            lst_include.append(name_item)

        print(result.get_metrics_by_cluster(lst_include, lst_metrics))

        # Revisa outliers
        result.view_outliers('puntaje')

        result.view_outliers('nota')

        # Guarda resultados
        """
        result.to_csv() # Un CSV por grupo
        result.to_csv(unique_file = True) # Un solo archivo CSV
        """