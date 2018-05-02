## calibre-dupescan

Scans [Calibre](https://calibre-ebook.com) libraries for duplicates by case
insensitive comparison of directory names ignoring numerical suffixes. Potential
duplicates are printed in pairs of directory paths. Separators and quoting are
configurable using options, so the output can be CSV or easily fed to utilities
like 'awk' for further processing.

```
usage: calibre-dupescan.py [-h] [-qs QS] [-qe QE] [-s S]
                           directory [directory ...]

Find duplicates in Calibre library directories.

positional arguments:
  directory

optional arguments:
  -h, --help  show this help message and exit
  -qs QS      Start quote string (default: ")
  -qe QE      End quote string (default: ")
  -s S        Separator string (default: Tabulator)

$ cd /my/calibre/library
$ calibre-dupescan.py -s :: Dostoyevsky Shakespeare
"Dostoyevsky/The Brothers Karamazov (123)"::"Dostoyevsky/The Brothers Karamazov (456)"
```
