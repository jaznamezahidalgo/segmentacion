class PCA_Work(object):
  def __init__(self, features_scaled):
      self.X_features_scaled = features_scaled
      self.num_pca = 1      

  def __getattr__(self, name: str):
      return object.__getattribute__(name)

  def __setattr__(self, name: str, value):
      self.__dict__[name] = value  

  def plotting_variances(self):
    # Plotting the variances for each PC
    pca = PCA()
    principal_components = pca.fit_transform(self.X_features_scaled)
    PC = range(1, pca.n_components_+1)
    plt.bar(PC, pca.explained_variance_ratio_, color='blue')
    plt.xlabel('Componentes principales')
    plt.ylabel('Varianza %')
    plt.xticks(PC)
    plt.title("Varianza utilizando varios componentes", fontsize=18, fontweight="bold")

    # Putting components in a dataframe for later
    self.PCA_components = pd.DataFrame(principal_components)    

  def cluster_by_PCA(self, max_clusters = 10, max_iter = 1000, 
                     kmeans_init = None):
    p_init = 'k-means++' if kmeans_init is None else kmeans_init
    inertias = []

    # Creating 10 K-Mean models while varying the number of clusters (k)
    for k in range(2,max_clusters + 1):
      model = KMeans(n_clusters=k, max_iter = max_iter,  init = p_init, random_state = 29)
    
      # Fit model to samples
      model.fit(self.PCA_components.iloc[:,:self.num_pca])
    
      # Append the inertia to the list of inertias
      inertias.append(model.inertia_)
    
    plt.plot(range(2,max_clusters+1), inertias, '-p', color='red')
    plt.xlabel('Número de cluster, k', fontsize=14)
    plt.ylabel('inercia', fontsize=14)
    plt.title('Variación de inercias usando PCA {0} y K-MEANS {1}'.format(self.num_pca, 
                                                                          p_init), 
              fontweight="bold")
    plt.show()  

  def group_by_PCA(self, n_clusters, max_iter = 1000, kmeans_init = None):
    kmeans_init = 'k-means++' if kmeans_init is None else kmeans_init
    model = KMeans(n_clusters=n_clusters, max_iter = max_iter, init = kmeans_init, random_state = 29)
    model.fit(self.PCA_components.iloc[:,:self.num_pca])
    fig, ax = plt.subplots(figsize=(8,8))
    labels = model.predict(self.PCA_components.iloc[:,:self.num_pca])
    scatter = ax.scatter(self.PCA_components[0], self.PCA_components[1], c=labels, cmap="Dark2_r", s=100, alpha=0.9)
    legend1 = ax.legend(*scatter.legend_elements(),
                    loc="best", title="Grupos")
    ax.add_artist(legend1)
    plt.title("Agrupación con reducción dimensional con K-MEANS {}".format(kmeans_init),fontsize=28, fontweight="bold")
    plt.show()
    self.labels = labels

  def get_data_final(self, data_selected, labels):
    self.data_final = data_selected.copy()
    self.data_final['grupo'] = self.labels