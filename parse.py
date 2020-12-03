import argparse
import urllib.request
import feedparser
import datetime
import re
import os

from utils import get_date, entries_on, contains, clean_whitespaces, write_in_color


if __name__ == '__main__':
    # Arguments
    parser = argparse.ArgumentParser(
        description='Parse cs.CV entries from arxiv.'
    )
    parser.add_argument('date', type=str, help='date from which articles are parsed, format: yyyy-mm-dd')
    parser.add_argument('keyword_file', type=str,
                        help='.txt file containing the keywords')

    args = parser.parse_args()

    # configs
    output_dir = 'summaries'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, '%s.md' % args.date)
    log_file = os.path.join(output_dir, '.log_%s.txt' % args.date)
    with open(output_file, 'w') as f:           # create empty file and add header
        f.write(write_in_color('Filtered arxiv publications from %s' % args.date, 'grey') + '\n\n\n\n')

    # read keywords from file
    keywords = []
    flaglist = []
    with open(args.keyword_file, "r") as f:
        for line in f:
            if line.startswith('#') or line == '\n':        # ignore comments and empty lines
                continue

            flag = []
            if line.endswith('*c*\n'):
                line = line[:-5]
            else:
                flag.append(re.IGNORECASE)

            keywords.append(line.strip())
            flaglist.append(flag)

    # save used keywords to log file
    with open(log_file, 'w') as f:
        f.write(', '.join(keywords))

    # date for which to get publications
    date = [int(n) for n in args.date.split('-')]
    date = datetime.datetime(*date, minute=0, hour=0, second=0, microsecond=0)

    # Base api query url
    base_url = 'http://export.arxiv.org/api/query?';

    # Search parameters
    search_query = 'cat:cs.CV'  # cs.CV mailing list
    start = 0  # retreive the first n results
    max_results = 100
    # TODO: adjust start value to enabling starting from far in the past

    print('Search for papers from %s...' % str(date))
    while True:
        query = 'search_query=%s&' \
                'start=%i&' \
                'max_results=%i&' \
                'sortBy=submittedDate&' \
                'sortOrder=descending' % (search_query, start, max_results)

        # Opensearch metadata such as totalResults, startIndex,
        # and itemsPerPage live in the opensearch namespase.
        # Some entry metadata lives in the arXiv namespace.
        # This is a hack to expose both of these namespaces in
        # feedparser v4.1
        feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
        feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

        # perform a GET request using the base_url and query
        response = urllib.request.urlopen(base_url + query).read()

        # parse the response using feedparser
        feed = feedparser.parse(response)

        if get_date(feed.entries[-1]) < date:
            break

        max_results += 100

    feed.entries = entries_on(feed.entries, date)

    print('Found %d papers.' % len(feed.entries))

    # Run through each entry, and filter for keywords
    for entry in feed.entries:
        abstract, title = entry.summary, entry.title

        matches = set(contains(title, keywords, flaglist) + contains(abstract, keywords, flaglist))
        if len(matches) == 0:
            continue

        authors = ', '.join(author.name for author in entry.authors)

        with open(output_file, 'a') as f:
            f.write('## %s \n\n' % clean_whitespaces(title))
            f.write('%s \n\n' % authors)
            f.write('###' + write_in_color('Keywords: ' + ', '.join(matches), 'gray') + '\n\n')
            f.write(abstract + '\n\n')

        # get the links to the abs page and pdf for this e-print
        for link in entry.links:
            if link.rel == 'alternate':
                with open(output_file, 'a') as f:
                    f.write('abs page link: %s' % link.href + '\n\n')
            elif link.title == 'pdf':
                with open(output_file, 'a') as f:
                    f.write('pdf link: %s' % link.href + '\n\n')

