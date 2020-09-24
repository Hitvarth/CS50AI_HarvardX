on gtsrb-small
1. just one layer - almost 100% accuracy
2. added another conv layer - lesser acc

on gtsrb
1. conv-pool-conv(5x5)-pool-conv(7x7)-pool-flatten-hidden(100)-dropout(0.5) gave error lesser size and all
2. removed pool between 55 and 77 and converted 55 and 77 to 33
still the accuracy was less
3. increased the number of filters of convulutional layer
4. further increase the accuracy, removed the initial pooling layer which was unnecessarily reducing the size of the 		images which might have eliminated a lot of significant features from the image
	conv-conv-pool-conv-pool-flatten-dense(100)-drop(0.5)
5. increased a hidden layer
	conv-conv-pool-conv-pool-flatten-dense(200)-drop(0.5)-dense(100)-drop(0.2)
chose a dropout of 0.2 instead of 0.5 for the last layer so that the result depends on relatively larger number of perceptrons

6. removed an initial conv layer and increased the filters of the remaining one
	but then accuracy fell down to 70 percent

7. so added another conv layer and reduced the size of filter for the first conv layer
	acc=94%

8. increased the number of filters for the last conv layer and added a hidden layer
	but the accuracy was increasing slowy and the final accuracy for the test date was around 80%
	It is difficult to get a good accuracy within 10 epochs because there are a lot of weights that the model has to learn

9. so increased the learning rate further but no significant change

10. removed a dense layer (hidden layer) and increased the number of perceptrons in a remaining hidden layer. and reduced the learning rate
produced good results 
acc=94%

11. increased dropout and perceptrons for a dense layer

12. decreased the learning rate a bit and increased the number of filters of one of the conv layers

13. increased the filters of the first conv layer

14. increased perceptrons in dense layer acc 95%  model14

15. decreased the learning rate a bit
