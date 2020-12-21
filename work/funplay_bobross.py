# NOTES AND RESOURCES
# These are fairly heavily annotated to help beginners understand what's happening

# pandas docs https://pandas.pydata.org/docs/
# especially https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/index.html
# and for plotting examples
# https://python-graph-gallery.com/
# bobross data 
# https://www.twoinchbrush.com/
# https://github.com/jwilber/Bob_Ross_Paintings

# RULES FOR FUNCTIONS
# To keep use simple, main functions should have no more than 2 arguments
# For functions using the main dataset bob, avoid function input
# Syntax for base functions compatible with companion R code for user, usually just function() 
# have some error checks with informative messages
# demo only one way to do something, e.g. use df.loc[:, "col"] or df[["col"]] not both

import re
import sys
import itertools
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


# HELPER FUNCTIONS
pat = re.compile(r"\\r|\\n|[\[\]']")

def get_bobross():
	bob = pd.read_csv("https://raw.githubusercontent.com/littlebuttermilk/ncssm_sessions/master/data/bob_ross_paintings.csv")
	bob = bob.assign(colors = bob.colors.replace(pat, "").str.split(r"\s*,\s*"), 
		color_hex = bob.color_hex.replace(pat, "").str.split(r"\s*,\s*"))

	return bob


def get_help():
	# help file for students who forget usage
  	# either with one argument, bare unquoted function name, to print usage for that fun
  	# or no arguments to print all
	return "TO DO"



# VIEW DATA

def get_colortable():
	ctable = bob.apply(lambda r: pd.Series(r['color_hex']), axis = 1).dropna().iloc[0]
	ctable.index = bob.apply(lambda r: pd.Series(r['colors']), axis = 1).dropna().iloc[0]
	ctable = ctable.rename(None)

	return ctable


def get_painting_names(random = False):
	# TODO: error checks for incorrect type for R/Python confusion
	# return as array rather than pandas series
	if random:
		return np.random.choice(bob.painting_title.array)
		# return bob.painting_title.sample(1).iloc[0]
	else:
		return bob.painting_title.array

def plot_blobs(painting = "Downstream View"):
	# check that bob has been loaded, return informative error

	# Filter & reshape data
	# .loc[...] returns dataframe, .iloc[0] returns first row as named series
	d = bob.loc[bob.painting_title == painting, ['colors', 'color_hex']].iloc[0]
	d = pd.DataFrame({'colors': d['colors'], 'color_hex': d['color_hex']})

	# Generate random point in two dimensional box from -10 to 10
	d = d.assign(x = np.random.uniform(low = -10, high = 10, size = d.shape[0]),
		y = np.random.uniform(low = -10, high = 10, size = d.shape[0]))

	p = d.plot.scatter(x = 'x', y = 'y', s = pd.Series(8000, index = d.colors),
		title = painting,
		alpha = .7, c = d['color_hex'],
		xlim = (-12, 12), ylim = (-12, 12),  
		xticks = None, figsize = (12, 8)) # (width, height) in inches

	for i, r in d.iterrows():
		p.annotate(text = r['colors'], xy = (r['x']-1.25, r['y'])) # no good centering

	# display
	p
	plt.axis('off')
	plt.show()

	return None


def plot_cloud(painting = "Downstream View"):
	# check that bob has been loaded, return informative error

	# Filter & reshape data
	d = bob.loc[bob.painting_title == painting, ['colors', 'color_hex']].iloc[0]
	d = pd.DataFrame({'colors': d['colors'], 'color_hex': d['color_hex']})
	d.colors = d.colors.str.strip()
	d.color_hex = d.color_hex.str.strip()

	# Generate centers of clouds in two dimensional box from -10 to 10
	d = d.assign(x = np.random.uniform(low = -10, high = 10, size = d.shape[0]),
		y = np.random.uniform(low = -10, high = 10, size = d.shape[0]))

	# Create new data frame in chunks of rows
	# with point cloud coordinates and colors, color_hex labels
	d = d.assign(cloud = d.apply(lambda r: np.random.multivariate_normal([r['x'], r['y']], [[1, 0], [0, 1]], 
				size = 100), axis = 1)
				)

	# 'explode' the cloud so we have one row for each 2d random point, 100 for each color
	# replace x, y column values with cloud values, drop cloud, to use familiar syntax from plot_blob
	d = d.explode('cloud').reset_index()
	d[["x", "y"]] = d.cloud.to_list()
	d = d.drop('cloud', axis = 1)


	d.plot.scatter(x = 'x', y = 'y', s = pd.Series(3000, index = d.colors),
		title = painting,
		alpha = .7, c = d['color_hex'],
		xlim = (-12, 12), ylim = (-12, 12),  
		xticks = None, figsize = (12, 8))
	
	plt.axis('off')
	plt.show()

	return None



# SUMMARIZE DATA

def colors_byseason(stat = "total", color = "all"):
	# for simplicity just one color or all

	# getting list of colors
	ctable = get_colortable()

	if color=="all":
		d = pd.concat([bob.loc[:, ctable.index.str.replace(r'\s+', "_")], bob.loc[:, 'season']], 
			axis = 1)
		if stat=="total":
			return d.groupby('season').sum()
		elif stat=="mean":
			return d.groupby('season').mean()
		else:
			sys.exit('Invalid stat argument. Use "total" or "mean", for average number of uses by season.')

	elif not any(ctable.index==color):
		sys.exit('Invalid color argument input. \
				Use "all" to see all colors or one color name (with caps!), e.g. "Dark Sienna",\
				as they appear in the data frame column called "color". \
				Check available colors with get_colortable()')

	else:
		# replacing space with _ to match actual column names
		color = re.sub(r"\s+", "_", color)
		if stat=="total":
			return bob.loc[:, ["season"]+[color]].groupby('season').sum()
		elif stat=="mean":
			return bob.loc[:, ["season"]+[color]].groupby('season').mean()
		else:
			sys.exit('Invalid stat argument. Use "total" or "mean", for average number of uses by season.')
			
# paintings_by(group = "season")





# EXAMPLE OF HOW TO USE

# load data
bob = get_bobross()

# get a random painting name
print(get_painting_names(True))

# get all painting names
print(get_painting_names())

# plot color blobs for the default painting, "Downstream View"
plot_blobs()

# plot the point cloud version
plot_cloud()

# plot color blobs for a random painting
painting = get_painting_names(True)
plot_blobs(painting)
plot_cloud(painting)



# Now you try!
# Look at some painting names
# to practice indexing

painting = get_painting_names()

# Get first 5 names 
print(painting[:5])

#  Get 5 names starting from the 3rd
# first index 0 because want to shift two spaces to the right starting from 0
print(painting[2:7])



# SUMMARIZING DATA
# Total number of times a color was used by season
print(colors_byseason(stat = "total", color = "Alizarin Crimson"))

print(colors_byseason(stat = "total", color = "all"))


# Average number of times a color was used by season
# meaning number of times used/number of total paintings in a season

print(colors_byseason(stat = "mean", color = "Alizarin Crimson"))


# Learn how to check your work!
print('\n Did he really use Alizarin Crimson every painting of season 3? \n', 
	bob.loc[bob.season==3, 'Alizarin_Crimson'])




# ADVANCED
# Python-specific syntax ok here
# Will learn: data frame and series object types

# REVISE: ONLY DEMONSTRATE .loc[[]] and .iloc methods for simplicyty, not [["asd"]]
# and maybe .loc[]

# first let's check the shape of our data frame
# **data frame** is the pandas version of a spreadsheet: it has two dimensions, with rows and columns
# type tells us what kind of object something is
# the .shape method tells us (number of rows, number of cols)
print(type(bob), bob.shape)

# look at all column names like this. these are in order, left to right
# if you were to imagine seeing the data frame in a spreadsheet
print(bob.columns)


# we can select rows and columns of a data frame using the .loc method
# bob.loc[row_index, column_label] gives you the cell in the data frame for a given index and column name
# to return all values of a column Phthalo_Green you would run
# (not printed)
bob.loc[:, 'Phthalo_Green']


# to see just the first 5 elements of the column Phthalo_Green do
print(bob.loc[:5, 'Phthalo_Green'])

# notice python starts indexing from 0, and does not include the final index number, so taht you get 5 elements here

# so bob.loc[:, 'Phthalo_Green'] is giving us a subset of our original data frame but with just one column
# each single column or single row in a data frame is called a **series**
# a series is one-dimensional. therefore .shape for a series just tells us (number of elements, )
print(type(bob.loc[:, 'Phthalo_Green']), bob.loc[:, 'Phthalo_Green'].shape)

# we can get a subset of our data frame with multiple columns by including more columns by name
print(type(bob.loc[:, ['Phthalo_Green', 'Alizarin_Crimson']]), 
	bob.loc[:, ['Phthalo_Green', 'Alizarin_Crimson']].shape)

# why do we use an extra bracket for the column names? 
# [a, b, c] is python syntax for a **list** type of object with elements a, b, c.
# so we are giving .loc a list of columns that we want

# if we want to get all of the columns between two of them, we can use a shortcut
# here we get all columns between Black_Gesso and Pthalo_Green
print(type(bob.loc[:, 'Black_Gesso':'Phthalo_Green']), 
	bob.loc[:, 'Black_Gesso':'Phthalo_Green'].shape)


# To get all of the columns *before* Black_Gesso
print(type(bob.loc[:, :'Black_Gesso']), 
	bob.loc[:, :'Black_Gesso'].shape)

# To get all of the columns *after* Phthalo_Green
print(type(bob.loc[:, 'Phthalo_Green':]), 
	bob.loc[:, 'Phthalo_Green':].shape)

# Which columns are these, even?
# Type tells us bob.loc[:, 'Phthalo_Green':] is a data frame,
# so we can use the .columns statement just as we did for teh original data frame bob
print(bob.loc[:, 'Phthalo_Green':].columns)





# GROUPWISE-SUMMARIES: 
# tutorial for grouping functionality
# https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#groupby
# Let's check the group summary functions and see how they work
# the colors have been broken out into columns already, where value 1 means it was used 0 not

# how many times was Phthalo Green used in season one?
print("\n total for season one \n", bob.loc[bob.season==1, 'Phthalo_Green'].sum())

# How many by **each season**?
# the .grouby('season') method tells the data frame bob.loc[:, ['Phthalo_Green', 'season']]
# to categorize its rows by the 'season' column values
# and the .sum() method says add up all the values of all other variables
# (only 'Phthalo_Green' in this case) **within** each group
# thereby giving the total number of paintings for which Bob Ross used this color in that season

print(bob.loc[:, ['Phthalo_Green', 'season']].groupby('season').sum())


# you could get the average by replacing sum with mean
print(bob.loc[:, ['Phthalo_Green', 'season']].groupby('season').mean())

# What about for other colors?
# The color counting columns start with Black_Gesso and end with 'Alizarin_Crimson', as we saw above
# again we use : as a shortcut to select multiple columns
# here it's easiest to sum ALL columns (columns with non-numeric info will be ignored)
# and just index as before
print(bob.groupby('season').sum().loc[:, 'Black_Gesso':])



## Plotting summarized information
# our grouped summary still returns a data frame!
# so we can use all of our data frame stuff for it!
# let's save it as a new object called gbob, to avoid recalculating every time
# use .ungroup() to tell the data frame to forget its grouping once sumamrizing is done

# as_index = False allows us to keep the season variable among the columns
# instead of turning it into a row index label
gbob = bob.groupby('season', as_index = False).sum()

print(type(gbob), gbob.shape, gbob.columns)


# let's make a bar plot of how many times Bob Ross used
# Black_Gesso in each season
# rather than, say, immediately saving it to jpeg or something

# we just give it the x-axis on the bar (season) and it plots bar values for everything else
# plt.show() just tells python to actually show us the graph 
gbob.plot.bar(x = 'season', title = 'UGLY')
plt.show()

# to limit the plot to black gesso we just get the two columns we need
# before writing .plot.bar(...) which will create the plot

gbob.loc[:, ['Black_Gesso', 'season']].plot.bar(x = 'season', title = 'Black Gesso by season')
plt.show()


# hmm, maybe this would be better as a line plot
gbob.loc[:, ['Black_Gesso', 'season']].plot.line(x = 'season', title = 'Black Gesso by season')
plt.show()


# let's look at several colors
gbob.loc[:, ['season', 'Black_Gesso', 'Yellow_Ochre', 'Phthalo_Green']].plot.line(x = 'season', title = 'Select colors by season')
plt.show()

# we can pretty this up a bit
# first let's make it bigger and probably the legend will drop into a better place
# use the argument to plot.line() called figsize, which specifies (width, height) in inches
gbob.loc[:, 
['season', 'Black_Gesso', 'Yellow_Ochre', 'Phthalo_Green']].plot.line(
	x = 'season', title = 'Select colors by season', figsize = (12, 8))
plt.show()


# Finally, let's make the colors correspond to their actual values
# For a few colors, this manual color input is a quick and simple way to do it
# Just find the hex you want using the color table I already created
# and put it as the c argument in the plot function (in the correct order)

print(get_colortable())

gbob.loc[:, 
['season', 'Black_Gesso', 'Yellow_Ochre', 'Phthalo_Green']].plot.line(
	x = 'season', 
	title = 'Turns out these colors make for poor line plots \n Also why did Bob stop using Phthalo Green? Looks too blue here.', 
	figsize = (12, 8),
	color = ['#000000', '#C79B00', '#102E3C'],
	linewidth = 4)
plt.show()



# Easily switch between plot types, changing plot.line to plot.bar
# stacked = True does the obvious

gbob.loc[:, 
['season', 'Black_Gesso', 'Yellow_Ochre', 'Phthalo_Green']].plot.bar(stacked = True,
	x = 'season', 
	title = 'Somewhat better', 
	figsize = (12, 8),
	color = ['#000000', '#C79B00', '#102E3C'],
	linewidth = 4)
plt.show()


# SAVE YOUR PICTURES!
# using the function plt.savefig

# it will interpret the file format you want to use


# for example, to save it as a pdf
# after creating your plot as above, 
# **instead of plt.show()** type plt.savefig('/pathtofile/filename.pdf')
gbob.loc[:, 
['season', 'Black_Gesso', 'Yellow_Ochre', 'Phthalo_Green']].plot.bar(stacked = True,
	x = 'season', 
	title = 'Somewhat better', 
	figsize = (12, 8),
	color = ['#000000', '#C79B00', '#102E3C'],
	linewidth = 4)
plt.savefig('/home/bb/mybobplt.pdf')

# to save it with a certain dpi, do
gbob.loc[:, 
['season', 'Black_Gesso', 'Yellow_Ochre', 'Phthalo_Green']].plot.bar(stacked = True,
	x = 'season', 
	title = 'Somewhat better', 
	figsize = (12, 8),
	color = ['#000000', '#C79B00', '#102E3C'],
	linewidth = 4)
plt.savefig('/home/bb/mybobplt.pdf', dpi=1200)

# to save as jpeg you would replace .pdf with .jpeg

# to see more options for formatting your output, type
# help(plt.savefig)


# FOR EVEN MORE PLOTTING

# the seaborn package (at the top of the file, put import seaborn as sns) has many good tools
# https://seaborn.pydata.org/index.html

# both seaborn and pandas plotting are based on the package matplotlib and matplotlib.pyplot
# we used some of this as show by the statement import matplotlib.pyplot as plt
# e.g. plt.savefig is a matplotlib.pyplot function
# but the documentation for it can be very bad, and the usage can be difficult




# HELP FOR ANY FUNCTION
# help(my_function) will give you a possibly large help file for the function my_function



# # A FOR-LOOP EXAMPLE
# For those who want to dip a toe into further programming
# A 'for' loop is a common task in all programming languages

# it tells the computer:
# for each item in a sequence
# do something

# for example, here is a loop telling python to print each item in the given list
# i is a dummy variable that stands in for a given item in the list at each iteration


for i in [1, 2, 3]:
	print(i)

# the dummy variable name is not important
for weirdname in [1, 2, 3]:
	print(weirdname)


# For loops are more useful than those examples suggest
# Let's use this to plot the painting palette cloud for a range of paintings
print(painting[2:7])

for p in painting[2:7]:
	plot_cloud(p)
