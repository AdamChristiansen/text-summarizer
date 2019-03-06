import argparse
import os

from utils import color as clr
from utils import doc
from utils import error
from utils import fs
from utils import text

#------------------------------------------------------------------------------
# Parse command line arguments
#------------------------------------------------------------------------------

parser = argparse.ArgumentParser(
        description='Preprocess article and summary data.')
parser.add_argument('output_dir', type=str,
        help='The directory which to write the output data')
parser.add_argument('corpus_dir', type=str,
        help='The directory which contains the corpus')
args = parser.parse_args()

# Get the command line arguments in a usable form
OUTPUT_DIR = os.path.abspath(args.output_dir)
CORPUS_DIR = os.path.abspath(args.corpus_dir)

ARTICLE_DIR = os.path.join(CORPUS_DIR, 'article')
SUMMARY_DIR = os.path.join(CORPUS_DIR, 'summary')

# The topics to be covered are the subdirectories of `ARTICLE_DIR` and
# `SUMMARY_DIR` to process.
TOPICS = fs.symmetric_dir_contents(ARTICLE_DIR, SUMMARY_DIR, dirs=True)

# Create the ouput directory
fs.make_dir(OUTPUT_DIR)

#------------------------------------------------------------------------------
# Process each file
#------------------------------------------------------------------------------

# Iterate over every file to process in the corpus
for topic in TOPICS:
    # The directories that the articles and summaries are in
    ARTICLE_TOPIC_DIR = os.path.join(ARTICLE_DIR, topic)
    SUMMARY_TOPIC_DIR = os.path.join(SUMMARY_DIR, topic)

    files_to_process = sorted(fs.symmetric_dir_contents(ARTICLE_TOPIC_DIR,
        ARTICLE_TOPIC_DIR, files=True))
    for filename in files_to_process:
        # The paths to the files used
        article = os.path.join(ARTICLE_DIR, topic, filename)
        summary = os.path.join(SUMMARY_DIR, topic, filename)
        outname = f"{topic}_{os.path.splitext(filename)[0]}.json"
        outfile = os.path.join(OUTPUT_DIR, outname)

        # The document to write the data to
        document = doc.Document()
        document.topic = topic

        # Load the article
        with open(article) as f:
            original = f.read()
            document.orig_article = original
            lines = text.split_sentence(original)
            document.title = lines[0]
            document.sent_orig_article = lines[1:]

        # Load the summary
        with open(summary) as f:
            original = f.read()
            document.orig_summary = original
            document.sent_orig_summary = text.split_sentence(original)

        # Make sure that every sentence in the summary is also present in the
        # article
        sentence_pool = set(document.sent_orig_article)
        for sentence in document.sent_orig_summary:
            if sentence not in sentence_pool:
                print(f"Summary {clr.blu(summary)} has the sentence:")
                print(f"    {clr.red(sentence)}")
                print(f"which does not appear in article {clr.blu(article)}.")
                print()

        # Write the file
        document.dump_file(outfile)
