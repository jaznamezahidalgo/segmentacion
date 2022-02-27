import seaborn as sns
import matplotlib.pyplot as plt

class SegmentationResult(object):
  def __init__(self, data, clusters):
    self.data = data
    self.clusters = clusters
    self.data_final = self.data.copy()
    self.data_final['grupo'] = self.clusters
    self.data_final['total'] = 1    

  def __getattr__(self, name: str):
    return object.__getattribute__(name)
    
  def __setattr__(self, name: str, value):
    self.__dict__[name] = value        

  def get_selected_features(self, features_selected = ['id', 'grupo', 'nota']):
    return self.data_final[features_selected]

  def get_clusters(self):
    return self.data_final['grupo'].unique()

  def get_total_by_cluster(self):
    return self.data_final.groupby('grupo')[['total']].sum()  

  def get_metrics_by_cluster(self, columns, metrics):
    return self.data_final.groupby('grupo')[columns].aggregate(metrics)

  def get_summary_cluster(self, cluster, selected):
    return self.data_final[self.data_final.grupo == cluster][selected]   

  def view_outliers(self, column):
    ax = sns.boxplot(x="grupo", y=column, data=self.data_final)
    ax.set_xlabel("Grupo", fontsize=16)
    ax.set_ylabel(column.capitalize(), fontsize=16)
    plt.ylim(min(self.data_final[column])-1, max(self.data_final[column])+1)
    ax.set_title("Dispersión de " + column + " por grupo", fontsize=24, fontweight = "bold")
    plt.show();

  def to_csv(self, unique_file = False, output = 'result.csv'):
    if unique_file:
      self.data_final[['id','nota','grupo']].to_csv(output, index=False)
    else:
      for n_grupo in self.data_final.grupo.unique():
        self.data_final[self.data_final.grupo == n_grupo][['id','nota']].to_csv("Grupo_{}.csv".format(n_grupo), index=False)