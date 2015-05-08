import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import offsetbox
from random import randint
from sklearn import (manifold, datasets, decomposition, ensemble, lda,
                     random_projection)

# read from files into X and y
X=[]
y=[]

for i in range(3):
	with open('interest/dump_test_doc.'+str(i), 'r') as XFile:
		for line in XFile:
			X.append([float(x) for x in line.split()])
	with open('interest/dump_test_pred.'+str(i), 'r') as yFile:
		#num_lines = sum(1 for line in yFile)
		for line in yFile:
			y.append(int(line.split()[0]))

political = ['libertarian', 'liberal', 'conservative', 'revolutionary','anarchist' ,  'moderate','tea party', 'progressive']
interest=['technology', 'music','sports',  'gaming']
class_num = len(interest) #20 for news group
print(str(len(X))+'*'+str(len(X[0]))) # X: array of arrays: dump_test_doc
print(len(y)) # y: array of labels: dump_test_pred

#----------------------------------------------------------------------
# Scale and visualize the embedding vectors
def plot_embedding(X, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max+5 - x_min)
    x_mid = (np.max(X, 0) + np.min(X, 0))/2
    print x_mid
    plt.figure()
    ax = plt.subplot(111)
    for i in range(X.shape[0]):
        plt.text(X[i, 0], X[i, 1], str(y[i]), color=plt.cm.Set1(y[i] / float(class_num)), fontdict={'weight': 'bold', 'size': 10})
    plt.xticks([]), plt.yticks([])
    if title is not None:
        plt.title(title)
#----------------------------------------------------------------------
tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
X_tsne = tsne.fit_transform(X)

plot_embedding(X_tsne, "t-SNE embedding of Interest Focused User Classification by MedLDA")

legend_patches=[]
for i in range(class_num):
	legend_patches.append(mpatches.Patch(color=plt.cm.Set1(i / float(class_num)), label=str(i)+':'+interest[i]))
plt.legend(handles=legend_patches, bbox_to_anchor=(0.,-0.09 , 1., .102), loc=3,ncol=4, mode="expand", borderaxespad=0., fontsize = 9)
plt.show()

