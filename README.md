# Python 15

Tests des nouveautés de **Python 3.15** : unpacking dans les comprehensions, imports lazy explicites et `frozendict`.

## Initialisation (uv)

Prérequis : [uv](https://docs.astral.sh/uv/) installé.\
Pour installer uv : `curl -LsSf https://astral.sh/uv/install.sh | sh`

```bash
# Créer le projet (déjà fait ici)
uv init python_15 --python 3.15
cd pythonè15

# Créer le venv et installer les dépendances
uv sync

# Basculer sur le venv
source .venv/bin/activate # source .venv/Scripts/activate

# vérifier la version python
$ python --version
Python 3.15.0
```

`pyproject.toml` impose `requires-python = ">=3.15"` : les exemples utilisent une syntaxe invalide avant 3.15.

## Exemples

Chaque exemple se lance avec `python <fichier>`.

### 1. Unpacking dans les comprehensions — [unpack.py](unpack.py)

Syntaxe `[*L for L in lists]`, `{*s for s in sets}`, `{**d for d in dicts}` :
aplatit/fusionne sans second `for`.

```bash
python unpack.py
```

| Syntaxe 3.15 | Équivalent |
|---|---|
| `[*L for L in lists]` | `[x for L in lists for x in L]` |
| `{*s for s in sets}` | `{x for s in sets for x in s}` |
| `{**d for d in dicts}` | `{k: v for d in dicts for k, v in d.items()}` |

Sortie attendue :

```
[1, 2, 3, 4, 5]
{1, 2, 3, 4}
{'a': 3, 'b': 2}
```

### 2. Imports lazy explicites — [lazy_import.py](lazy_import.py)

`lazy from unpack import list_unpack, set_unpack, dict_unpack` : le module n'est pas importé à la déclaration, mais au **premier accès** à l'un des noms.

```bash
python lazy_import.py
```

Savoir ce qui est chargé ou non :

- `"unpack" in sys.modules` : le module a été importé (une seule fois, au premier accès à un de ses noms).
- `type(globals()["set_unpack"]).__name__` : `lazy_import` = nom encore lazy, `function` = nom résolu.

Exemple : après `call_import_lazy()` (qui n'appelle que `list_unpack`), `unpack` est dans `sys.modules`, `list_unpack` est une `function`, `set_unpack` et `dict_unpack` restent `lazy_import`.

Utilitaires dans `sys` : `lazy_modules`, `get_lazy_imports()`, `set_lazy_imports()`, `set_lazy_imports_filter()`.

### 3. `frozendict` — [frozendict.py](frozendict.py)

Dict immuable et hashable (builtin en 3.15) : pas de modification accidentelle, utilisable comme clé de dict ou élément de set.

```bash
python frozendict.py
```

| | `dict` | `frozendict` |
|---|---|---|
| `d["port"] = 1` | OK | `TypeError: ... does not support item assignment` |
| `{d: "x"}` (clé) | `TypeError: unhashable type: 'dict'` | OK |

Note : `immutable_dict()` contient volontairement l'assignation `config["port"] = 1` qui lève `TypeError`. Commente-la pour voir la suite s'exécuter.

## Structure

```
.
├── pyproject.toml     # requires-python >= 3.15
├── .python-version    # 3.15
├── unpack.py          # unpacking dans comprehensions
├── lazy_import.py     # imports lazy explicites
└── frozendict.py      # dict immuable
```
