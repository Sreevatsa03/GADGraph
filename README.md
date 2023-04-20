# GADGraph

## How to Use

- Run `python GAD_app.py` to start the program and open the main menu.
- Follow the prompts to use the program.

## Functionality

1. `load network` - Loads in the gene-disease graph database.

2. `gene details` - Prompts the user to input a gene id or gene symbol and then returns the full details for that gene (all of its attributes).
  
3. `disease details` - Prompts the user to input a disease id or disease symbol and then returns the full details for that disease (all of its attributes).
  
4. `subgraph` - Prompts the user for a node index and a score threshold. Returns a graph visualization in NetworkX for that node and all of the nodes with an association with a score of at least the given one. (Use gene id `24` for a good example of this.)
  
5. `common diseases` - Prompts the user to input 2 gene id's. The user can also choose to enter a score threshold for each gene when asked by answering with 'y.' It will then return the common diseases shared between the given genes and, if the user chose to input thresholds, those disease assocations will be greater than or equal to the given score thresholds.
  
6. `common genes` - Prompts the user to input 2 disease id's. The user can also choose to enter a score threshold for each disease when asked by answering with 'y.' It will then return the common genes shared between the given disease and, if the user chose to input thresholds, those gene assocations will be greater than or equal to the given score thresholds.
  
7. `network stats` - Prompts the user for a statistic action:
    1. `central genes` - Prompts the user for number of genes to return. Returns a bar chart represention and list of the most central genes.
      
    2. `central diseases` - Prompts the user for number of diseases to return. Returns a bar chart represention and list of the most central diseases.
      
    3. `high association` - Prompts the user to enter the minimum number of edges for this high association graph. Returns a visualization of the graph with the nodes with the given number of associations.
      
    4. `back` - Returns back to the main menu of possible actions.
  
8.  `quit` - User can enter this action from the main menu and it will end the program.
