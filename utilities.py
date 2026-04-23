import matplotlib.pyplot as plt
import numpy as np
# plt.rcParams.update({"font.size":16,"font.family":"serif","mathtext.fontset":"stix","axes.linewidth":1.2})


tue_red, red_compl = "#C71918", "#18C6C7"

plt.rcParams.update({
    "font.size": 16,
    "font.family": "serif",
    "mathtext.fontset": "stix",
    "axes.linewidth": 1.2,
})


def write_csv(scan, filename):
	"""
	Write scan data in .csv file to import in Mimer.
	"""

	## Write header row
	header_row = ''
	for par_name in scan[0]:
		header_row += par_name + '; '
	header_row += "\n"
	with open(filename, "w") as file:
		file.write(header_row)

	## Write a row for each design point in the scan
	data_rows = ''
	for design_point in scan:
		for par_name in design_point:
			data_rows += str(design_point[par_name]) + '; '
		data_rows += "\n"
	with open(filename, "a") as file:
		file.write(data_rows)


def plot_scan(scan_out, x_par, y_par, outname="plot.png", color=tue_red):
    """
	change to use lineaamaaarkers babbyyy
    """
    x = [point[x_par] for point in scan_out]
    y = [point[y_par] for point in scan_out]

    fig, ax = plt.subplots()
    ax.plot(x, y, "-o", color=color, label=y_par)
    ax.set_xlabel(x_par)
    ax.set_ylabel(y_par, color="black")
	
    ax.tick_params(axis="y", labelcolor="black")

    fig.tight_layout()
    fig.savefig(outname, dpi=300, bbox_inches="tight")
    plt.close(fig)

color_left = tue_red
color_right = red_compl


def plot_scan_two_y(
    scan_out,
    x_par,
    y_par_left,
    y_par_right,
    outname="plot.png"
):
    
    x = [point[x_par] for point in scan_out]
    y_left = [point[y_par_left] for point in scan_out]
    y_right = [point[y_par_right] for point in scan_out]

	
    fig, ax1 = plt.subplots()
    line1 = ax1.plot(x, y_left, "-o", color=color_left, label=y_par_left)
    ax1.set_xlabel(x_par)
    ax1.set_ylabel(y_par_left, color=color_left)
    ax1.tick_params(axis="y", labelcolor=color_left)

    ax2 = ax1.twinx()
    line2 = ax2.plot(x, y_right, "-o", color=color_right, label=y_par_right)
    ax2.set_ylabel(y_par_right, color=color_right)
    ax2.tick_params(axis="y", labelcolor=color_right)

    lines = line1 + line2
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc="best")

    fig.tight_layout()
    fig.savefig(outname, dpi=300, bbox_inches="tight")
    plt.close(fig)


