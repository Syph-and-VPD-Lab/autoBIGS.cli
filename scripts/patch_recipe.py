#!/usr/bin/env python3

import argparse
from os import fdopen, path
import os
import re
import shutil
from sys import argv
import tempfile

INDENTATION = "  "
GRAYSKULL_OUTPUT_PATH = "autoBIGS.cli"
RUN_EXPORTED_VALUE = r'{{ pin_subpackage( name|lower|replace(".", "-"), max_pin="x.x") }}'
LICENSE_SUFFIX = "-or-later"
HOME_PAGE = "https://github.com/Syph-and-VPD-Lab/autoBIGS.cli"

def _calc_indentation(line: str):
    return len(re.findall(INDENTATION, line.split(line.strip())[0])) if line != "\n" else 0

def read_grayskull_output():
    original_recipe = path.abspath(GRAYSKULL_OUTPUT_PATH)
    original_meta = path.join(original_recipe, "meta.yaml")
    meta_file = open(original_meta)
    lines = meta_file.readlines()
    meta_file.close()
    return lines

def update_naming_scheme(lines):
    modified_lines = []
    for line in lines:
        matches = re.finditer(r"\{\{\s*name\|lower()\s+\}\}", line)
        modified_line = line
        for match in matches:
            modified_line = modified_line[:match.start(1)] + r'|replace(".", "-")' + modified_line[match.end(1):]
        modified_lines.append(modified_line)
    return modified_lines

def inject_run_exports(lines: list[str]):
    package_indent = False
    modified_lines = []
    for line in lines:
        indentation_count = _calc_indentation(line)
        if line == "build:\n" and indentation_count == 0:
            package_indent = True
            modified_lines.append(line)
        elif package_indent and indentation_count == 0:
            modified_lines.append(INDENTATION*1 + "run_exports:\n")
            modified_lines.append(INDENTATION*2 + "- " + RUN_EXPORTED_VALUE + "\n")
            package_indent = False
        else:
            modified_lines.append(line)
    return modified_lines

def suffix_license(lines: list[str]):
    about_indent = False
    modified_lines = []
    for line in lines:
        indentation_count = _calc_indentation(line)
        if line == "about:\n" and indentation_count == 0:
            about_indent = True
            modified_lines.append(line)
        elif about_indent and indentation_count == 1 and line.lstrip().startswith("license:"):
            modified_lines.append(line.rstrip() + LICENSE_SUFFIX  + "\n")
            about_indent = False
        else:
            modified_lines.append(line)
    return modified_lines

def inject_home_page(lines: list[str]):
    about_indent = False
    modified_lines = []
    for line in lines:
        indentation_count = _calc_indentation(line)
        if line == "about:\n" and indentation_count == 0:
            about_indent = True
            modified_lines.append(line)
        elif about_indent and indentation_count == 0:
            modified_lines.append(INDENTATION + "home: " + HOME_PAGE + "\n")
            about_indent = False
        else:
            modified_lines.append(line)
    return modified_lines

def write_to_original(lines: list[str]):
    original_recipe = path.abspath(GRAYSKULL_OUTPUT_PATH)
    original_meta = path.join(original_recipe, "meta.yaml")
    with open(original_meta, "w") as file:
        file.writelines(lines)

def rename_recipe_dir():
    new_recipe_name = path.abspath(path.join(GRAYSKULL_OUTPUT_PATH.replace(".", "-").lower()))
    shutil.rmtree(new_recipe_name, ignore_errors=True)
    os.replace(path.abspath(GRAYSKULL_OUTPUT_PATH), new_recipe_name)

if __name__ == "__main__":
    original_grayskull_out = read_grayskull_output()
    modified_recipe_meta = None
    modified_recipe_meta = update_naming_scheme(original_grayskull_out)
    modified_recipe_meta = inject_run_exports(modified_recipe_meta)
    modified_recipe_meta = suffix_license(modified_recipe_meta)
    modified_recipe_meta = inject_home_page(modified_recipe_meta)
    write_to_original(modified_recipe_meta)
    rename_recipe_dir()