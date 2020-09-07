# CodeAntiPattern_BayesianNetwork
This github repositery is implemented in python3 to find code anti-patterns based on bayesian networks. The model is first trained on some of the classes and can then find other anti-patterns in the code. This framework can work with different bad smells and source codes. 
Here 6 different bad smells (god class, data class, feature envy, spaghetti code, complex class and speculative generality) 
are found in 6 different java codes (freemind, junit, jgraph, jag, jedit and argo) .
By changing the input files, other bad smells in different source codes (and other programming languages) can also be found.

## Requirements

Install all libraries with the command: `pip3 install -r requirements.txt`
## Input file
For each code three input files are needed:
1. The xmi of the code (this can be exported with VisualParadigm)
2. The class relations (this can be parsed with the JavaCallgraph library)
3. Excel file of some of the bad smells (datasets like Fontana or Palomba)
The input files should be added to the `Input` -Folder in `extracting_features`.
