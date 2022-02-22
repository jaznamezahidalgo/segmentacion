import matplotlib.pyplot as plt
import seaborn as sns

class Visualize:
    def __init__(self, data_frame) :
        self.data_frame = data_frame

    def view_histogram(self, n_items, title):
        lst_feature = []
        for n_item in range(1, n_items + 1):
            lst_feature.append('i' + str(n_item))
        fig, ax = plt.subplots(2, 4, figsize=(20, 10))
        fig.suptitle(title, fontsize=28)
        row, col = 0, 0
        for feature in lst_feature:  
            sns.histplot(self.data_frame[feature], ax=ax[row][col], kde=True) 
            col += 1
            row += 0 if col < 4 else 1
            col = 0 if col > 3 else col
        plt.show()

    def view_histogram_by_column(self, column, title):
        try:
            sns.set(style='whitegrid')
            f, ax = plt.subplots(1,1, figsize=(6, 4))
            ax = sns.histplot(self.data_frame[column], kde = True, color = 'c')
            plt.title(title, fontsize = 18, fontweight="bold")
            plt.xlabel(column.capitalize())
            plt.ylabel("Densidad")
            plt.show();
        except KeyError:
            print("Problema para visualizar gráfico")  

    def count_by_column(self, column):
        return self.data_frame.groupby(column).size()

    def view_outliers(self, column, title):
        ax = sns.boxplot(y=column, data=self.data_frame)
        plt.suptitle(title, fontsize = 18, fontweight="bold");  

    def view_items(self, n_items, title):
        lst_feature = []
        for n_item in range(1, n_items + 1):
            lst_feature.append('i' + str(n_item))
        fig, ax = plt.subplots(2, 4, figsize=(20, 10))
        fig.suptitle(title, fontsize=28)
        row, col = 0, 0
        for feature in lst_feature:  
            sns.boxplot(y=self.data_frame[feature], ax=ax[row][col], 
                data=self.data_frame, color="r")
            col += 1
            row += 0 if col < 4 else 1
            col = 0 if col > 3 else col
        plt.show()  

    def view_distribution(self, hue, features):
        sns.pairplot(self.data_frame, hue=hue, height=4, vars=features, kind='scatter');