import numpy as np
from sklearn.preprocessing import StandardScaler

class Data(object):
  def __init__(self, data, column, limit):
      self.data = data
      self.query = "{0} >= {1}".format(column, limit) 
      self.selected = self.data.query(self.query)

  def __getattr__(self, name: str):
      return object.__getattribute__(name)

  def __setattr__(self, name: str, value):
      self.__dict__[name] = value  

  def get_metrics_by_columns(self, columns, include="selected"):
    if include == "all":
      return self.data.groupby('categoria')[columns].describe()    
    return self.selected.groupby('categoria')[columns].describe()

  def scale_data(self, n_items):
    data_selected = self.selected
    items_features = []
    for n_item in range(1, n_items + 1):
      items_features.append('i' + str(n_item))  
    exclude = data_selected.columns.difference(items_features)
    X_features = np.array(data_selected[data_selected.columns.drop(exclude)])  
    scaler = StandardScaler()
    X_features_scaled = scaler.fit_transform(X_features)
    return X_features_scaled