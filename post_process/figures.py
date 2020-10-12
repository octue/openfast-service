import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io
import json


def create_figure_file(analysis, results):
    """ Saves json file constructed from some analysis results. The json will be used later to create a figure.
        File can be saved to an arbitrary location, but by default is saved to the current directory
        The results expected to contain following dictionary {Airfoil_name: [AoA, Cl, Cd, Cm, Cp]}
    """

    for airfoil in results:
        figure = plot_result(airfoil, results[airfoil])
        name = analysis.output_dir + '/' + airfoil + '.json'
        with open(name, 'w') as outfile:
            plotly.io.write_json(figure, outfile, pretty=True)
    return


def plot_result(airfoil, result):
    # You can use the Plotly python sdk to construct figures, by adding it to requirements.txt
    # For examples https://plotly.com/python/

    fig = make_subplots(rows=2, cols=1,
                        subplot_titles=("Cl", "Cd"))  # Inititalize figure object

    fig.add_trace(go.Scatter(x=result[0].tolist(), y=result[1].tolist(),
                             mode='lines+markers',
                             name="Cl"),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=result[0].tolist(), y=result[2].tolist(),
                             mode='lines+markers',
                             name="Cd"),
                  row=2, col=1)
    fig.update_xaxes(title_text='Angle of Attack', row=2, col=1)
    fig.update_yaxes(title_text='CL', row=1, col=1)
    fig.update_yaxes(title_text='CL', row=2, col=1)
    fig.update_layout(title_text='Lift and Drag coefficients for ' + airfoil + ' airfoil',
                      plot_bgcolor='white')

    # At the same time, any plotly compliant dict or list that can be converted to json.
    # For examples and options https://chart-studio.plotly.com/create/
    '''
    fig = {"data": [
        {
            "x": ["giraffes", "orangutans", "monkeys"],
            "y": [20, 14, 23],
            "type": "bar"
        }
    ]
    }
    name = analysis.output_dir + '/figure_name.json'
    # Dump the dict to a plain text json file. Note that for more advanced data (e.g. including numpy arrays etc) you
    # may wish to use the serialiser provided with the plotly library
    with open(name, 'w') as outfile:
        json.dump(fig, outfile)
    '''

    return fig

# You can either do this here, or in your main run() function definition (or basically anywhere else you like)...
# but you need to add the created file (which is part of the analysis results) to the output results manifest. In
# this case we do it here, which has the advantage of keeping file creation and manifesting together; but has the
# disadvantage of needing to modify your code to pass the analysis around. If you're unable to alter the API of your
# code; no problem - just do all your manifest creation separately (e.g. at the end of the run function)
#fig_data = {'name': name,
#            'short_caption': 'A shortened caption',
#            'caption': 'A longer caption, perhaps including some description of why on earth we'
#                       ' would want to see a bar chart of different zoo animals'}
# TODO add_to_manifest('figure', name, fig_data)
