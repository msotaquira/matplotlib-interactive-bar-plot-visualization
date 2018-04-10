import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mpl

# Function definitions

def line_select_callback(eclick, erelease):
    '''For box interaction'''

    # Maintain width of the interactive box
    RS.extents = (xmin,xmax,RS.extents[2],RS.extents[3])

    # Check if error bars are inside the interactive box and change
    # bar colors correspondingly
    color_values = compare_bars_to_ranges(RS.extents,errors_max,errors_min)
    color_bars_based_on_values(the_bars,color_values,palette)
    
def color_bars_based_on_values(the_bars,color_values,palette):
    for i in range(len(the_bars)):
        color = palette[color_values[i]]
        the_bars[i].set_color(color)

def compare_bars_to_ranges(extents,errors_max,errors_min):
    # Parse extents
    ymin = extents[2]
    ymax = extents[3]

    # Comparison
    nbars = errors_max.shape[0]
    color_values = [0.0]*nbars
    for bar in range(nbars):
        bar_min = errors_min.iloc[bar]
        bar_max = errors_max.iloc[bar]

        if (ymax<bar_min) | (ymin>bar_max) : color_values[bar] = 0.0
        if (ymax>bar_max) & (ymin<bar_min): color_values[bar] = 1.0
        if (ymax>=bar_min) & (ymax<=bar_max) & (ymin<=bar_min):
            color_values[bar] = round( (ymax-bar_min)/(bar_max-bar_min),1 )
        if (ymax>=bar_min) & (ymax<=bar_max) & (ymin>bar_min) & (ymin<=bar_max):
            color_values[bar] = round( (ymax-ymin)/(bar_max-bar_min),1 )
        if (ymax>bar_max) & (ymin>bar_min) & (ymin<=bar_max):
            color_values[bar] = round( (bar_max-ymin)/(bar_max-bar_min),1 )

    return color_values

# Create the dataset
np.random.seed(12345)
df = pd.DataFrame([np.random.normal(150000,8200,3650), 
                   np.random.normal(100000,9300,3650), 
                   np.random.normal(140000,9350,3650), 
                   np.random.normal(70000,9800,3650)], 
                  index=[1992,1993,1994,1995])

# The color palette
keys = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
values = [[253,240,240], [251,212,211], [249,184,181], [246,155,152], [244,127,123], 
           [242,99,94], [199,82,77], [155,64,60], [110,45,43], [66,27,26], [44,18,18]]
values = [ tuple([element/255.0 for element in color]) for color in values]
palette = dict(zip(keys,values))

# Initial bar plots with error bars (95% CI = +- 1.96*std)
width = 0.5
means = df.apply(np.mean,axis=1)
errors = 1.96*df.apply(np.std,axis=1)
errors_max = means + errors
errors_min = means - errors
fig, ax = plt.subplots()
the_bars = ax.bar(df.index, means, width,yerr=errors,ecolor='k',capsize=5)
plt.xticks(df.index,df.index.map(str))

# The colorbar
cmap_name = 'custom_colormap'
n_bins = len(values)-1
cm = LinearSegmentedColormap.from_list(cmap_name,values,N=n_bins)

ax_colorbar = fig.add_axes([0.92, 0.25, 0.03, 0.5])
cb = mpl.colorbar.ColorbarBase(ax_colorbar, cmap=cm, orientation='vertical')

# The interactive box
RS = RectangleSelector(ax, line_select_callback,
                       drawtype='box', useblit=False,
                       button=[1],  # don't use middle button
                       minspanx=5, minspany=5,
                       spancoords='pixels',
                       interactive=True, 
                       rectprops=dict(alpha=0.5,color='gray'))

ymaxvalues = means + errors
yminvalues = means - errors
xmin, xmax = ax.get_xbound()
ymin, ymax = np.min(yminvalues), np.max(ymaxvalues)

RS.to_draw.set_visible(True)
RS.extents = (xmin,xmax,ymin,ymax)

# Initial coloring
color_values = compare_bars_to_ranges(RS.extents,errors_max,errors_min)
color_bars_based_on_values(the_bars,color_values,palette)

plt.show()



