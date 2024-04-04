# FoodNet: Mapping the Delicious Net
A project to visualize and detect communities within restaurants on Facebook. Data from the Network Repository. 

**Introduction**: 

Welcome to FoodNet! There are two different sets of data in this project: 
1. fb-pages-food-nodes.txt and fb-pages-food-edges.txt
2. test_nodes.txt and test_edges.txt

Set 1 is the actual data for FoodNet, corresponding to 620 different restaurants and their relationship. If the two restaurants are friends on Facebook, there exists an edge between them. 

Set 2 is a test set in similar format as FoodNet data. However, there are only 17 vertices and 27 vertices. This significantly reduces the runtime, and an appropriate graph will be produced in an instance! 

To run the program on Set 2 (test set), uncomment line 8 in main.py. It should take less than 5 seconds for the program to produce a graph. The graph will look something like this: 

![image](https://github.com/YoyoLiuuu/ArtistNetwork/assets/89408618/58ac8d80-247e-409f-b167-fde1fd573a24)

To run the program on Set 1 (actual set), comment out line 8 and uncomment line 7 in main.py. This will take a long time (4~5 min) to run, but once finished it will produce a graph like this: 

![image](https://github.com/YoyoLiuuu/ArtistNetwork/assets/89408618/42f56172-7787-4325-a11b-a7e498251f92)

In this graph, each colour represents a different community. So in this graph, we can see that there is a very big community of restaurants (light green) and some smaller communities that has less members. The colours might be different every time the graph is produced, but the structure should be similar. 


**Running the program**

To run the program, simply run main.py. This can be done by calling 'python3 main.py' in the console or run main.py with an IDE (such as PyCharm). 


**References**

Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, “Exploring network structure,
dynamics, and function using NetworkX”, in Proceedings of the 7th Python in
Science Conference (SciPy2008), G ̈ael Varoquaux, Travis Vaught, and Jarrod
Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008

Bush, Olivia. “Social Media Statistics in Canada.” Made in CA, 5 Jan. 2024,
madeinca.ca/social-media-statistics-canada

Jayawickrama, Thamindu Dilshan. “Community Detection Algorithms.” Medium,
Towards Data Science, 29 Jan. 2021, towardsdatascience.com/community-detection-
algorithms-9bd8951e7dae.

NetSci 06-2 Modularity and the Louvain Method. (2021, September 21). www.youtube.com.
https://www.youtube.com/watch?v=QfTxqAxJp0U

Rossi, Ryan A., and Nesreen K. Ahmed. “The Network Data Repository with
Interactive Graph Analytics and Visualization.” Network Data Repository, 2015,
networkrepository.com/fb-pages-artist.php.

“Software for Complex Networks.” Software for Complex Networks - NetworkX 3.2.1
Documentation, 28 Oct. 2023, networkx.org/documentation/stable/.

Stanford CS224W: Machine Learning with Graphs — 2021 — Lecture 13.3 -
Louvain Algorithm. (2021, May 25). www.youtube.com.
https://www.youtube.com/watch?v=0zuiLBOIcsw

Blondel, Vincent D, Guillaum, Jean-Loup, Lambiotte, Renaud and Lefebvre1,
Etienne Fast unfolding of communities in large networks. (2008, October 9).
https://iopscience.iop.org/article/10.1088/1742-5468/2008/10/P10008/meta

Weisstein, E. W. (n.d.). Adjacency Matrix. Mathworld.wolfram.com. Retrieved
March 31, 2024, from https://mathworld.wolfram.com/AdjacencyMatrix.html

West Health Institute Revision. “Documentation.” Documentation - Pyvis 0.1.3.1
Documentation, 2018, pyvis.readthedocs.io/en/latest/documentation.html


**Data obtained:**
  @inproceedings{nr-aaai15,
      title = {The Network Data Repository with Interactive Graph Analytics and Visualization},
      author={Ryan A. Rossi and Nesreen K. Ahmed},
      booktitle = {AAAI},
      url={http://networkrepository.com},
      year={2015}
  }
