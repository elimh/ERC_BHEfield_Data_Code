import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.transforms import ScaledTranslation
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

class ERC_Management:
    """
    ERC_Management_alt class manages the color codes and IDs for different vaults and provides
    methods to generate ID strings and create color dictionaries for plotting purposes.

    Attributes:
        blues (list): A list of blue color codes.
        west_ids (list): A list of IDs corresponding to the blue color codes.
        browns (list): A list of brown color codes.
        south_ids (list): A list of IDs corresponding to the brown color codes.
        greens (list): A list of green color codes.
        east_ids (list): A list of IDs corresponding to the green color codes.
    """

    def __init__(self) -> None:
        """
        Initializes the ERC_Management class with predefined color codes and their corresponding borehole IDs.
        """
        # Initialize the list of blue color codes
        self.blues = [
            '#4169E1', '#0047AB', '#89CFF0', '#0000FF', '#7393B3', '#0096FF',
            '#00FFFF', '#6495ED', '#6F8FAF', '#6082B6', '#5D3FD3', '#ADD8E6',
            '#191970'
        ]

        # Initialize the list of IDs corresponding to the blue color codes
        self.west_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        # Initialize the list of brown color codes
        self.browns = [
            '#E1C16E', '#CD7F32', '#A52A2A', '#F5DEB3', '#DAA06D', '#800020',
            '#6E260E', '#C19A6B', '#D27D2D', '#E97451', '#6F4E37', '#5C4033',
            '#988558', '#C2B280', '#C19A6B', '#C04000', '#A95C68', '#483C32'
        ]

        # Initialize the list of IDs corresponding to the brown color codes
        self.south_ids = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25]

        # Initialize the list of green color codes
        self.greens = [
            '#097969', '#AFE1AF', '#E4D00A', '#50C878', '#5F8575', '#4F7942',
            '#228B22', '#7CFC00', '#008000', '#355E3B', '#00A36C', '#90EE90',
            '#32CD32', '#8A9A5B', '#98FB98', '#93C572'
        ]

        # Initialize the list of IDs corresponding to the green color codes
        self.east_ids = [
            23, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40
        ]

    def generate_vault_id_strings(self, probe_strings=True, before='Probe_', after='_T_in'):
        """
        Generate three lists of formatted ID strings based on predefined identifiers for west, south, and east vaults. The identifiers are combined with the provided prefixes and suffixes to create the final ID strings.

        Args:
            probe_strings (bool): Flag to include 'before' and 'after' strings in the IDs.
            before (str): String to prefix each ID.
            after (str): String to suffix each ID.

        Returns:
            tuple: A tuple containing three lists of formatted ID strings:
                - west (list of str): Formatted ID strings for the west vault.
                - south (list of str): Formatted ID strings for the south vault.
                - east (list of str): Formatted ID strings for the east vault.
        """

        # Generate ID strings for the west vault
        if probe_strings:
            west = [f'{before}{x:02}{after}' for x in self.west_ids]
            south = [f'{before}{x:02}{after}' for x in self.south_ids]
            east = [f'{before}{x:02}{after}' for x in self.east_ids]
        else:
            west = [f'{x:02}' for x in self.west_ids]
            south = [f'{x:02}' for x in self.south_ids]
            east = [f'{x:02}' for x in self.east_ids]

        return west, south, east

    def create_colordict(self, probe_strings=True, before='Probe_', after='_T_in'):
        """
        Creates a dictionary mapping ID strings to color codes for each vault.

        Args:
            probe_strings (bool): Flag to include 'before' and 'after' strings in the IDs.
            before (str): String to prefix each ID.
            after (str): String to suffix each ID.

        Returns:
            dict: A dictionary mapping ID strings to color codes.
        """
        # Generate ID strings for each vault
        west, south, east = self.generate_vault_id_strings(probe_strings=probe_strings, before=before, after=after)

        # Map west vault ID strings to blue color codes
        self.colors_west = dict(zip(west, self.blues[:len(west)]))

        # Map south vault ID strings to brown color codes
        self.colors_south = dict(zip(south, self.browns[:len(south)]))

        # Map east vault ID strings to green color codes
        self.colors_east = dict(zip(east, self.greens[:len(east)]))

        # Combine all mappings into a single dictionary
        self.colors_all = {**self.colors_west, **self.colors_south, **self.colors_east}

        return self.colors_all

    def set_plot_params(self):
        """
        Sets the plotting parameters for matplotlib to ensure consistent styling.
        """
        # Set font type for PDF and PS outputs
        matplotlib.rcParams['pdf.fonttype'] = 42
        matplotlib.rcParams['ps.fonttype'] = 42

        # Set figure save parameters
        plt.rcParams['savefig.bbox'] = 'tight'
        plt.rcParams['savefig.pad_inches'] = 0.01

        # Set font family and size parameters
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial']
        plt.rcParams['axes.labelsize'] = 7
        plt.rcParams['ytick.labelsize'] = 7
        plt.rcParams['xtick.labelsize'] = 7
        plt.rcParams['legend.fontsize'] = 7
        plt.rcParams['font.size'] = 7
        plt.rcParams['ytick.minor.visible'] = True

        # Set math text font
        plt.rcParams['mathtext.fontset'] = "dejavusans"

def get_colordict(probe_strings=True, before='Probe_', after='_T_in'):
    """
    Generate a dictionary mapping color identifiers for probes.

    This function utilizes the ERC_Management class to create a color dictionary 
    based on specified probe string patterns. The function allows customization 
    of the prefix and suffix that surround the probe identifiers.

    Parameters:
    probe_strings (bool): Flag indicating whether to use probe strings. Defaults to True.
    before (str): Prefix string to place before the probe identifier. Defaults to 'Probe_'.
    after (str): Suffix string to place after the probe identifier. Defaults to '_T_in'.

    Returns:
    dict: A dictionary where keys are probe identifiers and values are their corresponding colors.
    """
    
    # Instantiate the ERC_Management class
    erc_manager = ERC_Management()

    # Create a color dictionary using the specified parameters
    color_dict = erc_manager.create_colordict(probe_strings=probe_strings, before=before, after=after)
    
    return color_dict


def plot_one_BHE(data, probe, figsize=(10, 2.5), dpi=300, linewidth=0.5, axis_label_T = 'Temperature (°C)', axis_label_V = 'Volume flow (l/min)', ylims=None, ax=None, fig=None, colordict=None, title=None):
    """
    Plot the temperatures and flow rates for a given Borehole Heat Exchanger (BHE) data.

    Parameters:
    - data (DataFrame): A pandas DataFrame containing the BHE data.
    - probe (str or int): A string or integer indicating the probe to be plotted.
    - figsize (tuple): Size of the figure (width, height) in inches. Default is (10, 2.5).
    - dpi (int): Dots per inch (DPI) for the figure. Default is 300.
    - linewidth (float): Line width of the plots. Default is 0.5.
    - ylims (list): List containing the min and max limits for the y-axis. Default is None.
    - ax (matplotlib.axes._subplots.AxesSubplot): Axis object to plot on. Default is None.
    - fig (matplotlib.figure.Figure): Figure object. Default is None.

    Returns:
    - fig (matplotlib.figure.Figure): The figure object containing the plot.
    - ax (matplotlib.axes._subplots.AxesSubplot): The axis object of the plot.
    """
    # Create a dictionary for colors based on the probe strings
    if not colordict:
        colordict = ERC_Management().create_colordict(probe_strings=False)
    
    # Convert integer probe to string
    probe = str(probe)
    
    # Initialize the title string
    if title is False:
        title = ''
    else:
        if not title:
            title = f'Data of BHE {int(probe):02d}'
    
    # Create figure and axis if not provided
    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
    
    # Create a second y-axis
    ax2 = ax.twinx()
    
    # Set y-axis limits if not provided
    if ylims is None:
        ylims = [6, 21]
    
    # Plot the flow rate
    data.plot(ax=ax2, y=f'Probe_{probe}_V_dot', color=colordict.get(f'Probe_{probe}_V_dot', 'blue'), linewidth=linewidth, x_compat=True, label='$\mathregular{V}$', zorder=-10, legend=False)
    
    # Plot the inlet temperature
    data.plot(ax=ax, y=f'Probe_{probe}_T_in', color=colordict.get(f'Probe_{probe}_T_in', 'green'), linewidth=linewidth, x_compat=True, label='$\mathregular{T_{in}}$', zorder=10, legend=False)
    
    # Plot the outlet temperature
    data.plot(ax=ax, y=f'Probe_{probe}_T_out', color=colordict.get(f'Probe_{probe}_T_out', 'red'), linewidth=linewidth, x_compat=True, label='$\mathregular{T_{out}}$', zorder=11, legend=False)
    
    # Set legends and labels
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')

    ax2.set_ylim(0, 120)
    ax2.set_ylabel(axis_label_V)

    ax.grid(alpha=.3, which='major')
    ax.grid(alpha=.1, which='minor')
    ax.set_ylabel(axis_label_T)
    ax.set_xlabel('')

    dx, dy = 10, 0
    offset = ScaledTranslation(dx / fig.dpi, dy / fig.dpi, fig.dpi_scale_trans)
    for label in ax.get_xticklabels():
        label.set_transform(label.get_transform() + offset)
        label.set_rotation(0)
    
    ax.set_ylim(ylims[0], ylims[1])

    ax.set_title(title)
    
    return fig, ax


def plot_multiple_BHEs_alt(data, probes, figsize=(10, 3), dpi=100, ylims=None, linewidth=1, ax=None, fig=None):
    """
    Plot the temperatures and flow rates for a given Borehole Heat Exchanger (BHE) data.

    Parameters:
    - data (DataFrame): A pandas DataFrame containing the BHE data.
    - probes (str, int, or list): A string, integer, or list of strings/integers indicating the probe(s) to be plotted.
    - figsize (tuple): Size of the figure (width, height) in inches. Default is (10, 3).
    - dpi (int): Dots per inch (DPI) for the figure. Default is 100.
    - ylims (list): List containing the min and max limits for the y-axis. Default is None.
    - linewidth (int): Line width of the plots. Default is 1.
    - ax (matplotlib.axes._subplots.AxesSubplot): Axis object to plot on. Default is None.
    - fig (matplotlib.figure.Figure): Figure object. Default is None.

    Returns:
    - fig (matplotlib.figure.Figure): The figure object containing the plot.
    - ax (matplotlib.axes._subplots.AxesSubplot): The axis object of the plot.
    """
    # Create a dictionary for colors based on the probe strings
    all_color_dict = ERC_Management().create_colordict(probe_strings=False)
    
    # Ensure probes is a list
    if isinstance(probes, (str, int)):
        probes = [probes]
    
    # Convert integer probes to strings
    probes = [str(probe) for probe in probes]
    
    # Initialize the title string
    titlestr = ''
    
    # Create figure and axis if not provided
    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
    
    # Create a second y-axis
    ax2 = ax.twinx()
    
    # Loop through each probe and plot the data
    for probe in probes:
        titlestr += probe
        
        # Set y-axis limits if not provided
        if ylims is None:
            ylims = [
                np.nanmin(data[[f'Probe_{probe}_T_in', f'Probe_{probe}_T_out']].values.ravel()), 
                np.nanmax(data[[f'Probe_{probe}_T_in', f'Probe_{probe}_T_out']].values.ravel())
            ]
        
        # Plot the inlet temperature
        data.plot(ax=ax, y=f'Probe_{probe}_T_in', figsize=figsize, color=all_color_dict.get(probe, 'default'), linewidth=linewidth)
        
        # Plot the outlet temperature
        data.plot(ax=ax, y=f'Probe_{probe}_T_out', figsize=figsize, color=all_color_dict.get(probe, 'default'), alpha=0.5, linewidth=linewidth)
        
        # Plot the flow rate
        data.plot(ax=ax2, y=f'Probe_{probe}_V_dot', color=all_color_dict.get(probe, 'default'), style='--', alpha=0.2, linewidth=linewidth)
        
        if probe != probes[-1]:
            titlestr += ', '
    
    # Set legends and labels
    ax.legend(loc='upper left')
    ax.set_ylabel('Fluid temperature [°C]')
    ax.set_ylim(ylims[0], ylims[1])
    ax2.set_ylim(0, 100)
    ax2.legend(loc='upper right')
    ax2.set_ylabel('Flow rate [l/min]')
    
    # Set the title of the plot
    ax.set_title('BHE ' + titlestr)
    
    return fig, ax

def plot_data_by_vault(data, figsize=(6.4, 3), dpi=300, ylims=None, color_dict=None, lw=0.3, 
                       title='Data by underground vault', ymax_volflow=120, legend=True):
    """
    Plot temperature and volume flow data for different underground vaults.

    Parameters:
    data (DataFrame): The data to be plotted, with temperature and volume flow information.
    figsize (tuple): Size of the figure (width, height) in inches. Default is (6.4, 3).
    dpi (int): Dots per inch for the figure. Default is 300.
    ylims (tuple): Tuple specifying the y-axis limits for temperature plots. If None, limits are inferred from data.
    color_dict (dict): Dictionary mapping data columns to colors. If None, colors are generated.
    lw (float): Line width for plots. Default is 0.3.
    title (str): Title of the entire figure. Default is 'Data by underground vault'.
    ymax_volflow (int): Maximum y-axis limit for volume flow plots. Default is 120.

    Returns:
    fig (Figure): The matplotlib figure object containing the plots.
    """

    # Create a 2x3 subplot arrangement
    fig, ax = plt.subplots(2, 3, figsize=figsize, dpi=dpi)
    if title:
        fig.suptitle(title, y=1.05)
    
    # Initialize ERC_Management object and set plot parameters
    m = ERC_Management()
    m.set_plot_params()
    
    # Generate color dictionary if not provided
    if not color_dict:
        color_dict = m.create_colordict()

    # Generate ID strings for different vaults
    west_in, south_in, east_in = m.generate_vault_id_strings(after='_T_in')
    west_out, south_out, east_out = m.generate_vault_id_strings(after='_T_out')
    west_vdot, south_vdot, east_vdot = m.generate_vault_id_strings(after='_V_dot')

    # Determine y-axis limits for temperature plots
    if not ylims:
        minT = data.filter(regex='Probe_[0-9]+_T_').min().min()
        maxT = data.filter(regex='Probe_[0-9]+_T_').max().max()
    else:
        minT = ylims[0]
        maxT = ylims[1]

    westlabel, southlabel, eastlabel  = ERC_Management().generate_vault_id_strings(before='', after='')

    # Plot data for West vault
    data.plot(ax=ax[0, 0], y=west_in, color=[color_dict.get(x, 'k') for x in west_in], legend=False, 
              xticks=[], xlabel="", linewidth=lw)
    ax2 = ax[1, 0].twinx()
    ax2.set_ylim(0, ymax_volflow)
    data.plot(ax=ax2, y=west_vdot, cmap='Greys', legend=False, xticks=[], xlabel="", linewidth=lw, alpha=.5)
    data.plot(ax=ax[1, 0], y=west_out, color=[color_dict.get(x, 'k') for x in west_in], legend=legend, 
              linewidth=lw, label=westlabel)


    # Plot data for South vault
    data.plot(ax=ax[0, 1], y=south_in, color=[color_dict.get(x, 'k') for x in south_in], legend=False, 
              xticks=[], xlabel="", linewidth=lw)
    ax3 = ax[1, 1].twinx()
    ax3.set_ylim(0, ymax_volflow)
    data.plot(ax=ax3, y=south_vdot, cmap='Greys', legend=False, xticks=[], xlabel="", linewidth=lw, alpha=.5)
    data.plot(ax=ax[1, 1], y=south_out, color=[color_dict.get(x, 'k') for x in south_in], legend=legend, 
              linewidth=lw, label=southlabel)

    # Plot data for East vault
    data.plot(ax=ax[0, 2], y=east_in, color=[color_dict.get(x, 'k') for x in east_in], legend=False, 
              xticks=[], xlabel="", linewidth=lw)
    ax4 = ax[1, 2].twinx()
    ax4.set_ylim(0, ymax_volflow)
    data.plot(ax=ax4, y=east_vdot, cmap='Greys', legend=False, xticks=[], xlabel="", linewidth=lw, alpha=.5)
    data.plot(ax=ax[1, 2], y=east_out, color=[color_dict.get(x, 'k') for x in east_in], legend=legend, 
              linewidth=lw, label=eastlabel)

    # Set titles for subplots
    ax[0, 0].set_title('A')
    ax[0, 1].set_title('B')
    ax[0, 2].set_title('C')
    ax4.set_ylabel('Volume flow (l/min)')

    # Set y-axis limits and remove unnecessary axis labels
    for axi in ax.flat:
        axi.set_ylim(minT, maxT)
        axi.set_xlabel('')

    ax[0, 0].set_ylabel('Inlet temp. (°C)')
    ax[1, 0].set_ylabel('Outlet temp. (°C)')

    for axi in ax[0, :]:
        axi.axes.get_xaxis().set_visible(False)
    for axi in ax[:, 1:].flat:
        axi.axes.get_yaxis().set_visible(False)

    ax2.axes.get_yaxis().set_visible(False)
    ax3.axes.get_yaxis().set_visible(False)

    if legend:
        for axi in ax[1,:]:
            axi.legend(loc='upper center', 
                    bbox_to_anchor=(0.5, -0.35),fancybox=False, shadow=False, ncol=5, prop={'size': 6}, handlelength=1, labelspacing=.5, columnspacing=0.8)


    # Adjust subplots layout
    fig.subplots_adjust(wspace=0.03, hspace=0.1)

    return fig


#########################################################
############### New from analysis paper #################
#########################################################
def plot_well_borders(ax):
    """Plots well borders on the given axis."""
    borders = {
        'south': ([3, 26, 26, 26, 26, 88, 88, 88, 110, 110, 118, 118, 118, 20, 3, 3],
                    [24, 24, 18, 11, 11, 11, 11, 18, 18, 8, 8, 3, 3, 3, 3, 18], '#6F4E37'),
        'west': ([3,26,26,26,26,64,64,64,64,3,3,3],
                    [25,25,25,47,47,47,47,54,54,54,54,25], '#6082B6'),
        'east': ([65, 88, 88, 88, 88, 111, 111, 111, 111, 118, 118, 118, 118, 65, 65, 65],
                    [47, 47, 47, 19, 19, 19, 19, 9, 9, 9, 9, 54, 54, 54, 54, 47], '#355E3B')
    }
    for key, (x, y, color) in borders.items():
        ax.fill(x, y, color='whitesmoke', edgecolor=color, linewidth=.9, alpha=.3)

def plot_ducts(ax, fontsize):
    """Plots the ducts and annotations on the given axis."""
    ducts = {
        'B': (74.01, 4.18, '#6F4E37'),
        'C': (100.9, 32.14, '#6082B6'),
        'A': (18.76, 46.45, '#355E3B')
    }
    for label, (x, y, color) in ducts.items():
        well = Rectangle((x, y), 5, 5, linewidth=1, edgecolor='k', facecolor='w', alpha=.9, zorder=100)
        ax.add_patch(well)
        ax.annotate(label, [x + 2.7, y + 2.3], va='center', ha='center', c=color, fontsize=fontsize, zorder=101)


def plot_bhe_field_comparison(left_plot, right_plot, figsize=(6.33,2.3), dpi=300, scattersize=200, fontsize=5, textcolor='w'):
    """
    Plot a comparison of Borehole Heat Exchanger (BHE) field data for two different scenarios.

    Parameters:
    left_plot (dict): Dictionary containing parameters for the left plot (e.g., cooling scenario).
        Expected keys: 'title', 'zValue', 'vmin', 'vmax', 'cmap', 'label'.
    right_plot (dict): Dictionary containing parameters for the right plot (e.g., heating scenario).
        Expected keys: 'title', 'zValue', 'vmin', 'vmax', 'cmap', 'label'.

    Returns:
    fig: The matplotlib figure object containing the plots.
    """
    # Load the BHE field data from a CSV file
    PipeData = pd.read_csv('D:/BHEfieldData/ERC_Datapub/ERC_BHEfield_Data_Code/Supplementary_BHE_Data.csv')
    
    # Create subplots with shared x and y axes
    fig, ax = plt.subplots(1, 2, figsize=figsize, dpi=dpi, sharex=True, sharey=True)

    # Plot common elements (well borders and ducts) on both subplots
    for axi in ax:
        plot_well_borders(axi)
        ERC = Rectangle((27.59, 12.43), 58.31, 33.48, linewidth=.9, edgecolor='k', facecolor='none', hatch=r"//")
        axi.add_patch(ERC)
        plot_ducts(axi, fontsize=fontsize+1)
        axi.set_aspect('equal')
        axi.axes.get_yaxis().set_ticks([])
        axi.set_axis_off()

    # Plot the left subplot (e.g., Cooling)
    ax[0].set_title(left_plot['title'], y=0.93)
    sc = ax[0].scatter(PipeData['X'], PipeData['Y'], s=scattersize, c=left_plot['zValue'], 
                       vmin=left_plot['vmin'], vmax=left_plot['vmax'], cmap=left_plot['cmap'])
    for i, row in PipeData.iterrows():
        ax[0].annotate(np.round(left_plot['zValue'][i], 2), [row['X'] + 0.2, row['Y'] - 0.2], 
                       va='center', ha='center', c=textcolor, fontsize=fontsize)

    # Add a scale bar to the left subplot
    asb = AnchoredSizeBar(ax[0].transData,
                          10,
                          r"10 m",
                          loc='lower left',
                          pad=0.0, borderpad=0.0, sep=1,
                          frameon=False, label_top=True,
                          bbox_to_anchor=(0.152, 0.295),
                          bbox_transform=ax[0].figure.transFigure)
    ax[0].add_artist(asb)
    # Add a colorbar to the left subplot
    cbax = ax[0].inset_axes([.375, -.07, 0.25, 0.04], transform=ax[0].transAxes)
    fig.colorbar(sc, ax=ax[0], cax=cbax, orientation='horizontal')
    ax[0].text(.33, -.06, left_plot['label'], transform=ax[0].transAxes)

    # Plot the right subplot (e.g., Heating)
    ax[1].set_title(right_plot['title'], y=0.93)
    sc = ax[1].scatter(PipeData['X'], PipeData['Y'], s=scattersize, c=right_plot['zValue'], 
                       vmin=right_plot['vmin'], vmax=right_plot['vmax'], cmap=right_plot['cmap'])
    for i, row in PipeData.iterrows():
        ax[1].annotate(np.round(right_plot['zValue'][i], 2), [row['X'] + 0.2, row['Y'] - 0.2], 
                       va='center', ha='center', c=textcolor, fontsize=fontsize)

    # Add a colorbar to the right subplot
    cbax = ax[1].inset_axes([.375, -.07, 0.25, 0.04], transform=ax[1].transAxes)
    fig.colorbar(sc, ax=ax[1], cax=cbax, orientation='horizontal')
    ax[1].text(.33, -.06, right_plot['label'], transform=ax[1].transAxes)

    # Adjust the space between the subplots
    fig.subplots_adjust(wspace=-0.05)
    
    return fig, ax



def plot_one_bhe_field(left_plot, figsize=(6.33,2.3), dpi=300, scattersize=200, fontsize=5, textcolor='w', plot_duct=True, plot_building=True, plot_scale_bar=True, plot_values=True, plot_BHE_IDs=False):
    """
    Plot a comparison of Borehole Heat Exchanger (BHE) field data for two different scenarios.

    Parameters:
    left_plot (dict): Dictionary containing parameters for the left plot (e.g., cooling scenario).
        Expected keys: 'title', 'zValue', 'vmin', 'vmax', 'cmap', 'label'.
    right_plot (dict): Dictionary containing parameters for the right plot (e.g., heating scenario).
        Expected keys: 'title', 'zValue', 'vmin', 'vmax', 'cmap', 'label'.

    Returns:
    fig: The matplotlib figure object containing the plots.
    """
    # Load the BHE field data from a CSV file
    PipeData = pd.read_csv('D:/BHEfieldData/ERC_Datapub/ERC_BHEfield_Data_Code/Supplementary_BHE_Data.csv')
    
    # Create subplots with shared x and y axes
    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi, sharex=True, sharey=True)

    # Plot common elements (well borders and ducts) on both subplots

    plot_well_borders(ax)
    if plot_building:
        ERC = Rectangle((27.59, 12.43), 58.31, 33.48, linewidth=.9, edgecolor='k', facecolor='none', hatch=r"//")
        ax.add_patch(ERC)
    if plot_duct:
        plot_ducts(ax, fontsize=fontsize+1)
    ax.set_aspect('equal')
    ax.axes.get_yaxis().set_ticks([])
    ax.set_axis_off()

    # Plot the left subplot (e.g., Cooling)
    ax.set_title(left_plot['title'], y=0.93)
    sc = ax.scatter(PipeData['X'], PipeData['Y'], s=scattersize, c=left_plot['zValue'], 
                       vmin=left_plot['vmin'], vmax=left_plot['vmax'], cmap=left_plot['cmap'])
    if plot_values:
        for i, row in PipeData.iterrows():
            ax.annotate(np.round(left_plot['zValue'][i], 2), [row['X'] + 0.2, row['Y'] - 0.2], 
                        va='center', ha='center', c=textcolor, fontsize=fontsize)
    if plot_BHE_IDs:
        for i, row in PipeData.iterrows():
            ax.annotate(int(row['BHE ID']), [row['X'] + 0.2, row['Y'] - 0.2], 
                        va='center', ha='center', c=textcolor, fontsize=fontsize)

    if plot_scale_bar:
        # Add a scale bar to the left subplot
        asb = AnchoredSizeBar(ax.transData,
                            10,
                            r"10 m",
                            loc='lower left',
                            pad=0.0, borderpad=0.0, sep=1,
                            frameon=False, label_top=True,
                            bbox_to_anchor=(0.152, 0.295),
                            bbox_transform=ax.figure.transFigure)
        ax.add_artist(asb)
    # Add a colorbar to the left subplot
    cbax = ax.inset_axes([.375, -.07, 0.25, 0.04], transform=ax.transAxes)
    fig.colorbar(sc, ax=ax, cax=cbax, orientation='horizontal')
    ax.text(.33, -.06, left_plot['label'], transform=ax.transAxes)

    return fig, ax