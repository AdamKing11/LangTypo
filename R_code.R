library(tidyverse)
library(onehot)
library(neuralnet)
rm(list = ls())
u <- read.csv('~/Desktop/mike_nn/assignment2/LangTypo/upsid.R_ready.txt', sep = "\t", quote = '', encoding = 'Latin-1')
w <- read.csv('~/Desktop/mike_nn/assignment2/LangTypo/wals.R_ready.txt', sep = "\t", quote = '')

u_nonames <- u[,2:ncol(u)]

l <- w[c('name', 'macroarea')]

encoder <- onehot(l['macroarea'])
p <- predict(encoder, l)

n_labels <- ncol(p)
d <- data.frame(p, u_nonames)

output_feats <- paste(colnames(d[, 1:n_labels]), collapse = ' + ')
input_feats <- paste(colnames(d[, (n_labels+1):ncol(d)]), collapse = ' + ')
f <- as.formula(paste(c(output_feats, input_feats), collapse = ' ~ '))

attach(d)
nnt <- neuralnet(f, data = d[1:370], hidden = c(10), linear.output = FALSE)
res <- compute(nnt, d[371:380,1:n_labels])
d$'1' <- 1
d$"iH"

d[c('uh')]
