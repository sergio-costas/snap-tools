#!/usr/bin/env python3

""" Removes files that are already in base snaps or have been generated
    in a previous part. Useful to remove files added by stage-packages
    due to dependencies, but that aren't required because they are
    already available in core22, gnome-42-2204 or gtk-common-themes,
    or have already been built by a previous part. """

import sys
import os
import glob
import argparse
try:
    import yaml
except:
    print("YAML module not found. Please, add 'python3-yaml' to the 'build-packages' list.")
    pass

parser = argparse.ArgumentParser(prog="remove_common", description="An utility to remove from snaps files that are already available in extensions")
parser.add_argument('extension', nargs='*', default=None)
parser.add_argument('-e', '--exclude', nargs='+', help="A list of file and folders to exclude from checking")
parser.add_argument('-m', '--map', nargs='+', help="A list of snap_name:path pairs")
parser.add_argument('-v', '--verbose', action='store_true', help="Show extra info")
args = parser.parse_args()

def get_snapcraft_yaml():
    base_folder = os.environ['CRAFT_PROJECT_DIR']
    snapcraft_file_path = os.path.join(base_folder, "snapcraft.yaml")
    if not os.path.exists(snapcraft_file_path):
        snapcraft_file_path = os.path.join(base_folder, "snap", "snapcraft.yaml")
        if not os.path.exists(snapcraft_file_path):
            return None
    return snapcraft_file_path

def check_if_exists(folder_list, relative_file_path):
    """ Checks if an specific file does exist in any of the base paths"""
    for folder, map_path in folder_list:
        if (map_path is not None) and relative_file_path.starts_with(map_path):
            relative_file_path = relative_file_path[len(map_path):]
        check_path = os.path.join(folder, relative_file_path)
        if os.path.exists(check_path):
            return True
    return False


def main(base_folder, folder_list, exclude_list, verbose=False):
    """ Main function """
    duplicated_bytes = 0
    for full_file_path in glob.glob(os.path.join(base_folder, "**/*"), recursive=True):
        if not os.path.isfile(full_file_path) and not os.path.islink(full_file_path):
            continue
        relative_file_path = full_file_path[len(base_folder):]
        if relative_file_path[0] == '/':
            relative_file_path = relative_file_path[1:]
        if relative_file_path in exclude_list:
            if verbose:
                print(f"Excluding {relative_file_path}")
            continue
        if os.path.split(relative_file_path)[0] in exclude_list:
            if verbose:
                print(f"Excluding {relative_file_path}")
            continue
        if check_if_exists(folder_list, relative_file_path):
            if os.path.isfile(full_file_path):
                duplicated_bytes += os.stat(full_file_path).st_size
            os.remove(full_file_path)
            if verbose:
                print(f"Removing duplicated file {relative_file_path}")
    print(f"Removed {duplicated_bytes} bytes in duplicated files")


if __name__ == "__main__":
    folders = []

    verbose = args.verbose
    exclude = args.exclude
    extensions = args.extension
    mapping = {}

    if exclude is None:
        exclude = []
    if len(extensions) == 0:
        # get the extensions from the snapcraft file
        snapcraft_file = get_snapcraft_yaml()
        if snapcraft_file is None:
            print("Failed to get the snapcraft.yaml file. Aborting")
            sys.exit(1)
        with open(snapcraft_file, "r") as snapcraft_stream:
            snapcraft_data = yaml.load(snapcraft_stream, Loader=yaml.Loader)
        parts_data = snapcraft_data["parts"]
        extensions = []
        for part_name in parts_data:
            part_data = parts_data[part_name]
            if "build-snaps" not in part_data:
                continue
            for extension in part_data["build-snaps"]:
                if extension not in extensions:
                    extensions.append(extension)

        if len(extensions) == 0:
            print("Called remove_common.py without a list of snaps, and no 'build-snaps' entry in the snapcraft.yaml file. Aborting.")
            sys.exit(1)

    if args.map is not None:
        for map in args.map:
            elements = map.split(":")
            if len(elements) != 2:
                print(f"Error in mapping ${map}. It must be in the format snap:path")
                sys.exit(1)
            if elements[0] not in extensions:
                print(f"Warning: The mapping '{map}' points to an undefined extension")
            while elements[1][0] == '/':
                elements[1] = elements[1][1:]
            if elements[1][-1] != '/':
                elements[1] += '/'
            mapping[elements[0]] = elements[1]

    if verbose:
        print(f"Removing duplicates already in {extensions}")
    folders.append((os.environ["CRAFT_STAGE"], None))
    for snap in extensions:
        path = f"/snap/{snap}/current"
        map_path = mapping[snap] if snap in mapping else None
        folders.append((path, map_path))

    print(folders)
    install_folder = os.environ["CRAFT_PART_INSTALL"]

    main(install_folder, folders, exclude, verbose)
