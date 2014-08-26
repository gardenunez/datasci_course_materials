library("methods")
library("lattice")
library("ggplot2")
library("caret")
library("ggplot2")

#Question 1: Read the data
seaflow_table <- read.csv(file='seaflow_21min.csv', head=TRUE, sep=',')
summary(seaflow_table$pop)

#Question 2: Split the dataset in train and test data
training = createDataPartition(seaflow_table$pop, p=0.5, list=FALSE)
trainPredictors <- seaflow_table[training, ]
testPredictors <- seaflow_table[-training, ]

#Question 3: Now we plot
pl <- ggplot(trainPredictors, aes(x=chl_small, y=pe)) + geom_point(aes(colour=pop))
ggsave(filename='plot.jpg', plot=pl)


