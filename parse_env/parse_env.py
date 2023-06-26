#!/usr/bin/env python3

import os

if __name__ == "__main__":
    discard = ["PWD", "HOME", "LANG", "TERM", "USER", "SHLVL", "OLDPWD", "_"]

    with open("environ.sh", "w") as env_data:
        for env in os.environ:
            if env in discard:
                continue
            data = os.environ[env]
            if -1 == data.find(" "):
                env_data.write(f"export {env}={os.environ[env]}\n")
            else:
                env_data.write(f'export {env}="{os.environ[env]}"\n')
