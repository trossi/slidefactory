# slidefactory

Generate lecture slides in CSC style from markdown (or reStructuredText).


## Usage

Convert slides from Markdown to HTML:
```bash
./slidefactory.sif example/example.md
```

Convert slides from Markdown to HTML and PDF:
```bash
./slidefactory.sif -p example/example.md
```

Use specific theme (see `./slidefactory -h` for available themes):
```bash
./slidefactory.sif -t csc-2023 -p example/example.md
```


## Install

Slidefactory container image is available in github container registry:
```bash
singularity pull slidefactory.sif docker://...
```


### Uninstall

To uninstall slidefactory, just remove the container image
```bash
rm slidefactory.sif
```


# Markdown file syntax

Every slide set should start with a metadata block (see [Syntax
Guide](docs/syntax-guide.md) for details) followed by slides in Markdown
syntax (Pandoc prefers Commonmark, but understands also other flavours).

Slides are separated by using first-level headers.

Even though Pandoc understands most flavours of Markdown syntax (and is quite
good in handling minor differences), to avoid conversion errors, it is a good
idea to be a bit picky about whitespaces etc. and to aim for consistent
syntax.

Please look at [example/example.md](example/example.md) for an example.


# Importing an existing presentation

In order to import an existing presentation, you need to:
1. convert all texts (bullet points, source code etc.) into Markdown syntax
2. convert all figures into separate files (e.g. into PNGs or SVGs)

If you want to convert a Powerpoint presentation, please see
[some tips for converting a Powerpoint](docs/import-powerpoint.md).

