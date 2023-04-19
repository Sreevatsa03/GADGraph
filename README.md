# GADGraph

Explanation of user interactive program

User can input any of these actions and will continue to be prompted for more unless the user quits:

1. 'load network'
  Loads in the gene-disease graph database.

2. 'gene details'
  Prompts the user to input a gene id or gene symbol and then returns the full details for 
  that gene (all of its attributes).
  
3. 'disease details'
  Prompts the user to input a disease id or disease symbol and then returns the full details  
  for that disease (all of its attributes).
  
4. 'subgraph'
  Prompts the user for a node index and a score threshold. Returns a graph visualization in 
  NetworkX for that node and all of the nodes with an association with a score of at least the
  given one.
  
5. 'common diseases'
  Prompts the user to input 2 gene id's. The user can also choose to enter a score threshold 
  for each gene when asked by answering with 'y.' It will then return the common diseases 
  shared between the given genes and, if the user chose to input thresholds, those disease 
  assocations will be greater than or equal to the given score thresholds.
  
6. 'common genes'
  Prompts the user to input 2 disease id's. The user can also choose to enter a score threshold 
  for each disease when asked by answering with 'y.' It will then return the common genes 
  shared between the given disease and, if the user chose to input thresholds, those gene 
  assocations will be greater than or equal to the given score thresholds.

7. 'similar genes'
  Prompts the user to input a gene id. It will return similar genes to the given one based on 
  their overlap in disease associations.
  
8. 'network stats'
  Prompts the user for a statistic action:
    1. 'most connected genes'
      Prompts the user for number of genes to return. Will return the given number of most 
      connected genes in the graph network.
      
    2. 'most connected diseases'
      Prompts the user for number of diseases to return. Will return the given number of most 
      connected diseases in the graph network.
      
    3. 'high association graph'
      Prompts the user to enter the minimum number of edges for this high association graph. 
      Returns a visualization of the graph with the nodes with the given number of 
      associations.
      
    4. 'back'
    Returns back to the main menu of possible actions.
  
9. 'quit'
  User can enter this action at any point and it will end the program.
