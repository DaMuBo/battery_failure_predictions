import pandas as pd

import functions as fu

from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import Spectral6

def bar_chart(df,x,y,group=None, title="Bar Chart"):
    """
    
    creates a figure for showing in streamlit
    """
    
    data = df
    if group is None:
        source = ColumnDataSource(data)
        p = figure(title=title, x_range=data[x])
        p.vbar(source=source,x=x, top= y, width = 0.9)
        p.xgrid.grid_line_color = None
    else:
        if group == 'klasse':
            colormap = {0:'green',
                        1:'lightgreen',
                        2:'yellow',
                        3:'orange',
                        4:'red'
                       }
        elif group == 'verteilung':
            colormap = {'neutrale Ampere':'grey',
                        'hohe Ampere':'red',
                        'niedrige Ampere':'green'
                       }
        elif group == 'raumtemperatur':
            colormap = {'40':'red',
                        '20-25':'green'
                       }
        elif group == 'randomisiert':
            colormap = {'auf- und entladen':'red',
                        'entladen':'green'
                       }

        data['color'] = [colormap[x] for x in df[group]]

        source = ColumnDataSource(data)
        TOOLTIPS = [(group, f"@{group}")
                   ]
        p = figure(title=title, x_range=data[x], tooltips= TOOLTIPS)
        p.vbar(source=source,x=x, top= y, fill_color='color', width = 0.9)

        p.xgrid.grid_line_color = None
        
    return p
   
    
    
    
def line_chart(df,x,y,group, title="Line Chart"):
    """
    Creates a figure to show a line chart for different lines
    """
    data = df
    liste = set(data['batteryname_'])
    if group == 'klasse':
        colormap = {0:'green',
                    1:'lightgreen',
                    2:'yellow',
                    3:'orange',
                    4:'red'
                   }
    elif group == 'verteilung':
        colormap = {'neutrale Ampere':'grey',
                    'hohe Ampere':'red',
                    'niedrige Ampere':'green'
                   }
    elif group == 'raumtemperatur':
        colormap = {'40':'red',
                    '20-25':'green'
                   }
    elif group == 'randomisiert':
        colormap = {'auf- und entladen':'red',
                    'entladen':'green'
                   }
    
    data['color'] = [colormap[x] for x in df[group]]

    TOOLTIPS = [(group, f"@{group}"),("batteryname","@batteryname_")]
    p = figure(title=title, x_axis_label=x, y_axis_label=y, tooltips=TOOLTIPS)
    for i in liste: 
        color = colormap[data[group][data.batteryname_== i].to_list()[0]]
        source = ColumnDataSource(data[data.batteryname_== i])
        p.line(source=source,x=x, y= y, line_color =color, legend_label=i)
    return p
    
    
    