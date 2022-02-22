from configparser import ConfigParser

class ConfigurationFile(object):
    def __init__(self, str_config, modelname):
        config = ConfigParser({'N_ITEMS' : '8',                                    
                                   'ESCALA': '5',
                                   'N_OBSERVACIONES': '100',
                                   "NOTA_MAXIMA" : '7.0',
                                   "NOTA_MINIMA" : '1.0',
                                   "NOTA_APROBACION": '4.0',
                                   "EXIGENCIA" : '0.6',
                                   "CLUSTERS" : '3'
                                   })
        config.read(str_config)   
        self.items = config[modelname].getint("ITEMS")
        self.escala = config[modelname].getint("ESCALA")    
        self.observaciones = config[modelname].getint("OBSERVACIONES")        
        self.nota_maxima = config[modelname].getint("NOTA_MAXIMA")
        self.nota_minima = config[modelname].getint("NOTA_MINIMA")
        self.nota_aprobacion = config[modelname].getint("NOTA_APROBACION")
        self.exigencia = config[modelname].getfloat("EXIGENCIA")
        self.clusters = config[modelname].getint("CLUSTERS")
        self.puntaje_maximo = self.escala*self.items
        self.puntaje_corte = round(self.exigencia*self.puntaje_maximo)

    def __getattr__(self, name: str):
        return object.__getattribute__(name)
    
    def __setattr__(self, name: str, value):
        self.__dict__[name] = value