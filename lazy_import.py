import sys
lazy from unpack import list_unpack, set_unpack, dict_unpack
# from unpack import list_unpack, set_unpack, dict_unpack

def call_list_unpack_import_lazy():
    list_unpack()

def lazy_status() -> dict[str, bool]:
    """
    Affiche le statut de chargement des fonctions du module unpack.

    Avec lazy
    module unpack chargé : True
    {'list_unpack': True, 'set_unpack': False, 'dict_unpack': False}
    
    Sans lazy
    module unpack chargé : True
    {'list_unpack': True, 'set_unpack': True, 'dict_unpack': True}

    """
    names = ("list_unpack", "set_unpack", "dict_unpack")
    return {n: type(globals()[n]).__name__ != "lazy_import" for n in names}

def display_module_status():
    print("module unpack chargé :", "unpack" in sys.modules)
    print(lazy_status())  # True = chargé, False = encore lazy

if __name__=='__main__':
    call_list_unpack_import_lazy()
    display_module_status()
    
