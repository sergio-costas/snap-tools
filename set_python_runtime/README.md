# Set the correct shebang in all python files

This script checks the *shebang* in all the python scripts and replaces
it with *#!/usr/bin/env python3*. This allows to ensure that they will
always work.

The script receives the top directory as the first parameter, and will
search recursively all the files that end in .py. Whenever it finds one,
it will check the first line, and will replace it with the specified
*shebang* if all of these criteria are met:

* The file length is not zero (empty scripts won't be modified)
* It already contains a *shebang* (scripts without it won't be modified)
* The *shebang* ends in *python*, *python2* or *python3*

This script is useful when using a python installer that configures the
*shebang* using the python's runtime path while building the snap; in
those cases, the *shebang* will point to the development snap path.
For example, when using the *gnome* extension and *core22*, the *shebang*
will point to */snap/gnome-42-2204-sdk/current/usr/bin/python3*, thus
preventing the snap to run unless the *gnome-42-2204-sdk* snap is
installed.
