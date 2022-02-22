from sklearn.cluster import KMeans
import matplotlib.pyplot as plt 
class SegmentationModel(object):
  def __init__(self, X, x_clusters, n_pca, x_iterations = 1000, name = "KMeans"):
    self.X = X
    
    self.n_clusters = x_clusters
    self.num_pca = n_pca
    self.max_iter = x_iterations
    self.dict_summary = {}
    self.name = name
    # Crea el modelo
    self.model = KMeans(n_clusters = self.n_clusters, max_iter = self.max_iter, 
                           random_state=29, init='random',
                       algorithm = 'auto').fit(X=X.iloc[:,:self.num_pca])
    self.y_predict = self.model.predict(self.X.iloc[:,:self.num_pca])

    self.dict_summary[name] = {}
    self.dict_summary[name]['inertia'] = self.model.inertia_
    self.dict_summary[name]['n_features_in'] = self.model.n_features_in_
    self.dict_summary[name]['init'] = self.model.init
    self.dict_summary[name]['clusters'] = self.model.n_clusters
    self.dict_summary[name]['model'] = self.model
  
  def view_graphic(self):
    fig, ax = plt.subplots(1, 1, figsize=(5, 4))
    ax.scatter(
        x = self.X[0],
        y = self.X[1], 
        c = self.y_predict,
        marker    = 'o',
        edgecolor = 'black'
    )
    ax.set_title('KMeans K={0}, PCA={1}'.format(self.n_clusters, self.num_pca), fontsize=20, fontweight="bold");

  def __getattr__(self, name: str):
      return object.__getattribute__(name)
    
  def __setattr__(self, name: str, value):
      self.__dict__[name] = value