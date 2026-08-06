import matplotlib.pyplot as plt
import pandas as pd

def bar_graph(df, filename):
    # bar graph plot
    states = ['Light', 'Minor', 'Moderate', 'Severe', 'Collapsed']
    total_count = [ sum([ region for region in df[state] ]) for state in states ]

    plt.bar(states, total_count)
    plt.title('Number of damaged buildings')
    # also add the total count as a label
    for i, y in enumerate(total_count):
        plt.text(i, y, y, ha='center')
    plt.savefig(filename)

# RiskScape post-processing-script entry point:
def function(metadata):
    # RiskScape passes us the output filepaths as a Python dictionary
    outputs = metadata['outputs']

    # open the summary.csv file as a pandas dataframe
    df = pd.read_csv(outputs['summary'])

    plot_filename = model_output('building-damage-states.png')

    # use matplotlib to turn the dataframe into a bar graph
    bar_graph(df, plot_filename)
    return plot_filename
    
