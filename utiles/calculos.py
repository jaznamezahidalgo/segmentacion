from sklearn.metrics import silhouette_score, silhouette_samples
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

import matplotlib.cm as cm
import numpy as np
import pandas as pd

def generate_descarted(data : pd.DataFrame, out_file : str, porc : float = 0.1):
    selected = data.query("categoria == 5")
    total = round(selected.shape[0]*(1-porc))
    selected.sample(total)['id'].to_csv('data/' + out_file, index=False)
    return selected.shape[0], total, selected.sample(total)

def calculate_grade(configuration, puntaje):
    """
    Calcula la nota de acuerdo a la fórmula definida
    """
    PUNTAJE_CORTE = configuration.puntaje_corte
    NOTA_MAXIMA = configuration.nota_maxima
    NOTA_MINIMA = configuration.nota_minima
    NOTA_APROBACION = configuration.nota_aprobacion
    PUNTAJE_MAXIMO = configuration.puntaje_maximo
    EXIGENCIA = configuration.exigencia
    if puntaje >= PUNTAJE_CORTE:
        nota = round((NOTA_MAXIMA - NOTA_APROBACION)*(puntaje-PUNTAJE_CORTE)/(PUNTAJE_MAXIMO*(1-EXIGENCIA))+NOTA_APROBACION,1)
    else: 
        nota = round((NOTA_APROBACION - NOTA_MINIMA)*(puntaje/PUNTAJE_CORTE)+NOTA_MINIMA,1)
    return nota

def calculate_category(nota):
    """
    Calcula la categoría de acuerdo a lo definido en los requerimientos
    """
    if nota >= 6.0: categoria = 1
    elif nota >= 5: categoria = 2
    elif nota >= 4: categoria = 3
    elif nota >= 3: categoria = 4
    else: categoria = 5
    return categoria

def evaluate_with_silhoutte(w_pca, model):
    score = silhouette_score(w_pca.PCA_components.iloc[:,:model.num_pca], 
                           model.y_predict, metric="sqeuclidean")
    print("* Model -> {} *".format(model.name))
    print(f"Silhouette Coefficient: {score:.3f} with{model.n_clusters:2d} clusters")
    score = silhouette_score(w_pca.PCA_components.iloc[:,:model.num_pca], model.y_predict)
    print(f"Silhouette Coefficient (metric -> euclidian): {score:.3f} with{model.n_clusters:2d} clusters")

def display_variants(w_pca, n_max_clusters, max_iter = 1000, kmeans_init = None):
  range_n_clusters = range(2, n_max_clusters+1)
  kmeans_init = 'k-means++' if kmeans_init is None else kmeans_init
  for n_clusters in range_n_clusters:
    # Create a subplot with 1 row and 2 columns
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(18, 7)

    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
    ax1.set_xlim([-0.1, 1])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(w_pca.PCA_components.iloc[:,:w_pca.num_pca]) + (n_clusters + 1) * 10])

    # Initialize the clusterer with n_clusters value and a random generator
    # seed of 10 for reproducibility.
    clusterer = KMeans(n_clusters=n_clusters, max_iter = max_iter, init = kmeans_init, random_state=29)
    cluster_labels = clusterer.fit_predict(w_pca.PCA_components.iloc[:,:w_pca.num_pca])

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    silhouette_avg = silhouette_score(w_pca.PCA_components.iloc[:,:w_pca.num_pca], cluster_labels, 
                                      metric="sqeuclidean")
    print(
        "For n_clusters =",
        n_clusters,
        "The average silhouette_score is :",
        silhouette_avg,
    )

    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(w_pca.PCA_components.iloc[:,:w_pca.num_pca], cluster_labels, 
                                                  metric="sqeuclidean")

    y_lower = 10
    for i in range(n_clusters):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / n_clusters)
        ax1.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            ith_cluster_silhouette_values,
            facecolor=color,
            edgecolor=color,
            alpha=0.7,
        )

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    # 2nd Plot showing the actual clusters formed
    colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
    ax2.scatter(
        w_pca.PCA_components[0], w_pca.PCA_components[1], marker=".", s=30, lw=0, alpha=0.7, 
        c=colors, edgecolor="k"
    )

    # Labeling the clusters
    centers = clusterer.cluster_centers_
    # Draw white circles at cluster centers
    ax2.scatter(
        centers[:, 0],
        centers[:, 1],
        marker="o",
        c="white",
        alpha=1,
        s=200,
        edgecolor="k",
    )

    for i, c in enumerate(centers):
        ax2.scatter(c[0], c[1], marker="$%d$" % i, alpha=1, s=50, edgecolor="k")

    ax2.set_title("The visualization of the clustered data.")
    ax2.set_xlabel("Feature space for the 1st feature")
    ax2.set_ylabel("Feature space for the 2nd feature")

    plt.suptitle(
        "Silhouette analysis for KMeans clustering on sample data with n_clusters = %d"
        % n_clusters,
        fontsize=14,
        fontweight="bold",
    )

  plt.show()