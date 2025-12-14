"""
Author: Matteo Loporchio
"""

DEFAULT_FONT_SIZE = 14
DEFAULT_FIGURE_SIZE = (3,3)
# SOURCE: https://colorbrewer2.org/#type=qualitative&scheme=Set1&n=5
COLORS = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#f781bf',"#4d4d4d"]

def set_font_size(ax, font_size=DEFAULT_FONT_SIZE):
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(font_size)