library(tidyverse)
library(onehot)
library(neuralnet)
rm(list = ls())

#######
setwd('') # <- set this!!!
######
u <- read.csv('upsid.R_ready.txt', sep = "\t", quote = '', encoding = 'Latin-1')
w <- read.csv('wals.R_ready.txt', sep = "\t", quote = '')
wals_index <- ncol(u) + 1
joined <- left_join(u, w, by = 'name')

# takes in a dataframe (d)
# and returns a subsetted new dataframe where the columns all match a passed
# regex
subset_by_featurename <- function(d, r, l = wals_index) {
  subset(d, select = grep(r, names(d[, 1:l])))
}

# takes a dataframe (d) and the name of a feature
# returns a one-hot MATRIX for that feature
make_onehot_df <- function(d, feature_name) {
  encoder <- onehot(d[feature_name])
  data.frame(predict(encoder, d[feature_name]))
}

# takes in a data-frame and a regex search term
# returns a new dataframe which has
# column 1: name of language
# column 2: count of all sounds in language that match passes RegEx
count_phonemes_by_regex <- function(d, r) {
  sub_d <- subset_by_featurename(d, r)
  sub_d$summed_vals <- rowSums(sub_d)
  new_d <- data.frame(d$name, sub_d$summed_vals)
  names(new_d) <- c('name', r)
  new_d
}
#########################################################



#########################################################3

vowels <- count_phonemes_by_regex(joined, 'vowel')

X <- subset_by_featurename(joined, 'vowel', wals_index)
y <- make_onehot_df(joined, 'macroarea')

d <- data.frame(X, y)

input_feats <- paste(colnames(X), collapse = ' + ')
output_feats <- paste(colnames(y), collapse = ' + ')
nn_formula <- as.formula(paste(c(output_feats, input_feats), collapse = ' ~ '))

attach(d)
nnt <- neuralnet(nn_formula, data = d, hidden = c(25), linear.output = FALSE)
res <- compute(nnt, d)
