# pyner
Python NER utility


## install dependecies
    pip install -r requirements.txt

## Stanford's NER dependency

[Download Stanfoard's NER library](https://nlp.stanford.edu/software/CRF-NER.shtml#Download).  Unzip to `stanford_ner` folder wherever you clone this repository.

## Initialize NLTK with Stanford NER

    from nltk.tag.stanford import StanfordNERTagger
    # init Stanford NER with NLTK 
    st = StanfordNERTagger('./stanford_ner/classifiers/english.all.3class.distsim.crf.ser.gz','./stanford_ner/stanford-ner.jar')

You can then analyze documents with the `TaggedDoc` class from `pyner.py`.

    doc = TaggedDoc(FILE_PATH, is_file=True)
    doc.analyze()
    doc.tags() # returns tags, grouped

Optionally, you can also pass a function to filter/clean tags before returning from `.analyze()`, a la:

    def tag_cleaner_example(tags):
        # loop through to remove instances of "kodak"
        tags[:] = [tag for tag in tags if 'kodak' not in tag[0].lower()]
        tags[:] = [tag for tag in tags if 'color control patches' not in tag[0].lower()]
        # loop through and remove trailing puncuation
        for tag in tags:
            tag = (tag[0].rstrip("."), tag[1])
            tag = (tag[0].rstrip(","), tag[1])
        # remove dupes and return
        return list(set(tags))

    doc.analyze(tag_filter = tag_cleaner_example)


