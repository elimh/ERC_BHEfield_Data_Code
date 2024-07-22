import matplotlib
import matplotlib.pyplot as plt
import numpy as np


class ERC_Management():
    def __init__(self) -> None:
        self.blues = ['#4169E1', '#0047AB', '#89CFF0', '#0000FF', '#7393B3','#0096FF','#00FFFF','#6495ED','#6F8FAF','#6082B6','#5D3FD3','#ADD8E6','#191970']
        self.west_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.browns = ['#E1C16E','#CD7F32','#A52A2A','#F5DEB3','#DAA06D','#800020','#6E260E','#C19A6B','#D27D2D','#E97451','#6F4E37','#5C4033','#988558','#C2B280','#C19A6B','#C04000','#A95C68','#483C32']
        self.south_ids = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25]
        self.greens = ['#097969', '#AFE1AF','#E4D00A','#50C878','#5F8575','#4F7942','#228B22','#7CFC00','#008000','#355E3B','#00A36C','#90EE90','#32CD32','#8A9A5B','#98FB98','#93C572']
        self.east_ids = [23, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    
    def generate_ID_strings_per_shaft(self, probe_strings=True, before='Probe_', after='_T_in'):
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
        west,south,east = self.generate_ID_strings_per_shaft(probe_strings=probe_strings, before=before, after=after)
        self.colors_west = dict(zip(west, self.blues[:len(west)]))
        self.colors_south = dict(zip(south, self.browns[:len(south)]))
        self.colors_east = dict(zip(east, self.greens[:len(east)]))
        self.colors_all = {**self.colors_west, **self.colors_south, **self.colors_east}
        return self.colors_all
    
    def set_plot_params(self):
        matplotlib.rcParams['pdf.fonttype'] = 42
        matplotlib.rcParams['ps.fonttype'] = 42
        plt.rcParams['savefig.bbox'] = 'tight'
        plt.rcParams['savefig.pad_inches'] = 0.01
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial']
        plt.rcParams['axes.labelsize'] = 7
        plt.rcParams['ytick.labelsize'] = 7
        plt.rcParams['xtick.labelsize'] = 7
        plt.rcParams['legend.fontsize'] = 7
        plt.rcParams['font.size'] = 7
        plt.rcParams['ytick.minor.visible']= True
        plt.rcParams['mathtext.fontset'] = "dejavusans"

def get_colordict(probe_strings=True, before='Probe_', after='_T_in'):
    return ERC_Management().create_colordict(probe_strings=probe_strings, before=before, after=after)


def plot_one_BHE(data, probes, figsize=(10,3), dpi=100, ylims=None):
    all_color_dict = ERC_Management().create_colordict(probe_strings=False)
    if type(probes) == str:
        probes = [probes]
    titlestr = ''
    fig, ax = plt.subplots(1,1,figsize=figsize, dpi=dpi)
    ax2 = ax.twinx()
    for probe in probes:
        titlestr += probe
        if ylims == None:
            ylims = [np.nanmin(data[[f'Probe_{probe}_T_in', f'Probe_{probe}_T_out']].values.ravel()), np.nanmax(data[[f'Probe_{probe}_T_in', f'Probe_{probe}_T_out']].values.ravel())]
        #if probe == probes[0]:
            #ax = data.plot(y = f'Probe_{probe}_T_in', figsize=figsize, color=all_color_dict.get(probe))
        data.plot(ax=ax, y = f'Probe_{probe}_T_in', figsize=figsize, color=all_color_dict.get(probe),linewidth=1)
        data.plot(ax=ax, y = f'Probe_{probe}_T_out', figsize=figsize, color=all_color_dict.get(probe), alpha=.5,linewidth=1)
        data.plot(ax=ax2, y= f'Probe_{probe}_V_dot', color=all_color_dict.get(probe), style='--', alpha=.2,linewidth=1)
        if probe != probes[-1]:
            titlestr +=', '
    ax.legend(loc='upper left')
    ax.set_ylabel('Fluid temperature [°C]')
    ax.set_ylim(ylims[0],ylims[1])
    ax2.set_ylim(0,100)
    ax2.legend(loc='upper right')
    ax2.set_ylabel('Flow rate [m3/h]')
    ax.set_title('BHE '+titlestr)
    return ax 

def plot_data_by_vault(data, figsize=(6.4,3), dpi=300, ylims=None, all_color_dict = None, lw=0.3, title='Data by underground vault'):
    fig, ax = plt.subplots(2,3,figsize=figsize, dpi=dpi)#,layout='constrained')
    fig.suptitle(title)
    m = ERC_Management()
    m.set_plot_params()
    if not all_color_dict:
        all_color_dict = m.create_colordict()
    west_in, south_in, east_in = m.generate_ID_strings_per_shaft(after='_T_in')
    west_out, south_out, east_out = m.generate_ID_strings_per_shaft(after='_T_out')
    west_vdot, south_vdot, east_vdot = m.generate_ID_strings_per_shaft(after='_V_dot')

    if not ylims:
        minT = data.filter(regex='Probe_[0-9]+_T_').min().min()
        maxT = data.filter(regex='Probe_[0-9]+_T_').max().max()
    else:
        minT = ylims[0]
        maxT = ylims[1]

    # blue
    data.plot(ax=ax[0,0],y=west_in,color=[all_color_dict.get(x, 'k') for x in west_in],legend=False, xticks=[], xlabel="", linewidth=lw)
    ax2 = ax[0,0].twinx()
    ax2.set_ylim(0,100)
    data.plot(ax=ax2,y=west_vdot, cmap='Greys', legend=False, xticks=[], xlabel="", linewidth=lw, alpha=.5)#color=[all_color_dict.get(x, 'k') for x in west_in]
    data.plot(ax=ax[1,0],y=west_out,color=[all_color_dict.get(x, 'k') for x in west_in],legend=False, linewidth=lw)

    data.plot(ax=ax[0,1],y=south_in,color=[all_color_dict.get(x, 'k') for x in south_in],legend=False, xticks=[], xlabel="", linewidth=lw)
    ax3 = ax[0,1].twinx()
    ax3.set_ylim(0,100)
    data.plot(ax=ax3,y=south_vdot, cmap='Greys', legend=False, xticks=[], xlabel="", linewidth=lw, alpha=.5)
    data.plot(ax=ax[1,1],y=south_out,color=[all_color_dict.get(x, 'k') for x in south_in],legend=False, linewidth=lw)

    data.plot(ax=ax[0,2],y=east_in,color=[all_color_dict.get(x, 'k') for x in east_in],legend=False, xticks=[], xlabel="", linewidth=lw)
    ax4 = ax[0,2].twinx()
    ax4.set_ylim(0,100)
    data.plot(ax=ax4,y=east_vdot, cmap='Greys', legend=False, xticks=[], xlabel="", linewidth=lw, alpha=.5)
    data.plot(ax=ax[1,2],y=east_out,color=[all_color_dict.get(x, 'k') for x in east_in],legend=False, linewidth=lw)

    ax[0,0].set_title('V1')
    ax[0,1].set_title('V2')
    ax[0,2].set_title('V3')
    ax4.set_ylabel('Volume flow [l/min]')

    ## Remove unnecessary axis labels
    for axi in ax.flat:
        axi.set_ylim(minT, maxT)

    ax[0,0].set_ylabel('Inlet temp. [°C]')
    ax[1,0].set_ylabel('Outlet temp. [°C]')

    for axi in ax[0,:]:
        axi.axes.get_xaxis().set_visible(False)

    for axi in ax[:,1:].flat:
        axi.axes.get_yaxis().set_visible(False)

    ax2.axes.get_yaxis().set_visible(False)
    ax3.axes.get_yaxis().set_visible(False)

    # adjust subplots
    fig.subplots_adjust(wspace=0.03, hspace=0.1)
    return fig