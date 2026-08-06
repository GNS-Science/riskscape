import pandas as pd
import matplotlib.pyplot as plt

#
# this is the same code as plot.py except it can be run manually outside of RiskScape
#
def function(rows):
    # turn the RiskScape input rows into a Pandas dataframe
    df = pd.DataFrame(rows)
    # turn the dataframe into a bar_graph
    bar_graph(df, model_output('building-damage-states.png'))

def bar_graph(df, filename):   
    # bar graph plot
    states = ['Light', 'Minor', 'Moderate', 'Severe', 'Collapse']
    total_count = [ sum([ region['count'] for region in df[state] ]) for state in states ]

    plt.bar(states, total_count)
    plt.title('Number of damaged buildings')
    # also add the total count as a label
    for i, y in enumerate(total_count):
        plt.text(i, y, y, ha='center')    
    plt.savefig(filename)

if __name__ == '__main__':
    # note that the results coming out of RiskScape are dict objects
    precanned_results = map(lambda x: { 'count': x }, [41, 115, 79, 70, 1369])
    df = pd.DataFrame(columns=['Light', 'Minor', 'Moderate', 'Severe', 'Collapse'],
                     data=[precanned_results])
    bar_graph(df, 'manual-test.png')
    print('Saved to: manual-test.png')
