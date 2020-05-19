from venv.preparation_functions import dict_into_lists
from matplotlib import pyplot as plt
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, OPTICS
from sklearn.mixture import GaussianMixture
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram
from scipy.interpolate import UnivariateSpline

from scipy.stats.kde import gaussian_kde
from time import time


def principal_component_analysis(sample_set):
    sample_set = np.array(sample_set)[:, [1,2,3,4,5,6]]
    #print(sample_set[0:2])
    print(sample_set)
    X = StandardScaler().fit_transform(sample_set)
    np.set_printoptions(suppress=True, precision=5)
    X = np.transpose(X)
    #print(X[0:10])

    C = np.cov(X)
    eva, eve = np.linalg.eig(C)
    print(C)
    print(eva)
    print(eve)
    Ext = np.matrix.transpose(eve)
    Ncm = np.dot(np.dot(Ext, C), eve)
    print(Ncm)

    X2 = np.transpose(X)
    decomp = PCA(n_components=6)
    principal_components = decomp.fit_transform(X2)
    print(np.shape(principal_components))
    print('Explained variation per principal component: {}'.format(decomp.explained_variance_ratio_))
    principal_components = np.transpose(principal_components)
    pc = [1,2,3,4,5,6]

    plt.bar(pc, decomp.explained_variance_ratio_)
    plt.ylabel("Percentage of variance")
    plt.xlabel("Principal component")
    plt.show()
    '''
    plt.figure()
    plt.figure(figsize=(10, 10))
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=14)
    plt.xlabel('Principal Component - 1', fontsize=20)
    plt.ylabel('Principal Component - 2', fontsize=20)
    plt.scatter(principal_components[0], principal_components[1], alpha=0.1)
    plt.show()
    '''
    return principal_components


def probability_distribution(sample_set):
    s = np.array(sample_set)
    N = len(s)
    n = N//100
    p, x = np.histogram(s, bins=n)
    x = x[:-1] + (x[1] - x[0])/2
    f = UnivariateSpline(x, p, s=n)
    f2 = UnivariateSpline(x, p, s=N)
    plt.plot(x, f(x)/N)
    plt.plot(x, f2(x)/N)
    plt.xlabel("Efficiency")
    plt.ylabel("Probability")
    plt.show()

    #kde = gaussian_kde(s)
    #dist_space = np.linspace(min(s), max(s), 1000)
    #plt.plot(dist_space, kde(dist_space))
    #plt.show()


def kmeans_clustering(sample_set):
    #array = dict_into_lists(sample_set)
    X = np.array(sample_set)
    X = np.transpose(X)

    inertias = []
    clust_num = [3,4,5,6,7,8]
    #for one in clust_num:
    kmeans = KMeans(n_clusters=5, init="k-means++", n_init=20, max_iter=300, precompute_distances="auto", random_state=None, algorithm="auto").fit(X)
    inertias.append(kmeans.inertia_)
    print(kmeans.labels_)
    print(kmeans.n_iter_)
    #print(kmeans.cluster_centers)

    plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_, alpha=0.1)
    plt.xlabel("Principal component 1")
    plt.ylabel("Principal component 2")
    plt.show()
    print(kmeans.inertia_)

    #print(kmeans.labels_)
    #print(kmeans.cluster_centers_)
        #silhouette = silhouette_score(X, kmeans.labels_, sample_size=30000)
        #print("Silhouette: " + str(silhouette))
    '''
    print(inertias)
    plt.plot(clust_num, inertias, ".-")
    plt.xlabel("Number of clusters")
    plt.ylabel("Inertias")
    plt.show()
    '''
    "speed"
    "rpm"
    "consumption"
    "efficiency"
    "sideG"
    "outputPower"
    "fontAcc"
    '''
    fig, four = plt.subplots(2, 2)
    four[0, 0].scatter(X[:, 0], X[:, 1], c=kmeans.labels_, alpha=.1)
    four[0, 0].set_title('speed/rpm')
    four[0, 1].scatter(X[:, 1], X[:, 2], c=kmeans.labels_, alpha=.1)
    four[0, 1].set_title('rpm/consumption')
    four[1, 0].scatter(X[:, 0], X[:, 4], c=kmeans.labels_, alpha=.1)
    four[1, 0].set_title('speed/efficiency')
    four[1, 1].scatter(X[:, 2], X[:, 5], c=kmeans.labels_, alpha=.1)
    four[1, 1].set_title('rpm/efficiency')
    plt.show()
    '''
    #plt.plot(clust_num, inertias, '.-')
    #plt.scatter(X[:, 0], X[:, 1], c=kmeans)
    #plt.show()
    return kmeans


def kmeans_predicting(model, X):
    X = np.array(X)
    X = np.transpose(X)
    model = model.predict(X)
    return model


def agglomerative_clustering(sample_set):

    #print(load_iris().data)

    def plot_dendrogram(model, **kwargs):
        # Create linkage matrix and then plot the dendrogram

        # create the counts of samples under each node
        counts = np.zeros(model.children_.shape[0])
        n_samples = len(model.labels_)
        for i, merge in enumerate(model.children_):
            current_count = 0
            for child_idx in merge:
                if child_idx < n_samples:
                    current_count += 1  # leaf node
                else:
                    current_count += counts[child_idx - n_samples]
            counts[i] = current_count

        linkage_matrix = np.column_stack([model.children_, model.distances_,
                                          counts]).astype(float)

        # Plot the corresponding dendrogram
        dendrogram(linkage_matrix, **kwargs)


    X = np.array(sample_set)

    # setting distance_threshold=0 ensures we compute the full tree.
    model = AgglomerativeClustering(linkage='single', distance_threshold=0, n_clusters=None)

    model = model.fit(X)
    plt.title('Hierarchical Clustering Dendrogram')
    # plot the top three levels of the dendrogram
    plot_dendrogram(model, truncate_mode='level', p=3)
    plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    plt.show()
    print(model.labels_)


def agglomerative_experiment1(matrix_percentages):

    def plot_dendrogram(model, **kwargs):
        # Create linkage matrix and then plot the dendrogram

        # create the counts of samples under each node
        counts = np.zeros(model.children_.shape[0])
        n_samples = len(model.labels_)
        for i, merge in enumerate(model.children_):
            current_count = 0
            for child_idx in merge:
                if child_idx < n_samples:
                    current_count += 1  # leaf node
                else:
                    current_count += counts[child_idx - n_samples]
            counts[i] = current_count

        linkage_matrix = np.column_stack([model.children_, model.distances_,
                                          counts]).astype(float)
        dendrogram(linkage_matrix, **kwargs)


    matrix_percentages = matrix_percentages.astype(np.float64)
    mp = np.transpose(matrix_percentages)
    a = np.array(mp[1:])
    mp = np.transpose(a)
    print(mp)
    #print(principal_components)
    types = ['ward']
    for ty in types:
        clustering = AgglomerativeClustering(linkage=ty, distance_threshold=None, n_clusters=4).fit(mp)
        print(clustering.labels_)
        #labels = clustering.fit_predict(principal_components)
        colormap = {0: "b", 1: "g", 2: "y", 3: "r", 4: "k", 5: "s"}
        #label_color = [colormap[l] for l in clustering.labels_]
        #plt.title("Hierarchical clustering - "+ty)
        #plot_dendrogram(clustering, truncate_mode='level', p=3)
        #plt.show()


    plt.scatter(mp[:, 0], mp[:, 1], c=clustering.labels_)
    plt.show()
    plt.scatter(mp[:, 1], mp[:, 4], c=clustering.labels_)
    plt.show()
    plt.scatter(mp[:, 1], mp[:, 2], c=clustering.labels_)
    plt.show()

    labels = clustering.labels_.reshape(-1,1)
    returnmatrix = np.append(matrix_percentages, labels, axis=1)
    return returnmatrix, labels


def dbscan(principal_components):
    #a = np.array(principal_components[1])
    #b = np.array(principal_components[0])
    #principal_components = np.stack((a, b))
    X = np.transpose(principal_components)
    db = DBSCAN(eps=0.3, min_samples=200).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print('Estimated number of clusters: %d' % n_clusters_)
    print('Estimated number of noise points: %d' % n_noise_)

    plt.scatter(X[:, 0], X[:, 1], c=labels, alpha=.1)
    plt.show()
    plt.scatter(X[:, 1], X[:, 2], c=labels, alpha=.1)
    plt.show()
    plt.scatter(X[:, 0], X[:, 4], c=labels, alpha=.1)
    plt.show()
    plt.scatter(X[:, 1], X[:, 4], c=labels, alpha=.1)
    plt.show()

    # #############################################################################
    # Plot result

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14, alpha=0.1)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6, alpha=0.1)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()


def optics_clustering(principal_components):
    X = np.transpose(principal_components)
    clust = OPTICS(min_samples=500, metric="minkowski")

    # Run the fit
    clust.fit(X)

    plt.scatter(X[:, 0], X[:, 1], c=clust.labels_, alpha=0.1)
    plt.show()
    plt.scatter(X[:, 1], X[:, 4], c=clust.labels_, alpha=0.1)
    plt.show()
    plt.scatter(X[:, 1], X[:, 2], c=clust.labels_, alpha=0.1)
    plt.show()


def gaussian_mix(principal_components):
    X = np.transpose(principal_components)
    mix = GaussianMixture(n_components=7, covariance_type="full")
    mix.fit(X)
    plt.scatter(X[:, 0], X[:, 1], c=mix.labels_, alpha=0.1)
    plt.show()
    plt.scatter(X[:, 1], X[:, 4], c=mix.labels_, alpha=0.1)
    plt.show()
    plt.scatter(X[:, 1], X[:, 2], c=mix.labels_, alpha=0.1)
    plt.show()