from rake_nltk import Rake

model = Rake(min_length=1, max_length=2)

def text_to_keywords(text):
    model.extract_keywords_from_text(text)
    return model.get_ranked_phrases()