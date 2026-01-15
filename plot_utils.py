"""
Author: Matteo Loporchio
"""

import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib import font_manager
from pathlib import Path

# SOURCE: https://colorbrewer2.org/#type=qualitative&scheme=Set1&n=5
COLORS = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#f781bf',"#4d4d4d"]
DEFAULT_FONT_SIZE = 14
DEFAULT_FIGURE_SIZE = (3, 3)

# Set default font
DEFAULT_FONT_PATH = 'fonts/texgyreheros-regular.otf'
if os.path.exists(DEFAULT_FONT_PATH):
    font_manager.fontManager.addfont(DEFAULT_FONT_PATH)
    prop = font_manager.FontProperties(fname=DEFAULT_FONT_PATH)
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = prop.get_name()

plt.rcParams.update({'font.size': DEFAULT_FONT_SIZE})
plt.rcParams.update({'axes.titlesize': DEFAULT_FONT_SIZE})

# data = sdf[event_type]
def plot_dist(data, title, xlabel, ylabel, xscale, yscale, output_file=None, show=True):
    data_freq = data.value_counts(name="frequency")
    fig = plt.figure(figsize=DEFAULT_FIGURE_SIZE, layout="tight")
    ax = fig.add_subplot()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    ax.scatter(data_freq[data.name], data_freq['frequency'], color=COLORS[1], marker='.')
    ax.grid(linestyle='--', linewidth=0.5, which="major")
    ax.grid(linestyle='--', linewidth=0.5, which="minor", alpha=0.2)
    #ax.tick_params("x", rotation=90)
    plt.xticks(ha='left', rotation=90)
    tick_labels = plt.xticks()[1]
    tick_labels[0].set_horizontalalignment('center')
    if not output_file is None: 
        plt.savefig(output_file, format='pdf', bbox_inches='tight')
    if show:
        plt.show() 
    else:
        plt.close()

# data = sdf[event_type]
def plot_ecdf(data, title, xlabel, ylabel, xscale, yscale, output_file=None, show=True):
    fig = plt.figure(figsize=DEFAULT_FIGURE_SIZE, layout="tight")
    ax = fig.add_subplot()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    sns.ecdfplot(data, color=COLORS[1], ax=ax)
    ax.grid(linestyle='--', linewidth=0.5, which="major")
    ax.grid(linestyle='--', linewidth=0.5, which="minor", alpha=0.2)
    #ax.tick_params("x", rotation=90)
    plt.xticks(ha='left', rotation=90)
    tick_labels = plt.xticks()[1]
    tick_labels[0].set_horizontalalignment('center')
    if not output_file is None: 
        plt.savefig(output_file, format='pdf', bbox_inches='tight')
    if show:
        plt.show() 
    else:
        plt.close()

def set_font_size(ax, font_size=DEFAULT_FONT_SIZE):
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(font_size)