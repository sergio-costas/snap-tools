#!/usr/bin/env python3

""" Ensures that any python script uses #!/usr/bin/env python3 """

import sys
import os
import glob

BASE_PATH = sys.argv[1]
for full_file_path in glob.glob(os.path.join(BASE_PATH, "**/*"), recursive=True):
    if not os.path.isfile(full_file_path):
        continue
    with open(full_file_path, "rb") as file_data:
        shebang = file_data.read(2)
    if shebang != b"#!":
        continue
    try:
        with open(full_file_path, "r", encoding='utf-8') as file_data:
            content = file_data.readlines()
    except:
        content = []
    if len(content) == 0:
        continue
    first_line = content[0].strip()
    if (not first_line.endswith("python") and
            not first_line.endswith("python2") and
            not first_line.endswith("python2.7") and
            not first_line.endswith("python3")):
        continue
    with open(full_file_path, "w", encoding='utf-8') as file_data:
        if first_line.endswith("python2"):
            file_data.write("#!/usr/bin/env python2\n")
        elif first_line.endswith("python2.7"):
            file_data.write("#!/usr/bin/env python2.7\n")
        else:
            file_data.write("#!/usr/bin/env python3\n")
        for line in content[1:]:
            file_data.write(line)
        print(f"Fixing file {full_file_path}")
