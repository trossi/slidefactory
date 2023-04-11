#!/usr/bin/python
#---------------------------------------------------------------------------#
# Function: Convert a presentation from Markdown (or reStructuredText) to   #
#           reveal.js powered HTML5 using pandoc.                           #
# Usage: python convert.py talk.md                                          #
# Help:  python convert.py --help                                           #
#---------------------------------------------------------------------------#
import argparse
import inspect
import os
import shlex
import sys
import subprocess
import tempfile

from pathlib import Path

slidefactory_root = Path(os.environ['SLIDEFACTORY_ROOT'])
slidefactory_is_custom = os.environ['SLIDEFACTORY_ROOT'] != '/slidefactory'


def run(run_args, *, verbose=False, dry_run=False):
    run_args = [str(a) for a in run_args]

    if verbose or dry_run:
        print(shlex.join(run_args), flush=True)

    if not dry_run:
        p = subprocess.run(run_args,
                           check=False, shell=False,
                           capture_output=True)
        if p.returncode != 0:
            print(f'error: {repr(run_args[0])} failed '
                  f'with exit code {p.returncode}',
                  file=sys.stderr, flush=True)
            print(p.stderr.decode(),
                  file=sys.stderr, flush=True)
            sys.exit(1)


def error(msg, code=1):
    """Custom error messages"""
    print('')
    print(inspect.cleandoc(msg))
    print('')
    sys.exit(code)


def find_theme(theme):
    is_custom = False
    if os.sep in str(theme):
        is_custom = True
        p = Path(theme)
        if not p.is_dir():
            error(f'Nonexistent theme directory {p.absolute()}')
    else:
        theme_root = slidefactory_root / 'theme'
        p = theme_root / theme
        if not p.is_dir():
            available_themes = [str(x.name) for x in theme_root.iterdir() if x.is_dir()]
            error(f'Invalid theme {theme}.'
                  f' Available themes: {", ".join(available_themes)}.')
    for fname in ['defaults.yaml', 'template.html', 'csc.css']:
        if not (p / fname).is_file():
            error(f'File {fname} missing from the theme directory'
                  f' {p.absolute()}')
    return p, is_custom


def create_html(input_fpath, html_fpath, args):
    # choose theme url
    theme_dpath, is_custom_theme = find_theme(args.theme)
    if is_custom_theme or slidefactory_is_custom or args.format in ['pdf', 'html-offline']:
        theme_url = f'file://{theme_dpath.absolute()}/csc.css'
    else:
        theme_url = f'https://cdn.jsdelivr.net/gh/csc-training/slidefactory/theme/{args.theme}/csc.css'

    # choose other urls
    if args.format in ['pdf', 'html-offline']:
        urls_fpath = slidefactory_root / 'urls_local.yaml'
    else:
        urls_fpath = slidefactory_root / 'urls.yaml'

    # convert
    run_args = [
        'pandoc',
        f'--defaults={theme_dpath / "defaults.yaml"}',
        f'--template={theme_dpath / "template.html"}',
        f'--metadata-file={urls_fpath}',
        f'--metadata=theme-url:{theme_url}',
        f'--output={html_fpath}',
        input_fpath,
        ]
    run_args += [f'--filter={f}' for f in args.filter]
    run(run_args, verbose=args.verbose, dry_run=args.dry_run)


def create_pdf(html_fpath, pdf_fpath, args):
    run_args = [
        args.browser,
        '--headless',
        '--disable-gpu',
        '--disable-software-rasterizer',
        '--hide-scrollbars',
        '--virtual-time-budget=10000000',
        '--run-all-compositor-stages-before-draw',
        f'--print-to-pdf={pdf_fpath}',
        f'file://{html_fpath.absolute()}?print-pdf'
        ]
    run(run_args, verbose=args.verbose, dry_run=args.dry_run)


def main():
    parser = argparse.ArgumentParser(description="""Convert a presentation
    from Markdown (or reStructuredText) to reveal.js powered HTML5 using
    pandoc.""")
    parser.add_argument('input', metavar='input.md', nargs='+', type=Path,
            help='filename for presentation source (e.g. in Markdown)')
    parser.add_argument('--output', metavar='prefix',
            help='prefix for output filenames (by default uses the '
            'basename of the input file, i.e. talk.md -> talk.html)')
    parser.add_argument('-t', '--theme', metavar='THEME', default='csc-2016',
            help=(f'presentation theme (default: %(default)s)'))
    parser.add_argument('-f', '--format', metavar='FORMAT', default='pdf',
            choices=['pdf', 'html', 'html-offline'],
            help='output format (default: %(default)s; available: %(choices)s)')
    parser.add_argument('-c', '--self-contained',
            action='store_true', default=False,
            help='produce as self-contained HTMLs as possible')
    parser.add_argument('-b', '--browser', default='chromium-browser',
            help='browser to use for converting PDFs (default: %(default)s)')
    parser.add_argument('--filter', action='append', default=[],
            metavar='filter.py',
            help='pandoc filter script (multiple allowed)')
    parser.add_argument('--dry-run', '--show-command',
            action='store_true', default=False,
            help='do nothing, only show the full commands to be run')
    parser.add_argument('--verbose', action='store_true', default=False,
            help='be loud and noisy')
    args = parser.parse_args()

    # self contained HTML
    if args.self_contained:
        urlencode = os.path.join(path['filters'], 'url-encode.py')
        if urlencode not in args.filter:
            args.filter.append(urlencode)
        contained = '--self-contained'
    else:
        contained = ''

    if args.format == 'html-offline' and not slidefactory_is_custom:
        error('Install slidefactory locally in order to create offline htmls.')

    # convert files
    for filename in args.input:
        output = filename
        if args.output:
            output = Path(args.output + str(output))

        if args.format == 'pdf':
            # use temporary html output for pdf
            with tempfile.TemporaryDirectory() as tmpdir:
                html = Path(tmpdir) / 'tmp.html'
                pdf = output.with_suffix('.pdf')
                create_html(filename, html, args)
                create_pdf(html, pdf, args)
        else:
            html = output.with_suffix('.html')
            create_html(filename, html, args)


if __name__ == '__main__':
    main()
