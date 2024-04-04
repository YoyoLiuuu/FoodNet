# FoodNet: Mapping the Delicious Net
A project to visualize and detect communities within restaurants on Facebook. Data from the Network Repository. 

**Introduction**: 

Welcome to FoodNet! There are two different sets of data in this project: 
1. fb-pages-food-nodes.txt and fb-pages-food-edges.txt
2. test_nodes.txt and test_edges.txt

Set 1 is the actual data for FoodNet, corresponding to 620 different restaurants and their relationship. If the two restaurants are friends on Facebook, there exists an edge between them. 

Set 2 is a test set in similar format as FoodNet data. However, there are only 17 vertices and 27 vertices. This significantly reduces the runtime, and an appropriate graph will be produced in an instance! 

To run the program on Set 2 (test set), uncomment line 8 in main.py. It should take less than 10 seconds for the program to produce a graph. The graph will look something like this: 

![image](https://github.com/YoyoLiuuu/ArtistNetwork/assets/89408618/58ac8d80-247e-409f-b167-fde1fd573a24)

To run the program on Set 1 (actual set), comment out line 8 and uncomment line 7 in main.py. This will take a very long time (10+ min) to run, but once finished it will produce a graph like this: 

![image](https://github.com/YoyoLiuuu/ArtistNetwork/assets/89408618/42f56172-7787-4325-a11b-a7e498251f92)

In this image, each colour represents a different community. So in this graph, we can see that there is a very big community of restaurants (light green) and some smaller communities that has less members. 

**Running the program**
