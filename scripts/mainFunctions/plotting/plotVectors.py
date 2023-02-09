import geopandas as gpd, os, sys
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import rasterio 
import rasterio.plot
import numpy as np
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(base_dir)
sys.path.append(base_dir + '/mainFunctions/plotting')
from binsDefinition import defineBins

def plot_mapVector(city, evalType, src, exportPath, title, LegendTitle, attr_value, column, districtPath, neighPath, waterPath, 
                           invertArea, streetsPath, addLabels=True):
    """Plot data from vector polygonal datasets using an auxiliary raster to represent water with labels.

    Parameters
    ----------
    src : geopandas.GeoDataFrame
        layer of lower administrative division to be plotted [grid-neighborhood-district-municipality-nuts3]
    districtPath : str
        layer of higher administrative division 
    neigh : geopandas.GeoDataFrame
        layer of lower administrative division [grid-neighborhood-district-municipality-nuts3]
    column : str
        name of column in src_path to be plotted
    evalType : str
        type of evaluation ['mae', 'div']
    title : str
        title of the map
    LegendTitle : str
        titlr of the legend
    waterPath : str
        path to raster layer for water representation
    invertArea : str
        Area outside case study area to represent sth of hide sth
    exportPath : str
         Path to save the map

    Returns
    -------
    image .png

    """
    print(city)
    src['{}'.format(column)].replace(np.inf, 0, inplace=True)
    mean = np.round(src['{}'.format(column)].mean(),2)
    valMax =  np.round(src['{}'.format(column)].max(),2)
    valMin = src['{}'.format(column)].min()
    print(valMax,valMin, mean)
    fig, ax = plt.subplots(figsize=(20, 20),facecolor='white') #50, 50

    cmap, norm, legend_labels = defineBins(evalType, attr_value, valMin, valMax, mean)
    
    # Plot the data                       
    src.plot(column='{}'.format(column), ax=ax, cmap=cmap, norm=norm, edgecolor='#000000',linewidth= 0.0, zorder=1) #norm=norm,
    if os.path.isfile(districtPath) == True :
        srcfile = gpd.read_file(districtPath)
        srcfile.plot(ax=ax, facecolor='none', edgecolor='#000000', linewidth=0.8,  zorder=17 ) #alpha=0.8,
        if addLabels:
            srcfile['coords']= srcfile['geometry'].apply(lambda x: x.representative_point().coords[:])
            srcfile['coords'] = [coords[0] for coords in srcfile['coords']]
            for idx, row in srcfile.iterrows():
                if 'Stadsdeel' in srcfile.columns:
                    plt.annotate(text = row['Stadsdeel'], xy=row['coords'], horizontalalignment= 'center', fontsize=12, zorder=20) 
                elif 'gm_naam' in srcfile.columns:
                    plt.annotate(text = row['gm_naam'], xy=row['coords'], horizontalalignment= 'center', fontsize=12, zorder=20)
                elif 'KOMNAVN' in srcfile.columns:
                    plt.annotate(text = row['KOMNAVN'], xy=row['coords'], horizontalalignment= 'center', fontsize=12, zorder=20)
                elif 'SOGNENAVN' in srcfile.columns:
                    plt.annotate(text = row['SOGNENAVN'], xy=row['coords'], horizontalalignment= 'center', fontsize=12, zorder=20)
                elif 'name' in srcfile.columns:
                    plt.annotate(text = row['name'], xy=row['coords'], horizontalalignment= 'center', fontsize=12, zorder=20)
                else:
                    print("There is no column for labels")

        xlim = ([srcfile.total_bounds[0],  srcfile.total_bounds[2]])
        ylim = ([srcfile.total_bounds[1],  srcfile.total_bounds[3]])
    else:
        xlim = ([src.bounds[0],  src.bounds[2]])
        ylim = ([src.bounds[1],  src.bounds[3]])
    if invertArea:
        outArea= gpd.read_file(invertArea)
        outArea.plot(ax=ax, facecolor='#FFFFFF', edgecolor='#000000', linewidth=.3, zorder=3 )
    if neighPath:
        neighborhoods = gpd.read_file(neighPath)
        neighborhoods.plot(ax=ax, facecolor='none', edgecolor='#000000', linewidth=.3, alpha=0.6, zorder=4 )
    if waterPath:
        waterTif = rasterio.open(waterPath)
        # colors for water layer
        cmapWater = ListedColormap(["#00000000","#7fa9b060" ])
        rasterio.plot.show(waterTif, ax=ax, cmap=cmapWater, zorder=5)
    if streetsPath:
        streets = gpd.read_file(streetsPath).to_crs('EPSG:3035')
        streets.plot(ax=ax, facecolor='none', edgecolor='#000000', linewidth=.5, alpha=0.6, zorder=10)

      
    # Set the plot extent                
    #xlim = ([src.total_bounds[0],  src.total_bounds[2]])
    #ylim = ([src.total_bounds[1],  src.total_bounds[3]])
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    # Add a title
    ax.set_title(title, color="black", fontsize=18)
    # Connect labels and colors, create legend and save the image
    patches = [mpatches.Patch(color=color, label=label)
                for color, label in legend_labels.items()]   
    if city == "ams" :         
        ax.legend(handles=patches,  loc='lower left', facecolor="white", fontsize=12, title = LegendTitle, title_fontsize=14).set_zorder(6)
    else:
        ax.legend(handles=patches,  loc='lower right', facecolor="white", fontsize=12, title = LegendTitle, title_fontsize=14).set_zorder(6)
  
    print("-----PLOTTING IMAGE {}-----".format(title))
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().axes.get_xaxis().set_visible(False)

    plt.savefig(exportPath, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(),transparent=True) #
    #ax.axis('off')
    #plt.show()
    plt.cla()
    plt.close()


