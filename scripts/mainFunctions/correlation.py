import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np, pandas as pd
def calc_cor(js, cor_path, year, selectList, selection, title):
    # Load data
    frame = pd.DataFrame(js, columns=selectList)
    cor = frame.corr(method='pearson')
    cor = cor.replace(np.nan, 0)

    #dfTOxls(dest_path, fileName, cor)
    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(cor, dtype=bool))
    
    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(cor, annot=True, mask=mask, cmap=cmap, center=0,
                square=True, linewidths=.5, annot_kws={"fontsize":6}, cbar_kws={"shrink": .5})  

    plt.title("{1}, {0}".format(year, title),fontsize=10)
    plt.xlabel("Layers", fontsize=8)
    plt.ylabel("Layers", fontsize=8)
    plt.xticks(fontsize=5, rotation=45, ha="right")
    plt.yticks(fontsize=5, rotation=0)
    plt.savefig(cor_path + "/{0}_corMatrix_{1}.png".format(year,selection), dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(),transparent=True)
    plt.cla()
    plt.close() 