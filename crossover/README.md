This directory contains plots and code to collect and analyze Harry Potter fanfiction cross-overs data from [fanfiction.net](https://www.fanfiction.net/crossovers/Harry-Potter/224/)

**Data Collection**

I have scraped and structured the data using requests and Beautiful Soup python libraries along with regex. 
The data contains 5 fandoms sharing the highest number of cross-overs with HP. Following that we collect cross-over information for each of these 5 fandoms, ie. the top 5 crossovers in these fandoms

The data contains the following columns:
`to`: the primary fandom
`from`: the crossover fandom
`num_fanfics`: number of cross over fanfictions 


**Data Visualization**

I wanted to create a network diagram to analyze the interconnectivity between these fandoms. Here, the fandoms are nodes and the node-size could potentially be the number of cross-over fanfics written about it.
for example, in 'Naruto' - 'Inyasha' the size of 'Naruto' node would be number of crossover fanfics in total written for it and node size of 'Inuyasha' would be number of crossover fanfics written for 'Inyasha-Naruto' crossover. 

I have used networkx python library with matplotlib to visualize the same. 

![Network diag](https://github.com/nt03/HarryPotter_fanfics/blob/master/crossover/xover_nodes.png)
