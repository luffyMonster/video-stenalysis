import matplotlib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def train_and_test(data_file):
    test_size = 38
    df = pd.read_csv(data_file)
    df.head()

    y = df['label'].values
    X = df.drop(['label', 'image_name'], axis=1).values

    x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=42)

    X0 = X[y == 0, :]
    print("Sample of frame cover\n", X0)

    X1 = X[y == 1, :]
    print("Sample of frame stego\n", X1)

    print("Training size: %d" % len(y_train))
    print("Test size    : %d" % len(y_test))

    n_neighbors = 3
    clf = neighbors.KNeighborsClassifier(n_neighbors, p=2)
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)

    print("Predicted labels: ", y_pred[:])
    print("Ground truth    : ", y_test[:])



    fig = plt.figure()
    ax = Axes3D(fig)

    ent_values = df["entropy"].values
    kur_values = df["kurtosis"].values
    per_values = df["percentile"].values

    # ent_values = x_train[:, 0]
    # kur_values = x_train[:, 1]
    # per_values = x_train[:, 2]


    # Create color maps
    #cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA'])
    # cmap_bold = ListedColormap(['blue', 'red'])

    # ax.scatter(ent_values, per_values, kur_values, c=y, cmap=cmap_bold)
    #
    ax.set_xlabel('Kurtosis')
    ax.set_ylabel('Entropy')
    ax.set_zlabel('Percentile')

    cdict = {0: 'blue', 1: 'red'}
    for g in np.unique(y):
        ix = np.where(y == g)
        ax.scatter(kur_values[ix], ent_values[ix], per_values[ix], c=cdict[g], label=('cover', 'stego')[g==1])

    ax.legend()
    plt.show()


