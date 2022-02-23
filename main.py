import pathlib
import sys
sys.path.append(str(pathlib.Path().absolute()))

from utiles.configuration import ConfigurationFile
from utiles.generate import Generate
from utiles.load import Load

import argparse
import os

if __name__ == '__main__' :   
    parser = argparse.ArgumentParser(description = "Clustering model")
    parser.add_argument("-config", type = str, help = "<str> configuration file", required = True)
    parser.add_argument("-name", type=str, help=" name of section in the configuration file", required = False, default="CONFIG")
    parser.add_argument("-mode", type=str, choices=['generate', 'load'],  help=" generate or run", required = False, default = 'generate')
    parser.add_argument("-file", type=str, choices=['generate', 'load'],  help=" generate or run", required = False, default = 'Simulated_data.csv')    
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
    if pargs.mode == 'load':   
        input_file = pargs.file
        print("Carga de datos desde {} ...".format(input_file))
        data_load = Load(input_file)
        data_frame = data_load.createDF(sep=",")
        print("Datos cargados desde {}".format(input_file))
        print(data_frame)
     