import matplotlib.pyplot as plt
import geopandas as gpd

def choropleth_map(gdf, filename, column):

    ax = gdf.plot(column=column, cmap='Reds', legend=True)
    # labels
    gdf.apply(lambda x: ax.annotate(text=x['Region'], xy=x.geometry.centroid.coords[0], ha='center', size=5), axis=1)
    ax.set_axis_off()
    ax.set_title(column + ' buildings in Upolu by region')
    plt.savefig(filename)

    return filename

# RiskScape post-processing-script entry point:
def function(metadata):
    # RiskScape passes us the output filepaths as a Python dictionary
    outputs = metadata['outputs']

    # open the regional-impact.geojson file as a geopandas dataframe
    df = gpd.read_file(outputs['regional-impact'])

    # get the value specified for the choropleth model parameter.
    # This lets us control which column in the output to plot dynamically
    column = metadata['parameters']['choropleth']

    # we can even change the file that gets produced dynamically to match the column name
    output_filename = model_output('regional-%s-buildings.png' % column.lower())

    # use matplotlib to turn the dataframe into a choropleth plot
    choropleth_map(df, output_filename, column)
    return output_filename

