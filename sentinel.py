#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.15"
# dependencies = []
# ///
"""Python 3.15 : sentinel, distinguer "absent" de None.

Lancer :
    uv run sentinel_demo.py
ou, directement depuis le gist :
    uv run https://gist.githubusercontent.com/zorky/462042b72641fd2633396f851006d3bd/raw/ade66af0f5cda1f41bdc916c87d468b5299232c4/sentinel_demo.py
"""

import copy
import pickle
from dataclasses import dataclass


@dataclass
class User:
    email: str | None = "old@example.com"


# --------------------------------------------------------------------------
# SANS sentinel : None sert à la fois de défaut et de valeur valide
# --------------------------------------------------------------------------
def update_user_old(user: User, email: str | None = None) -> None:
    if email is not None:
        user.email = email


# --------------------------------------------------------------------------
# AVEC sentinel (3.15) : MISSING = "non fourni", None = "effacer"
# --------------------------------------------------------------------------
MISSING = sentinel("MISSING")


def update_user_new(user: User, email: str | None | MISSING = MISSING) -> None:
    if email is not MISSING:
        user.email = email


def patch(payload: dict) -> dict:
    """Simule la vue PATCH : clé absente -> MISSING, clé à null -> None."""
    old, new = User(), User()
    update_user_old(old, email=payload.get("email"))
    update_user_new(new, email=payload.get("email", MISSING))
    return {"sans sentinel": old.email, "avec sentinel": new.email}


def main() -> None:
    print("=== PATCH ===")
    for payload in ({}, {"email": None}, {"email": "new@example.com"}):
        print(f"{payload!r:28} -> {patch(payload)}")

    print("\n=== repr ===")
    print("object()  :", object())
    print("sentinel  :", MISSING)

    print("\n=== identité conservée (copy / pickle) ===")
    print("copy      :", copy.copy(MISSING) is MISSING)
    print("deepcopy  :", copy.deepcopy(MISSING) is MISSING)
    print("pickle    :", pickle.loads(pickle.dumps(MISSING)) is MISSING)

    print("\n=== typage ===")
    print("annotation:", update_user_new.__annotations__["email"])


if __name__ == "__main__":
    main()