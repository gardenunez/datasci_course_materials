library("methods")
library("lattice")
library("ggplot2")
library("caret")
library("rpart")
library("e1071")

#read the data
seaflow_table <- read.csv(file='seaflow_21min.csv', head=TRUE, sep=',')

#Question 1: How many particles labeled "synecho" are in the file provided?
summary(seaflow_table$pop)

#Question 2: What is the 3rd Quantile of the field fsc_small? (the summary function computes this on your behalf)
summary(seaflow_table$fsc_small, digits=12)

#Get train and test data
trainIndex = createDataPartition(seaflow_table$pop, p=0.5, list=FALSE)
training <- seaflow_table[trainIndex, ]
testing <- seaflow_table[-trainIndex, ]

#Question 3: What is the mean of the variable "time" for your training set?
mean(training$time)


#Question 4:  plot
pl <- ggplot(training, aes(x=chl_small, y=pe)) + geom_point(aes(colour=pop))
ggsave(filename='plot.jpg', plot=pl)

#Decision tree
response ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small
fol <- formula(pop ~ fsc_small + fsc_perp + chl_small + pe + chl_big + chl_small)
dt_model <-rpart(fol, method="class", data=training)

# Question 5: what populations, if any, is the tree incapable of measuring?
# Question 6: Verify there's a threshold on PE learned in the model.
# Question 7: Based on your decision tree, which variables appear to be most important in predicting the class population?
print(dt_model)

#Question 8: How accurate was your decision tree on the test data?
dt_predict <- predict(dt_model, newdata=testing, type="class")
dt_result <- dt_predict==testing$pop
summary(dt_result)

#Question 9:What was the accuracy of your random forest model on the test data?
library("randomForest")
rf_model <- randomForest(fol, data=training)
rf_predict <- predict(rf_model, newdata=testing, type="class")
rf_result <- rf_predict == testing$pop
summary(rf_result)

#Question 10:determine which variables appear to be most important in terms of the gini impurity measure.
importance(rf_model)

#Question 11: What was the accuracy of your support vector machine model on the test data?
svm_model <- svm(fol, data=training)
svm_predict <- predict(svm_model, newdata=testing, type="class")
svm_result <- svm_predict == testing$pop
summary(svm_result)

#Question 12: Confusion matrices. What appears to be the most common error the models make?
table(pred = dt_predict, true = testing$pop)
table(pred = rf_predict, true = testing$pop)
table(pred = svm_predict, true = testing$pop)

