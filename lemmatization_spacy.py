import spacy
# from terminal:  python -m spacy download en_core_web_sm

# Load the English language model
nlp = spacy.load('en_core_web_sm')

# Sample text
# text = "The dogs are barking outside."

text_file = './text_file_input.txt'

with open(text_file, 'r') as file:
    # text = file.read().lower()
    text = file.read()

# Process the text with spaCy
doc = nlp(text)

# Lemmatize each token in the text
lemmatized_text = ' '.join([token.lemma_ for token in doc])

print(lemmatized_text)
