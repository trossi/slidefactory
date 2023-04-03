#!/bin/sh

# Default arguments
do_pdf=
theme="csc-2023"

# Parse arguments
while getopts "hpt:" name; do
    case "$name" in
        p)
            do_pdf=1;;
        t)
            theme="$OPTARG";;
        h|?)
            printf "Usage: %s: [-p] [-t theme] file.md\n" $0
            exit 2;;
    esac
done
shift $(($OPTIND - 1))

theme_dpath="$SLIDEFACTORY_THEME_ROOT/$theme"

# Convert files
for fpath in "$@"; do
    html_fpath=${fpath%.*}.html
    echo "Converting $fpath to $html_fpath"
    pandoc -d "$theme_dpath/defaults.yaml" --template="$theme_dpath/template.html" -o "$html_fpath" "$theme_dpath/settings.yaml" "$fpath"
    if [ $? -eq 0 ] && [ ! -z "$do_pdf" ]; then
        pdf_fpath=${fpath%.*}.pdf
        echo "Converting $html_fpath to $pdf_fpath"
        node /decktape/decktape.js --chrome-path chromium-browser --chrome-arg=--no-sandbox "$html_fpath" "$pdf_fpath" > /dev/null
    fi
done
