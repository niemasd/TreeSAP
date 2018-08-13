# NiHYLiSIM
NiHYLiSIM: Non-Homogeneous YuLe SIMulator

## Installation
NiHYLiSIM can be installed via `pip`:

```bash
sudo pip install nihylisim
```

If you are using a machine on which you lack administrative powers, TreeSwift can be installed locally using `pip`:

```bash
pip install --user nihylisim
```

## Usage
```bash
from nihylisim import nonhomogeneous_yule_tree
tree = nonhomogeneous_yule_tree(lambda x: 2*x, num_leaves=100)
print(tree.newick())
```

Full documentation can be found at [https://niemasd.github.io/NiHYLiSIM/](https://niemasd.github.io/NiHYLiSIM/).
