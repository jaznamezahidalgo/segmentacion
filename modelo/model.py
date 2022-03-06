from sklearn.cluster import KMeans
import matplotlib.pyplot as plt 

import numpy as np

class SegmentationModel(object):
  def __init__(self, features : np.array, work_pca, x_clusters, x_iterations = 1000, name = "KMeans", num_pca = None):
    self.X = work_pca.PCA_components
    
    self.n_clusters = x_clusters
    self.num_pca = work_pca.num_pca if num_pca is None else num_pca
    self.max_iter = x_iterations
    self.dict_summary = {}
    self.name = name
    self.features = features
    # Crea el modelo
    self.model = KMeans(n_clusters = self.n_clusters, max_iter = self.max_iter, 
                           random_state=29, init='k-means++',
                       algorithm = 'auto').fit(X=self.X.iloc[:,:self.num_pca])
    self.y_predict = self.model.predict(self.X.iloc[:,:self.num_pca])

    self.dict_summary[name] = {}
    self.dict_summary[name]['inertia'] = self.model.inertia_
    self.dict_summary[name]['n_features_in'] = self.model.n_features_in_
    self.dict_summary[name]['init'] = self.model.init
    self.dict_summary[name]['clusters'] = self.model.n_clusters
    self.dict_summary[name]['model'] = self.model
  
  def view_graphic(self, feature_x : int = 0, feature_y : int = 1):
    fig, ax = plt.subplots(1, 1, figsize=(5, 4))
    ax.scatter(
        x = self.X[feature_x],
        y = self.X[feature_y], 
        c = self.y_predict,
        marker    = 'o',
        edgecolor = 'black'
    )
    ax.set_xlabel(self.features[feature_x])
    ax.set_ylabel(self.features[feature_y])
    ax.set_title('KMeans K={0}, PCA={1}'.format(self.n_clusters, self.num_pca), fontsize=20, fontweight="bold")
    plt.show();

  def __getattr__(self, name: str):
      return object.__getattribute__(name)
    
  def __setattr__(self, name: str, value):
      self.__dict__[name] = value