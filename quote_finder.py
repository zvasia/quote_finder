import re

import spacy


nlp = spacy.load('ru_core_news_lg')


def find_sents(doc):
    return list(doc.sents)


def get_quotes(sent):
    return re.findall(r"[«\'\"]([^\"\'«»]*)[»\'\"]", sent)


def get_quotes_and_author(content):

    doc = nlp(content)
    sentence_list = find_sents(doc)

    result = []
    for sent in sentence_list:
        sent_str = str(sent)
        quote_list = get_quotes(sent_str)
        if len(quote_list):
            author = None
            for ent in sent.ents:
                if ent.label_ == 'PER':
                    author = ent
            quotes_str = ' '.join(quote_list)
            result.append(f"{author}: {quotes_str}\n")
    return result

