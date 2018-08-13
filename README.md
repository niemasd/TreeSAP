# NiHYLiSIM&nbsp;&nbsp;&nbsp;[![Build Status](https://travis-ci.org/niemasd/NiHYLiSIM.svg?branch=master)](https://travis-ci.org/niemasd/NiHYLiSIM)
NiHYLiSIM: Non-Homogeneous YuLe SIMulator

## Installation
NiHYLiSIM depends on [SciPy](https://scipy.org/) and [TreeSwift](https://github.com/niemasd/TreeSwift) and can be installed via `pip`:

```bash
sudo pip install nihylisim
```

If you are using a machine on which you lack administrative powers, NiHYLiSIM can be installed locally using `pip`:

```bash
pip install --user nihylisim
```

## Usage
```bash
from nihylisim import nonhomogeneous_yule_tree
tree = nonhomogeneous_yule_tree(lambda x: 2*x, end_num_leaves=100)
print(tree.newick())
```

Full documentation can be found at [https://niemasd.github.io/NiHYLiSIM/](https://niemasd.github.io/NiHYLiSIM/).
