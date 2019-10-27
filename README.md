# manage_chessella-PY

Scripts to manage the chessella site (http://www.chessella.com)

## STEPS


Replace <YYYY-MM-DD> with current data

First retrieves the links from chessbase that are not processed yet
```
python collect_links_from_chessbase.py --out=<YYYY-MM-DD>.lst 
```

Then saves in the `from_cbase` directory the pgn files

```
python retrieve_from_chessbase.py --fileLink=chessbase_links/<YYYY-MM-DD>.lst
```

The biggest file without comments must be moved from `from_cbase` to `uncommented`
Otherwise you can use `clean_raw_files.py` to process files in `from_cbase_raw` and move them to `work`

Move files from `from_cbase` and from `work` into the server that will move files to chessella.

After that move files from `from_cbase` to `onserver` and from `from_cbase_raw` to `processed`