# Python 15

Tests des nouveautés de **Python 3.15** : unpacking dans les comprehensions, imports lazy explicites, `frozendict` et `sentinel`.

## Initialisation (uv)

Prérequis : [uv](https://docs.astral.sh/uv/) installé.\
Installer uv : `curl -LsSf https://astral.sh/uv/install.sh | sh`

```bash
# Créer le projet si non déjà fait
uv init python_15 --python 3.15
cd python_15

# ou git pull
git pull git@github.com:zorky/python315-features.git python_p15
cd python_15

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

### 4. `sentinel` — [sentinel.py](sentinel.py)

Builtin `sentinel("NOM")` : valeur unique pour distinguer « non fourni » de `None` (valeur valide). Remplace l'idiome `MISSING = object()`, avec un `repr` lisible, une identité conservée par `copy` / `pickle`, et utilisable dans les annotations (`str | None | MISSING`).

Cas typique : un `PATCH` où clé absente = ne rien changer, `null` = effacer.

```python
MISSING = sentinel("MISSING")

def update_user_new(user: User, email: str | None | MISSING = MISSING) -> None:
    if email is not MISSING:
        user.email = email
```

Le script est autonome (PEP 723), il se lance avec `uv run` :

```bash
uv run sentinel.py
```

| Payload PATCH | Sans sentinel (`None` par défaut) | Avec sentinel |
|---|---|---|
| `{}` | inchangé | inchangé |
| `{"email": None}` | inchangé (**effacement impossible**) | `None` (effacé) |
| `{"email": "new@example.com"}` | `new@example.com` | `new@example.com` |

Sortie attendue (extrait) :

```
object()  : <object object at 0x...>
sentinel  : MISSING
copy      : True
deepcopy  : True
pickle    : True
annotation: str | None | MISSING
```

## Structure

```
.
├── pyproject.toml     # requires-python >= 3.15
├── .python-version    # 3.15
├── unpack.py          # unpacking dans comprehensions
├── lazy_import.py     # imports lazy explicites
├── frozendict.py      # dict immuable
└── sentinel.py        # sentinel : absent vs None
```
