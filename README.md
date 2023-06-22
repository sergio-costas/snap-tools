# SNAP BUILD TOOLS

This is a set of tools useful to be used inside snapcraft.yaml to
simplify the process of snapping applications. Just add them in your
*parts* with:

      snapbuildtools:
        source: https://github.com/sergio-costas/snap-build-tools.git
        source-depth: 1
        plugin: nil
        override-pull: |
          craftctl default
          $CRAFT_PART_SRC/install

and ensure that all the other parts in your system have an

    after: [snapbuildtools]

into them to ensure that this is installed before any other part.

Once you have it, you can use any tool from any other part. For example,
to call *set_python_runtime.py* to ensure that all python scripts in the
final stage begin with the *#!/usr/bin/env python3* shebang, just do:

    $CRAFT_PROJECT_DIR/snapbuildtools/set_python_runtime.py $CRAFT_STAGE

Each tool has its own README.md explaining how to use it.

If, for some reason, there is already a folder called *snapbuildtools* in the
project dir, you can install the tools in a different folder just by
adding a folder name after *$CRAFT_PART_SRC/install*.
