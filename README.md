# arxiv_parser

Basic tool using arxiv API to filter the latest publications on arxiv from cs.CV mailing list.

### Requirements

Make sure to use feedparser version 5.x, e.g. by running
```
conda install -c anaconda feedparser
```
The code uses `okular` for displaying the `.md` output files 
but you can view them with the document viewer of your choice, e.g. `vim`.
If you do not use `okular` simply comment out the corresponding lines in `get_pubs.sh` and `get_pubs_multiple.sh`.

### Usage

Start by entering your custom keywords in `keywords.txt`.

Then you can filter yesterday's publications by running
```
./get_pubs.sh
```
This creates a folder `summaries` and creates a file `./summaries/YYYY-MM-DD.md` with the summary of 
yesterday's filtered publications.

For processing multiple dates you can run
```
./get_pubs_multiple.sh FROM TO
```
where `FROM` is the earliest date in the format `YYYY-MM-DD`. `TO` (same format) is the latest date. 
It is optional and defaults to the current date.
Note, that values for `FROM` from more than a few days ago currently make the code very slow.