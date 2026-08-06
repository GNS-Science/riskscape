import os
import geopandas as gpd
import builtins
from markdown_pdf import MarkdownPdf, Section
# we reuse the main functions from plot.py and choropleth.py here
from plot import function as bar_graph
from choropleth import function  as choropleth_map

def path(name):
    return os.path.join(os.path.dirname(__file__), name)

def make_pdf(df, pdf_fname, bar_graph_filename, choropleth_map_filename):

    # work out some total numbers to insert into the report
    states = ['None', 'Light', 'Minor', 'Moderate', 'Severe', 'Collapsed']
    totals = {}
    total_damaged = 0
    # use 'table' to shuffle around the dataframe structure slightly
    table = df[["Region"] + states].copy()

    for state in states:
        totals[state] = table[state].sum()
        if state != 'None':
            total_damaged += totals[state]

    # replace the {placeholder} values in the template with the actual results
    with open(path('template.md')) as template:
        text = template.read().format(
            total_damaged=total_damaged,
            total_buildings=sum(totals.values()),
            total_collapsed=totals['Collapsed'],
            bar_graph_fname=bar_graph_filename,
            choropleth_map_fname=choropleth_map_filename
        )

    # insert the simplified table of results
    text += "\n" + table.to_markdown(index=False)

    with open(path('style.css')) as file:
        style = file.read()
    pdf = MarkdownPdf()
    pdf.add_section(Section(text), user_css=style)
    pdf.save(pdf_fname)

# RiskScape post-processing-script entry point:
def function(metadata):
    # NB: model_output() is only accessible to the current module's global
    # namespace. But we can also make it available to other python files we
    # import (i.e. plot.py/choropleth.py) by adding it to the builtins
    builtins.model_output = model_output

    # generate the bar graph and choropleth maps for the PDF
    bar_graph_filename = bar_graph(metadata)
    choropleth_map_filename = choropleth_map(metadata)

    # open the regional-impact.geojson file as a geopandas dataframe
    df = gpd.read_file(metadata['outputs']['regional-impact'])

    # generate the PDF
    pdf_filename = model_output('Report-Summary.pdf')
    make_pdf(df, pdf_filename, bar_graph_filename, choropleth_map_filename)


# code to manually run the script outside of RiskScape
if __name__ == '__main__':

    metadata = {
        'parameters': {'choropleth': 'Collapsed'},
        'outputs': {
            'regional-impact': './output/example/regional-impact.geojson',
            'summary': './output/example/summary.csv',
        }
    }

    def model_output(name):
        filepath = "output/example/%s" % name
        print('Writing ' + filepath)
        return filepath

    function(metadata)
