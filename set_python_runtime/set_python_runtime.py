#!/usr/bin/env python3

""" Ensures that any python script uses #!/usr/bin/env python3 """

import sys
import os
import glob

BASE_PATH = sys.argv[1]
for full_file_path in glob.glob(os.path.join(BASE_PATH, "**/*.py"), recursive=True):
    if not os.path.isfile(full_file_path):
        continue
    with open(full_file_path, "r", encoding='utf-8') as file_data:
        content = file_data.readlines()
    if len(content) == 0:
        continue
    if content[0][:2] != '#!':
        continue
    if (not content[0].endswith("python") and
            not content[0].endswith("python2") and
            not content[0].endswith("python3")):
        continue
    with open(full_file_path, "w", encoding='utf-8') as file_data:
        file_data.write("#!/usr/bin/env python3\n")
        for line in content[1:]:
            file_data.write(line)
