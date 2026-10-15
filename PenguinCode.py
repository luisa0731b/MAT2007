# Copmaring flipper length vs body mass of penguins, per species! #
# The following packages are required
# - numpy
# - pandas
# - matplotlib
# - scipy

import numpy as np # for number crunching
import pandas as pd # for handling data table
import matplotlib.pyplot as plt # for figures
from scipy import stats # imports scipy statistic tools

np.random.seed(1) # same random numbers every run

# reads the data
df = pd.read_csv("C:/Users/luisa/OneDrive/Desktop/MAT2007/5. penguin project/PenguinsResearchData.csv") # read data and loads CSV into a table called df, one row per penguion
df = df.rename(columns={"Flipper Length (mm)": "flipper", "Body Mass (g)": "mass"}) # shortens the long column names
df = df.dropna(subset=["flipper", "mass"]) # drop the 2 penguins that have no measurements </3
df["species"] = df["Species"].str.split().str[0] # "Adelie Penguin (...)" -> "Adelie"

SPECIES = ["Adelie", "Chinstrap", "Gentoo"] # list of the three species
COLORS = {"Adelie": "#2a6fb0", "Chinstrap": "#d9822b", "Gentoo": "#3a9d5d"} # dictionary linking each species to a color, so species looks the same in every figure

# sub-sampling
def subsample(g, func, k, repeats=200): # defines function\
    # split penguins into random parts, apply function to each part, and return mean and uncertainty
    values, errors = [], [] # two empty lists to collect results
    for _ in range(repeats): # repeat everything below 200 times
        shuffled = g.sample(frac=1) # shuffle the penguins
        parts = [shuffled.iloc[i] for i in np.array_split(np.arange(len(g)), k)] # picks penguins out of shuffled table
        results = [func(p) for p in parts] # runs function on each part
        values.append(np.mean(results)) # average of k results, saved to values
        errors.append(np.std(results, ddof=1) / np.sqrt(k)) # standard deviation of k results divided by sqrt k (uncertainty)
    return np.mean(values), np.mean(errors)

# means (flipper and mass) per species
means = {} # empty dictionary to store results
for s in SPECIES:
    g = df[df.species == s] # loop over each species
    for col in ["flipper", "mass"]: # loop over two measurements
        m, e = subsample(g, lambda p: p[col].mean(), k=10) # splits into 10 parts, return mean & uncertainty
        means[(s, col)] = (m, e, g[col].std()) # mean, uncertainty, STD # stores mean & std under the key
        print(f"{s:10s} {col:8s} mean = {m:7.1f} ± {e:5.1f}   STD = {g[col].std():6.1f}") # prints one line per species and measurement

# regression per species
print()
fits = {} # empty dictionary to store the fits
for s in SPECIES:
    g = df[df.species == s]
    fit = stats.linregress(g.flipper, g.mass) # slope, intercept, rvalue, pvalue, stderr
    r_err = subsample(g, lambda p: stats.linregress(p.flipper, p.mass).rvalue, k=5)[1] # uncertainty of r
    R2_err = subsample(g, lambda p: stats.linregress(p.flipper, p.mass).rvalue ** 2, k=5)[1] # same for R^2
    fits[s] = fit # saves the fit, so the plots can use it later
    print(f"{s:10s} slope = {fit.slope:5.1f} g/mm   r = {fit.rvalue:.2f} ± {r_err:.2f}   " # prints the slope
          f"R² = {fit.rvalue ** 2:.2f} ± {R2_err:.2f}   p = {fit.pvalue:.1e}")

# figure 1 (histograms)
fig, ax = plt.subplots(2, 3, figsize=(11, 6), sharex="row", sharey="row") # creates 2x3 grid of empty plots
for j, s in enumerate(SPECIES):
    for i, (col, label) in enumerate([("flipper", "Flipper length (mm)"), ("mass", "Body mass (g)")]):
        m, e, sd = means[(s, col)] # reads mean, uncertainty, std for this species & measurement from the means dictionary
        ax[i, j].hist(df[df.species == s][col], bins=15, color=COLORS[s]) # draws the histogram of that species' values, using the species' color
        ax[i, j].axvline(m, color="black", ls="--") # draws the dashed vertical line at the mean
        d = 1 if col == "flipper" else 0 # decimals to show
        ax[i, j].set_title(f"{s} (Mean: {m:.{d}f} ± {e:.{d}f}, STD: {sd:.{d}f})", fontsize=10) # the title
        ax[i, j].set_xlabel(label) # axis label
ax[0, 0].set_ylabel("Count of penguins") # y-label
ax[1, 0].set_ylabel("Count of penguins")
fig.tight_layout(); fig.savefig("peng_fig1_hist.png") # prevents overlapping

# figures 2-4 (one scatter plot per species)
for s in SPECIES:
    g, fit = df[df.species == s], fits[s] # g is that species' penguins and fit is its regression result
    fig, ax = plt.subplots(figsize=(5.5, 4.5)) # new empty figure and one plot
    ax.scatter(g.flipper, g.mass, s=18, alpha=0.65, color=COLORS[s]) # draws one dot per penguion
    x = np.array([g.flipper.min(), g.flipper.max()]) # x is just the smallest & largest flipper length of the species
    ax.plot(x, fit.intercept + fit.slope * x, color="black", lw=2) # draws regression line between those two x-values, with fit.intercept + fit.slop * x as the y-intercept
    ax.text(0.03, 0.97, f"r = {fit.rvalue:.2f}\nR² = {fit.rvalue ** 2:.2f}\n" # writes the box with r, R^2, p, and the equation
            f"p < 0.001\nmass = {fit.intercept:.0f} + {fit.slope:.1f}·flipper",
            transform=ax.transAxes, va="top", bbox=dict(boxstyle="round", fc="white"))
    ax.set(xlabel="Flipper length (mm)", ylabel="Body mass (g)", title=s) # axis label
    fig.tight_layout(); fig.savefig(f"peng_fig3_scatter_{s}.png") # saves the figure