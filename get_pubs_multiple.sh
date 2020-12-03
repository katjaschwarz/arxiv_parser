# filter multiple dates at once
# first argument is the start date
# second argument is the end date, if empty current date is used

set -e

kwfile='keywords.txt'

from=$(date -d "${1}" '+%Y-%m-%d')
to=$(date -d "${2}" '+%Y-%m-%d')

datum=$(date -d "$from-1 days" '+%Y-%m-%d')

while true; do
	datum=$(date -d "$datum+1 days" '+%Y-%m-%d')
	python parse.py $datum $kwfile
	
	(okular "./summaries/${datum}.md") &	
	
	if [[ "$datum" == "$to" ]]; then
	    break
  	fi
done

