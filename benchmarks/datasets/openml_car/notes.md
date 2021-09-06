## OpenML - [Car](https://www.openml.org/d/40975) 

Author: Marko Bohanec, Blaz Zupan  

Source: [UCI](https://archive.ics.uci.edu/ml/datasets/car+evaluation) - 1997  
Please cite: [UCI](http://archive.ics.uci.edu/ml/citation_policy.html)   

Car Evaluation Database  

This database was derived from a simple hierarchical decision model originally developed for the demonstration of DEX (M. Bohanec, V. Rajkovic: Expert system for decision making. Sistemica 1(1), pp. 145-157, 1990.).  

The model evaluates cars according to the following concept structure:  

CAR car acceptability 
. PRICE overall price 
. . buying buying price 
. . maint price of the maintenance 
. TECH technical characteristics 
. . COMFORT comfort 
. . . doors number of doors 
. . . persons capacity in terms of persons to carry 
. . . lug_boot the size of luggage boot 
. . safety estimated safety of the car  

Input attributes are printed in lowercase. Besides the target concept (CAR), the model includes three intermediate concepts: PRICE, TECH, COMFORT. Every concept is in the original model related to its lower level descendants by a set of examples (for these examples sets see http://www-ai.ijs.si/BlazZupan/car.html).  

The Car Evaluation Database contains examples with the structural information removed, i.e., directly relates CAR to the six input attributes: buying, maint, doors, persons, lug_boot, safety. Because of known underlying concept structure, this database may be particularly useful for testing constructive induction and structure discovery methods.  

### Changes with respect to car (1)  
The ordinal variables are stored as ordered factors in this version.   

### Relevant papers: 
M. Bohanec and V. Rajkovic: Knowledge acquisition and explanation for multi-attribute decision making. In 8th Intl Workshop on Expert Systems and their Applications, Avignon, France. pages 59-78, 1988.   

M. Bohanec, V. Rajkovic: Expert system for decision making. Sistemica 1(1), pp. 145-157, 1990.