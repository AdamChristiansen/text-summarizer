# Corpus¬

This corpus contains select modified documents from this [data set][1], cited
in full below.

> Pariza Sharif. BBC News Summary, version 2, 2018.
> URL https://www.kaggle.com/pariza/bbc-news-summary.
> [Online; retrieved February 25, 2019].

The data is released under the [CC0: Public Domain][2] license.

The documents and data set structure were slightly modified. The changes are:

* The directories were renamed.
* The first 20 articles and summaries from each of the 5 categories (business,
  entertainment, politics, sport, and tech) were selected.
* Each article and summary were modified so that they have one sentence per
  line.
* The articles and summaries were corrected so that every sentence that
  appears in a summary also appears in its respective article in exactly the
  same way.

The corpus is set up so that the path for a document is
`<type>/<topic>/<document>`, where:

* `<type>` is `article` or `summary`
* `<topic>` is the topic that the article-summary pair belongs to
* `<document>` is the name of the document

Using this convention, every article has a corresponding summary, so
`article/tech/001.txt` has its summary stored in `summary/tech/001.txt`.

[1]: https://www.kaggle.com/pariza/bbc-news-summary
[2]: https://creativecommons.org/publicdomain/zero/1.0/
