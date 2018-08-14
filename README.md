# TreeSAP&nbsp;&nbsp;&nbsp;[![Build Status](https://travis-ci.org/niemasd/TreeSAP.svg?branch=master)](https://travis-ci.org/niemasd/TreeSAP)
TreeSAP: Tree SAmpling under Phylogenetic models

## Installation
TreeSAP depends on [SciPy](https://scipy.org/) and [TreeSwift](https://github.com/niemasd/TreeSwift) and can be installed via `pip`:

```bash
sudo pip install treesap
```

If you are using a machine on which you lack administrative powers, TreeSAP can be installed locally using `pip`:

```bash
pip install --user treesap
```

## Usage
```bash
from treesap import nonhomogeneous_yule_tree
tree = nonhomogeneous_yule_tree(lambda x: 2*x, end_num_leaves=100)
print(tree.newick())
```

Full documentation can be found at [https://niemasd.github.io/TreeSAP/](https://niemasd.github.io/TreeSAP/).
