from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score

import numpy as np
import pandas as pd

class SearchOptimusK(object):
  def __init__(self, work_pca, max_clusters = 10, 
               max_iter = 1000, algorithm = None, kmeans_init = None):
      self.num_pca = work_pca.num_pca
      self.PCA_components = work_pca.PCA_components
      self.max_clusters = max_clusters
      self.max_iter = max_iter
      self.algorithm = "auto" if algorithm is None else algorithm
      self.kmeans_init = "k-means++" if kmeans_init is None else kmeans_init      
      self.elbow = 2
      self.silhoutte = 2
      self.GAP = 2

  def __getattr__(self, name: str):
      return object.__getattribute__(name)

  def __setattr__(self, name: str, value):
      self.__dict__[name] = value  

  def get_cluster_elbow(self):
    """
    Método curva de elbow para identificar el número óptimo de clusters
    """    
    num_clusters = range(2, self.max_clusters+1)
    
    models = [KMeans(n_clusters=i, max_iter = self.max_iter, random_state=29, 
                     algorithm=self.algorithm, init = self.kmeans_init) for i in num_clusters]
    score = [models[i].fit(self.PCA_components.iloc[:,:self.num_pca]).score(self.PCA_components.iloc[:,:self.num_pca]) for i in range(len(models))] 
    y_predict = [models[i].predict(self.PCA_components.iloc[:,:self.num_pca]) for i in range(len(models))]
    inercias = [models[i].inertia_ for i in range(len(models))] 

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].plot(num_clusters, inercias, marker='o')
    ax[0].set_title("Evolución de la varianza intra-cluster total", fontsize=18, fontweight="bold")
    ax[0].set_xlabel('Número clusters', fontsize=14)
    ax[0].set_ylabel('Intra-cluster (inertia)', fontsize=14);

    ax[1].plot(num_clusters,score)
    ax[1].grid(color='r', linestyle='dotted', linewidth=1)
    ax[1].set_title("Evolución del score total", fontsize = 18, fontweight="bold")
    ax[1].set_xlabel('Número de Clusters', fontsize=14)
    ax[1].set_ylabel('Score', fontsize=14)

    plt.show()

  def get_cluster_silhoutte(self):
    """
    Método silhouette para identificar el número óptimo de clusters
    """
    self.range_n_clusters = range(2, self.max_clusters+1)
    self.valores_medios_silhouette = []
    for n_clusters in self.range_n_clusters:
      modelo_kmeans = KMeans(
                        n_clusters   = n_clusters, 
                        max_iter = self.max_iter,
                        random_state = 29, 
                        algorithm = self.algorithm, init = self.kmeans_init
                    )
      cluster_labels = modelo_kmeans.fit_predict(self.PCA_components.iloc[:,:self.num_pca])
      silhouette_avg = silhouette_score(self.PCA_components.iloc[:,:self.num_pca], cluster_labels, metric="sqeuclidean")
      self.valores_medios_silhouette.append(silhouette_avg)
    self.ideal_number = list(range(2,self.max_clusters+1))[np.argmax(self.valores_medios_silhouette)]
    #self_values_medios_silhoutte = self.valores_medios_silhouette  
    return self.ideal_number, self.valores_medios_silhouette, self.range_n_clusters    

  def graphic_view(self):  
    fig, ax = plt.subplots(1, 1, figsize=(6, 3.84))
    ax.plot(self.range_n_clusters, self.valores_medios_silhouette, marker='o')
    ax.set_title("Evolución de media de los índices silhouette con {}".format(self.algorithm), fontsize=18, fontweight="bold")
    ax.set_xlabel('Número clusters', fontsize=14)
    ax.set_ylabel('Media índices silhouette', fontsize=14)
    plt.show();

  def get_cluster_GAP(self, nrefs=3, maxClusters=10):
    """
    Calculates KMeans optimal K using Gap Statistic 
    Params:
        data: ndarry of shape (n_samples, n_features)
        nrefs: number of sample reference datasets to create
        maxClusters: Maximum number of clusters to test for
    Returns: (gaps, optimalK)
    """
    data = self.PCA_components.iloc[:,:self.num_pca]
    gaps = np.zeros((len(range(2, maxClusters+1)),))
    resultsdf = pd.DataFrame({'clusterCount':[], 'gap':[]})
    for gap_index, k in enumerate(range(2, maxClusters+1)):
      # Holder for reference dispersion results
      refDisps = np.zeros(nrefs)
      # For n references, generate random sample and perform kmeans getting resulting dispersion of each loop
      for i in range(nrefs):      
        # Create new random reference set
        randomReference = np.random.random_sample(size=data.shape)
        # Fit to it
        km = KMeans(k, init = self.kmeans_init, max_iter = self.max_iter, random_state=29)
        km.fit(randomReference)
        refDisp = km.inertia_
        refDisps[i] = refDisp
        # Fit cluster to original data and create dispersion
        km = KMeans(k, init = self.kmeans_init, max_iter = self.max_iter, random_state=29)
        km.fit(data)
        
        origDisp = km.inertia_
        # Calculate gap statistic
        gap = np.log(np.mean(refDisps)) - np.log(origDisp)
        # Assign this loop's gap statistic to gaps
        gaps[gap_index] = gap
        
        #resultsdf = resultsdf.append({'clusterCount':k, 'gap':gap}, ignore_index=True)
        x_df = pd.DataFrame([[k, gap]], columns=['clusterCount', 'gap'])
        resultsdf = pd.concat([resultsdf, x_df], ignore_index=True)
    self.resultsdf = resultsdf
    self.GAP = self.resultsdf.clusterCount[gaps.argmax()]
    return (gaps.argmax() + 1, self.resultsdf, self.resultsdf.clusterCount[gaps.argmax()])

  def view_result_GAP(self):
    plt.plot(self.resultsdf['clusterCount'], self.resultsdf['gap'], linestyle='--', marker='o', color='b');
    plt.xlabel('K', fontsize=18);
    plt.ylabel('Estadístico GAP', fontsize=16);
    plt.title('Estadístico GAP versus K', fontsize=25, fontweight="bold")
    plt.show();

  def __str__(self) -> str:
    return "elbow : {0}; silhoutte : {1}; GAP : {2}\n NUM_COMPONENTES : {3}".format(self.elbow, 
    self.silhoutte, self.GAP, self.num_pca)