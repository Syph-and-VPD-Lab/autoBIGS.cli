# autoBIGS.cli

A command-line interface (CLI) based program that allows quickly batched requests for obtaining MLST profiles on multiple FASTA sequences and exporting it as a convenient CSV. Capable of querying a variety of MLST databases from both Institut Pasteur and PubMLST.

This program is simply a command-line interface for [autoBIGS.engine](https://pypi.org/project/autoBIGS.engine).

## Features

This CLI is capable of exactly what [autoBIGS.engine](https://pypi.org/project/autoBIGS.engine) is capable of:
- Import multiple whole genome FASTA files
- Fetch the available BIGSdb databases that is currently live and available
- Fetch the available BIGSdb database schemas for a given MLST database
- Retrieve exact/non-exact MLST allele variant IDs based off a sequence
- Retrieve MLST sequence type IDs based off a sequence
- Inexact matches are annotated with an asterisk (\*)
- Output all results to a single CSV

## Planned Features for CLI
- Specifications of multi-threading capacity
- Session authentication for updated database schemas (as required by both PubMLST and Institut Pasteur)

Please refer to [autoBIGS.engine](https://pypi.org/project/autoBIGS.engine) for more planned features.

## Usage

This CLI can be installed with `pip`. Please ensure [pip is installed](https://pip.pypa.io/en/stable/installation/). Then:

1. Run `pip install autoBIGS-cli` to install the latest version of the CLI for autoBIGS.

2. Once installation is complete, run `autoBIGS --version` to test that the installation succeeded (and that you are running the appropriate version).

3. Run `autoBIGS -h` to get information on how to get started.

### Example

Let's say you have a fasta called `seq.fasta` which contains several sequences. You know all sequences in `seq.fasta` are Bordetella pertussis sequences, and you know you have the sequences for the necessary targets of your schema in each of them. You want to retrieve MLST profiles for all of them. This can be done by:

1. Running `autobigs info -l` to list all available `seqdef` databases and find the database associated with Bordetella (you should see one called `pubmlst_bordetella_seqdef`).

2. Then, run `autobigs info -lschema pubmlst_bordetella_seqdef` to get the available typing schemas and their associated IDs. In this example, let's assume we want a normal MLST scheme. In this case, we would pay attention to the number next to `MLST` (it should be `3`).

3. Then, run `autobigs st -h` and familiarize yourself with the parameters needed for sequence typing.

4. Namely, you should find that you will need to run `autobigs st seq.fasta pubmlst_bordetella_seqdef 3 output.csv`. You can optionally include multiple `FASTA` files, and `--stop-on-fail` to stop typing if one of your sequences fail to retrieve any type. 

5. Sit tight, and wait. The `output.csv` will contain your results once completed.

## Versioning

the autoBIGS project follows [semantic versioning](https://semver.org/) where the three numbers may be interpreted as MAJOR.MINOR.PATCH.

Note regarding major version 0 ([spec item 4](https://semver.org/#spec-item-4)), the following adaptation of semantic versioning definition is as follows:

1. Given x.Y.z, Y is only incremented when a backwards incompatible change is made.

2. Given x.y.Z, Z is only incremented when a backwards compatible change is made.

Versions of autoBIGS items with a major version number of 0 will introduce numerous changes and patches. As such, changes between such versions should be considered highly variable.