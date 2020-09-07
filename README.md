# CodeAntiPattern_BayesianNetwork
This Github repository is implemented in python3 to find code anti-patterns based on Bayesian networks. The model is first trained on some of the classes and can then find other anti-patterns in the code. This framework can work with different bad smells and source codes. 
Here 6 different bad smells (god class, data class, feature envy, spaghetti code, complex class, and speculative generality) 
are found in 6 different java codes (Freemind, Junit, Jgraph, Jag, Jedit, and Argo).
By changing the input files, other bad smells in different source codes (and other programming languages) can also be found.

## Requirements

Install all libraries with the command: `pip3 install -r requirements.txt`
## Input file
For each code three input files are needed:
1. The .xmi of the code (this can be exported with VisualParadigm)
2. The class relations (this can be parsed with the JavaCallgraph library)
3. Excel file of some of the bad smells (datasets like Fontana or Palomba)

The input-files should be added to the `Input`-folder in `extracting_features`.

## Running the code
After adding the input-files, for converting them to the appropriate pickle-files just run
 `python3 data_creator.py` in extracting_featrues

The created pickle-files should be added to the `Pickle`-folder in `PGM_Model`.
After that, the model is trained and tested with the command: `python3 test.py`

## Changing model parameters
Based on your code you can change some parameters of the Bayesian model. In `test.py` the `test`-function gets different inputs which can change the training phrase of the model:
- The name of the Pickle-file
- Range of features for training the model (here a number between 1-8).
- The threshold of the model (between 0-1)
- Precision and Recall calculation can be either "micro", "weighted", "macro" or "None"
- If the model has to be trained with some specific features, a list can be passed to the function like [1,2] (feature 1 and 2). Otherwise [] is written (Note that the range should be 8).
- The number of folds for the K-cross-validation (Here only k=5 has been implemented).
- Dataset-type. Can be either "smells", "equal" or "None". This parameter decides if the model is just trained with the classes that have code smells or should be trained with an equal number of classes with and without smells. By choosing "none" all the data is trained.
- Bayesian model. Can be either "child", "parent" or "both"

## Output

The output of each system is an excel file that is saved in the `Output`-folder located in `PGM_Model`.

## Analyzing results

In the `Results`-folder the results of all code-runs with different parameters of the model can be found.
