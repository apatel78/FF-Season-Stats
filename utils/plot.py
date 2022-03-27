from matplotlib import pyplot as plt
import numpy as np
import os

def plot_single_bar(x_data, y_data, filename, bottom_label, title, path):
    try:
        os.mkdir(path)
    except OSError as error:
        pass

    plt.rcdefaults()
    fig, ax = plt.subplots()

    y_pos = np.arange(len(x_data))

    colors = []
    color = plt.cm.rainbow(np.linspace(0, 1, len(y_data)))
    for i, c in zip(range(len(y_data)), color):
        colors.append(c)

    ax.barh(y_pos, y_data, align='center',color=colors, edgecolor='blue')
    ax.set_yticks(y_pos, labels=x_data)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(bottom_label)
    ax.set_title(title)
    plt.tight_layout()

    #add numbers to plot
    for i, datum in enumerate(y_data):
        ax.text(datum / 2, i + .12, str(datum), color='black', fontweight='bold')

    print("Successfully Created " + filename)
    plt.savefig(path + '/' + filename)

def plot_triple_bar(x_data, y_data, filename, path):
    try:
        os.mkdir(path)
    except OSError as error:
        pass

    labels = list(y_data.keys())
    data = np.array(list(y_data.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['Dark2'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(x_data, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncol=len(x_data), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    plt.tight_layout()
    print("Successfully Created " + filename)
    plt.savefig(path + '/' + filename)