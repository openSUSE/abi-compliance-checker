#!/usr/bin/env python3

from glob import glob

import os
import shutil
import subprocess
import sys

EXECUTABLE_NAME = "abi-compliance-checker"


def has_extension(filename, *extensions):
    expanded_extensions = list(extensions) + list(
        map(lambda ext: ext.upper(), extensions)
    )

    valid = [filename.endswith(ext) for ext in expanded_extensions]
    if not any(valid):
        return False

    return True


def generate_xml(version, directory):
    headers = set()
    shared_objects = set()

    filenames = glob(os.path.join(directory, "**"), recursive=True)
    for filename in filenames:
        if has_extension(filename, ".h", ".hpp"):
            headers.add(filename)

        if has_extension(filename, ".so"):
            shared_objects.add(filename)

    headers = "\n".join(headers)
    shared_objects = "\n".join(shared_objects)

    output = f"<version>{version}</version>"
    output = f"{output}\n<headers>\n{headers}\n</headers>"
    output = f"{output}\n<libs>\n{shared_objects}\n</libs>"

    return output


def main():
    executable = shutil.which(EXECUTABLE_NAME)
    if not executable:
        print(f"{EXECUTABLE_NAME} not installed")
        sys.exit(1)

    try:
        name = sys.argv[1]
        v1, v1_dir = sys.argv[2], sys.argv[3]
        v2, v2_dir = sys.argv[4], sys.argv[5]
    except IndexError:
        print("Usage: <package name> <v1> <v1 directory> <v2> <v2 directory>")
        sys.exit(1)

    print(f"Found executable: {executable}")
    print(f"Comparing: {v1} -> {v2}")
    print(f"Directory for {v1}: {v1_dir}")
    print(f"Directory for {v2}: {v2_dir}")

    v1_xml_filename = f"{v1}.xml"
    with open(v1_xml_filename, "w") as handle:
        print(f"Creating: {v1_xml_filename}")
        handle.write(generate_xml(v1, v1_dir))

    v2_xml_filename = f"{v2}.xml"
    with open(v2_xml_filename, "w") as handle:
        print(f"Creating: {v2_xml_filename}")
        handle.write(generate_xml(v2, v2_dir))

    subprocess.run(
        [executable, "-lib", name, "-old", v1_xml_filename, "-new", v2_xml_filename]
    )


if __name__ == "__main__":
    main()
