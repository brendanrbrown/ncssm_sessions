library(readr)
library(dplyr)
library(ggplot2)
library(rlang)
library(purrr)
library(stringr)
library(mvtnorm)

# BB'S RULES FOR HIMSELF
# never more than 2 args
# always character, quoted arguments (for python compatibility, in case we use)
# just enough functionality to have fun, never enough for mischief
# Reconcile TRUE with True and FALSE with False

# HELPERS
get_bobross <- function(){
  # CHANGE FILEPATH TO GITHUB SITE
  bob <- read_csv("./data/Bob_Ross_Paintings/data/bob_ross_paintings.csv") %>%
  mutate(color_hex = str_replace_all(color_hex, "[\\[\\s\\]']", "") %>% str_split(., ","),
         # uppercase hex causes problems for ggplot2?
         color_hex = map(color_hex, tolower),
         colors = str_replace_all(colors, "[\\[\\]']|\\\\r|\\\\n", "") %>% str_split(., ","),
         colors = map(colors, str_trim))
}

get_help <- function(){
  # TODO
  # help file for students who forget usage
  # either with one argument, bare unquoted function name, to print usage for that fun
  # or no arguments to print all
}


# VIEW DATA
get_painting_names <- function(random = FALSE){
  # error rather than calling the fun as teaching moment
  if (!exists("bob", .GlobalEnv))
    stop("You haven't loaded the dataset! Run get_bobross() first.")
  
  if (!is.logical(random))
    if (as_string(enexpr(random)) == "True"){
      random <- TRUE
      warning("We're using R! Use TRUE next time. In Python use True.")
    } else if (as_string(enexpr(random)) == "False"){
      random <- FALSE
      warning("We're using R! Use FALSE next time. In Python use False.")
    } else {
      stop("Invalid argument for random. Should be TRUE or FALSE. Run get_help().")
    }
  
  if (random)
    sample(bob$painting_title, 1)
  else
    bob$painting_title
}

plot_blobs <- function(painting="Downstream View"){
  if (!exists("bob", .GlobalEnv))
    stop("You haven't loaded the dataset! Run bob = get_bobross() first.")
  if (!is.character(painting))
    stop("painting_title must be the name of a painting in quotations. Run get_help().")
  
  d <- filter(bob, painting_title == painting)
  blobd <- bind_rows(d$blob[[1]], .id='color') %>% 
    mutate(color = d$colors[[1]],
            x = runif(n(), min = -8, max = 8),
            y = runif(n(), min = -8, max = 8))
  
  ggplot(blobd, aes(x, y, color = color)) + geom_point(alpha = .7, size = 35) +
    theme_void() + scale_color_manual(values = d$color_hex[[1]]) +
    theme(legend.position="none") +
    annotate('text', x = blobd$x, y = blobd$y,
             label = blobd$color, size = 3, color = 'grey20') +
    xlim(-1.3*8, 1.3*8) + ylim(-1.3*8, 1.3*8) +
    ggtitle(label = painting)
}



# ADVANCED
# R-specific syntax OK here





# EXAMPLES OF HOW TO USE

# load data
bob = get_bobross()

# get a random painting name
print(get_painting_names(True))

# get all painting names
print(get_painting_names())


# plot color blobs for the default painting, "Downstream View"
plot_blobs()

# plot color blobs for a random painting
plot_blobs(get_painting_names(True))