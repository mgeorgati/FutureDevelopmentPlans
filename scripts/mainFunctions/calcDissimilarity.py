import geopandas as gpd, os,sys, numpy as np 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/mainFunctions/')
from plotting.plotVectors import plot_mapVector

def calcDissimilarity(srcPath, dissimFile, year, selection, totalpop, city, districtPath, neighPath, streetsPath, waterPath, invertArea):
    df = gpd.read_file(srcPath, driver='GPKG',crs="EPSG:3035")
    for col in df.columns:
        if col != 'geometry':
            print(col)
            df[col] = df[col].replace(np.nan, 0)
    print(df.head())
    for k in selection:
        if k !=  totalpop:
            df['restPop'] = df['{}'.format(totalpop)] - df['{}'.format(k)]
            df['D_{}'.format(k)] = 0.5 * np.sum((np.absolute((df['{}'.format(k)]/df['{}'.format(k)].sum()) - (df['restPop']/df['restPop'].sum()))))
            d90 = round(df['D_{}'.format(k)].mean(), 4)

            if os.path.exists(dissimFile):
                with open(dissimFile, 'a') as myfile:
                    myfile.write(str(year) + ';' + k + ';' + str(d90) + '\n')       
            else:
                with open(dissimFile , 'w+') as myfile:
                    myfile.write('Dissimilarity Measures in Amsterdam \n')
                    myfile.write('Region of Origin;{}\n'.format(year))
                    myfile.write(str(year) + ';' + k + ';' + str(d90) + '\n')

        title90 ="Dissimilarity Index in Amsterdam\n({0})({1})".format(k, year)
        LegendTitle = "Dissimilarity"
        exportPath90 = "C:/Users/NM12LQ/OneDrive - Aalborg Universitet/MeasuringSegregation/Amsterdam/dissimilarity/{2}_dissimilarity_{1}.png".format(city, k, year)
        #plot_mapVector(city, 'diss', df, exportPath90, title90, LegendTitle,k, 'D_{}'.format(k), districtPath = districtPath, neighPath = neighPath, streetsPath = streetsPath, waterPath = waterPath, invertArea =  invertArea, addLabels=True)
    
    #src_file = "C:/Users/NM12LQ/OneDrive - Aalborg Universitet/MeasuringSegregation/Amsterdam/dissimilarity/{0}_dissimilarity.gpkg".format(year)
    #df.to_file(src_file, driver='GPKG',crs="EPSG:3035")


