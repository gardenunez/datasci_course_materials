library("methods")
library("lattice")
library("ggplot2")
library("caret")
library("e1071")



#read the data
seaflow_table <- read.csv(file='seaflow_21min.csv', head=TRUE, sep=',')



# Question 13: We assumed variables were continuous.
plot(seaflow_table$chl_big, seaflow_table$chl_small)
plot(seaflow_table$fsc_big, seaflow_table$fsc_small)
plot(seaflow_table$fsc_perp, seaflow_table$pe)


# Question 14.

trainIndex = createDataPartition(seaflow_table$pop, p=0.5, list=FALSE)
training <- seaflow_table[trainIndex, ]
testing <- seaflow_table[-trainIndex, ]
fol <- formula(pop ~ fsc_small + fsc_perp + chl_small + pe + chl_big + chl_small)

svm_model <- svm(fol, data=training)
svm_predict <- predict(svm_model, newdata=testing, type="class")
svm_result <- svm_predict == testing$pop
summary(svm_result)

table2 = subset(seaflow_table, seaflow_table$file_id != 208)
trainIndex2 = createDataPartition(table2$pop, p=0.5, list=FALSE)
training2 <- table2[trainIndex2, ]
testing2 <- table2[-trainIndex2, ]

new_svm_model = svm(fol, data=training2)
new_svm_predict = predict(new_svm_model, newdata=testing2)
new_svm_result = new_svm_predict == testing2$pop
summary(new_svm_result)

