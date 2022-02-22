import pandas as pd
import numpy as np
class Load:
    def __init__(self, source_file):
        self.source = source_file

    def createDF(self, sep=";"):
        self.data_frame = pd.read_csv(self.source, sep=sep)
        return self.data_frame

    def getFeatures(self, exclude=["id"]):
        return self.data_frame.columns.drop(exclude)

    def getData(self):
        return np.array(self.data_frame[self.getFeatures()])