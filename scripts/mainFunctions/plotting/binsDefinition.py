import numpy as np
import matplotlib.colors as colors
from matplotlib.colors import ListedColormap

def defineBins(evalType, attr_value, valMin, valMax, mean): #
    if evalType == "popdistribution":
        bins = 7
        colors_palette = ["#f1eef600","#fc9ca2","#e66778", "#fa324d", "#b51d31", "#992636", "#631b25"] #graduate of red
        #colors_palette = ["#f1eef600","#ffffb2","#ffd76d", "#fea649", "#f86c30", "#e62f21", "#bd0026"] #graduate of orange
        if attr_value == 'totalpop' or attr_value == 'POL' or attr_value == 'TOTALPOP' or attr_value == 'NLD':
            if valMax > 250:
                a = [0, 1, 50, 100, 150, 200, 250, valMax]
            else:
                a = [0, 1, 50, 100, 150, 200, 250, 300]
        else:
            if valMax<50:
                a=[valMin, 1, 10, 20, 30, 40, 50, 100]
            else:
                a=[valMin, 1, 10, 20, 30, 40, 50, valMax]

        cmap = ListedColormap(colors_palette)
        norm = colors.BoundaryNorm(a, bins) 
          
        # Add a legend for labels
        legend_labels = { colors_palette[1]: "{0}-{1}".format(a[1], a[2]), 
        colors_palette[2]: "{0}-{1}".format(a[2],a[3]), colors_palette[3]: "{0}-{1}".format(a[3],a[4]),
        colors_palette[4]: "{0}-{1}".format(a[4],a[5]), colors_palette[5]: "{0}-{1}".format(a[5],a[6]), 
        colors_palette[6]: "{0}-{1}".format(a[6],a[7])}
    elif evalType == "popdistributionPred":
        bins = 7
        colors_palette = ["#f1eef600","#ffffb2","#ffd76d", "#fea649", "#f86c30", "#e62f21","#bd0026"] #graduate of orange
        if valMax < 250:
            a=[valMin,1, 25, 50, 75, 100, 150, 250]
        else:
            a=[valMin, 1, 50, 100, 200, 300, 400, 500]
            #a=[valMin,1, 25, 50, 75, 100, 150, valMax]
        cmap = ListedColormap(colors_palette)
        norm = colors.BoundaryNorm(a, bins)  
        # Add a legend for labels
        legend_labels = { colors_palette[1]: "{0}-{1}".format(a[1], a[2]), 
        colors_palette[2]: "{0}-{1}".format(a[2],a[3]), colors_palette[3]: "{0}-{1}".format(a[3],a[4]),
        colors_palette[4]: "{0}-{1}".format(a[4],a[5]), colors_palette[5]: "{0}-{1}".format(a[5],a[6]), 
        colors_palette[6]: "{0}-{1}".format(a[6],a[7])}
    elif evalType == "popdistributionPolyg":
        bins = 7
        if valMin <= valMax <= 7500:
            a=[valMin, 1, 500, 1500, 3000, 4500, 6000, 7500]
        else:
            a=[valMin, 1, 500, 1500, 3000, 4500, 6000, valMax]
        cmap = ListedColormap(["#f1eef600","#e0c8e2","#da9acb", "#df65b0", "#de348a", "#c61266","#980043"])
        norm = colors.BoundaryNorm(a, bins)  
        # Add a legend for labels
        legend_labels = { "#e0c8e2": "{0}-{1}".format(int(a[1]), int(a[2])), "#da9acb": "{0}-{1}".format(int(a[2]),int(a[3])), 
        "#df65b0": "{0}-{1}".format(int(a[3]),int(a[4])),
        "#de348a": "{0}-{1}".format(int(a[4]),int(a[5])), "#c61266": "{0}-{1}".format(int(a[5]),int(a[6])), 
        "#980043": "{0}-{1}".format(int(a[6]),valMax), "#2b83ba00": "mean total:{}".format(mean)}
    
    elif evalType == "mae":
        bins = 7
        colors_palette = ["#d7191c","#f17c4a","#fec980", "#ffffbf", "#c7e9ad", "#80bfac","#2b83ba"]
        if -50<=valMin:
            a=[-50, -25, -10, -2, 2, 10, 25, valMax]
        elif valMax<=50:
            a=[valMin, -25, -10, -2, 2, 10, 25, 50]
        else:
            a=[valMin,-25, -10, -2, 2, 10, 25, valMax]

        cmap = ListedColormap(colors_palette)
        norm = colors.BoundaryNorm(a, bins)  
        # Add a legend for labels
        legend_labels = { colors_palette[0]: "<{1}".format(a[0],a[1]), colors_palette[1]: "{0}-{1}".format(a[1], a[2]), 
        colors_palette[2]: "{0}-{1}".format(a[2],a[3]), colors_palette[3]: "{0}-{1}".format(a[3],a[4]),
        colors_palette[4]: "{0}-{1}".format(a[4],a[5]), colors_palette[5]: "{0}-{1}".format(a[5],a[6]), 
        colors_palette[6]: ">{1}".format(a[6],a[7])}
         
    elif evalType == "pe":
        bins = 7
        colors_palette = ["#d7191c00","#fff5f0", "#fdccb8", "#fc8f6f", "#f44d37","#c5161b","#67000d"]
        a=[0, 1, 20, 40, 60, 80, 100]
        cmap = ListedColormap(colors_palette)
        norm = colors.BoundaryNorm(a, bins)  
        # Add a legend for labels
        legend_labels = { colors_palette[0]: "{0}-{1}".format(a[0],a[1]), colors_palette[1]: "{0}-{1}".format(a[1], a[2]), 
        colors_palette[2]: "{0}-{1}".format(a[2],a[3]), colors_palette[3]: "{0}-{1}".format(a[3],a[4]),
        colors_palette[4]: "{0}-{1}".format(a[4],a[5]), colors_palette[5]: "{0}-{1}".format(a[5],a[6]), 
        colors_palette[6]: "{0}<".format(a[6])}
    
    elif evalType == "ree":
        bins = 7
        colors_palette = ['#d7191c','#f17c4a','#fec980','#ffffbf','#c7e9ad','#80bfac','#2b83ba']
        a=[valMin, -50, -25, -5, 5, 25, 50, valMax]
        cmap = ListedColormap(colors_palette)
        norm = colors.BoundaryNorm(a, bins)  
        # Add a legend for labels
        legend_labels = { colors_palette[0]: "<{1}".format(a[0],a[1]), colors_palette[1]: "{0}-{1}".format(a[1], a[2]), 
        colors_palette[2]: "{0}-{1}".format(a[2],a[3]), colors_palette[3]: "{0}-{1}".format(a[3],a[4]),
        colors_palette[4]: "{0}-{1}".format(a[4],a[5]), colors_palette[5]: "{0}-{1}".format(a[5],a[6]), 
        colors_palette[6]: ">{0}".format(a[6])}

    elif evalType == "dif_KNN":
        # Light green to purple 
        print('----', valMin, valMax)
        bins = 7
        colors_palette = ["#386641","#6a994e","#a7c957", "#f2e8cf50", "#ff6f59", "#db504a","#bc4749"]
        a=[-8, -5, -3, -1, 1, 3, 5, 8] #a=[valMin,-15, -10, -5, 5, 10, 15,valMax]
        cmap = ListedColormap(colors_palette)
        norm = colors.BoundaryNorm(a, bins)  
        # Add a legend for labels
        legend_labels = { colors_palette[0]: "{0}-{1}".format(a[0], a[1]), colors_palette[1]: "{0}-{1}".format(a[1], a[2]), 
        colors_palette[2]: "{0}-{1}".format(a[2],a[3]), colors_palette[3]: "{0}-{1}".format(a[3],a[4]),
        colors_palette[4]: "{0}-{1}".format(a[4],a[5]), colors_palette[5]: "{0}-{1}".format(a[5],a[6]), 
        colors_palette[6]: "{0}-{1}".format(a[6],a[7])}
    
    elif evalType == "KNN":
        # Light green to green 
        print('----', valMin, valMax)
        bins = 7
        colors_palette = ["#a1cca5" ,"#8fb996", "#709775","#415d43","#111d13"]
        a=[0, 1, 3, 5, 7, 8] 
        cmap = ListedColormap(colors_palette)
        norm = colors.BoundaryNorm(a, bins)  
        # Add a legend for labels
        legend_labels = { colors_palette[0]: "< {1}".format(a[0], a[1]), colors_palette[1]: "{0}-{1}".format(a[1], a[2]), 
        colors_palette[2]: "{0}-{1}".format(a[2],a[3]), colors_palette[3]: "{0}-{1}".format(a[3],a[4]),
        colors_palette[4]: "{0}-{1}".format(a[4],a[5])}
    
    elif evalType == "diss":
        # Light blue (vivid sky blue) to flickr pink 
        bins = 7
        colors_palette = ["#4CC9F0","#4361EE","#3A0CA3", "#560BAD", "#7209B7", "#B5179E","#F72585"]
        a=[0.00, 0.10, 0.30, 0.45, 0.55, 0.70, 0.9, 1.0] #a=[valMin,-15, -10, -5, 5, 10, 15,valMax]
        cmap = ListedColormap(colors_palette)
        norm = colors.BoundaryNorm(a, bins)  
        # Add a legend for labels
        
        legend_labels = { colors_palette[0]: "<{1}".format(a[0], a[1]), colors_palette[1]: "{0}-{1}".format(a[1], a[2]), 
        colors_palette[2]: "{0}-{1}".format(a[2],a[3]), colors_palette[3]: "{0}-{1}".format(a[3],a[4]),
        colors_palette[4]: "{0}-{1}".format(a[4],a[5]), colors_palette[5]: "{0}-{1}".format(a[5],a[6]), 
        colors_palette[6]: ">{0}".format(a[6],a[7])}

    elif evalType == "rdi":
        # Light green to purple 
        bins = 7
        colors_palette = ["#13f644","#2ccf63","#45a782", "#5e80a2", "#7759c1", "#9031e0","#a90aff"]
        
        a=[0.00, 0.10, 0.30, 0.45, 0.55, 0.70, 0.9, 1.0] #a=[valMin,-15, -10, -5, 5, 10, 15,valMax]
        
        cmap = ListedColormap(colors_palette)
        norm = colors.BoundaryNorm(a, bins)  
        # Add a legend for labels
        
        legend_labels = { colors_palette[0]: "<{1}".format(a[0], a[1]), colors_palette[1]: "{0}-{1}".format(a[1], a[2]), 
        colors_palette[2]: "{0}-{1}".format(a[2],a[3]), colors_palette[3]: "{0}-{1}".format(a[3],a[4]),
        colors_palette[4]: "{0}-{1}".format(a[4],a[5]), colors_palette[5]: "{0}-{1}".format(a[5],a[6]), 
        colors_palette[6]: ">{0}".format(a[6],a[7])}

    else:
        bins = 7
        hist=np.asarray(np.histogram([valMin,valMax], bins=bins, density=True))
        a = hist[1]
        cmap = ListedColormap(["#d7191c","#f17c4a","#fec980", "#ffffbf", "#c7e9ad", "#80bfac","#2b83ba"])
        norm = colors.BoundaryNorm(a, bins)  
        # Add a legend for labels
        legend_labels = { "#d7191c": "{0}-{1}".format(valMin, round(a[1],2)), "#f17c4a": "{0}-{1}".format(round(a[1],2), round(a[2],2)), "#fec980": "{0}-{1}".format(round(a[2],2),round(a[3],2)), 
        "#ffffbf": "{0}-{1}".format(round(a[3],2),round(a[4],2)),
        "#c7e9ad": "{0}-{1}".format(round(a[4],2),round(a[5],2)), "#80bfac": "{0}-{1}".format(round(a[5],2),round(a[6],2)), 
        "#2b83ba": "{0}-{1}".format(round(a[6],2),valMax), "#2b83ba00": "mean total:{}".format(mean)}
            
    return cmap, norm, legend_labels