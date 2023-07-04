# PARSE_ENV

Stores the environment variables during a build session, to allow to restore
them in a debug shell.

## Rationale

When using *snapcraft --debug*, if there is an error during any step, a shell
inside the build container will be open, to allow the developer to debug the
error.

Unfortunately, sometimes the environment gets corrupted and it's not possible
to run commands like *make*, *configure*, *ninja*... Also, sometimes we would
need to execute something in a different part than the one that failed, but
the environment is set for the current part.

Here is where *parse_env* enters: by running it just before starting the build
process, it will store in the *environ.sh* file all the current environment
variables (with some exceptions to avoid troubles). This allows to restore it
and execute any build command.

## How to use it

After installing the *snap-build-tools*, just add this in each part of your
*snapcraft.yaml* file:

    override-build: |
      $CRAFT_PROJECT_DIR/snapbuildtools/parse_env.py

Or, if you are already overriding it, put it as the first line.

Now, if there is an error and the system enters a debug shell, and the environment
is corrupted, you only have to go to the *build* folder and type:

    source environ.sh

to reload all the environment.

## Known bugs

For some reason, changing the current folder resets the environment, so in case
of doing *cd XXXX*, it is a must to run again the *source /PATH/TO/PART/BUILD/environ.sh*
command.
