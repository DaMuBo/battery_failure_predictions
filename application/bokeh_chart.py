from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import Spectral6


def bar_chart(df,x,y,group, title="Bar Chart"):
    """
    
    creates a figure for showing in streamlit
    """
    
    data = df
    colormap = {0:'green',
                1:'lightgreen',
                2:'yellow',
                3:'orange',
                4:'red'
               }
    data['color'] = [colormap[x] for x in df[group]]
    source = ColumnDataSource(data)

    p = figure(title=title, x_range=data[x])
    p.vbar(source=source,x=x, top= y, fill_color='color')
    
    return p
    
    
    