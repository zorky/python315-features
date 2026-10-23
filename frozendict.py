#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.15"
# dependencies = []
# ///
def no_immutable_dict():
    print("no_immutable_dict()")
    config = {"host": "localhost", "port": 5432}

    config["port"] = 1                  # OK : modifié, parfois par erreur
    # cache = {config: "connexion"}       # TypeError: unhashable type: 'dict'
    # print(cache)
    print(config["port"])

def immutable_dict():
    print("immutable_dict()")
    config = {"host": "localhost", "port": 5432}
    config = frozendict(config)         # immutable, hashable

    config["port"] = 1                  # TypeError: 'frozendict' object does not support item assignment
    cache = {config: "connexion"}       # OK : hashable, immutable
    print(cache)
    print(config["port"])

if __name__=='__main__':    
    no_immutable_dict()    
    immutable_dict()
