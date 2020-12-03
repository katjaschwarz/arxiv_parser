# filter yesterdays publications

set -e

yesterday=$(date -d "yesterday 13:00" '+%Y-%m-%d')
kwfile='keywords.txt'

python parse.py $yesterday $kwfile
(okular "./summaries/${yesterday}.md") &

