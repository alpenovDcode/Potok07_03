import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('wordnet')

# Initialize the WordNet lemmatizer
lemmatizer = WordNetLemmatizer()

# Sample text
# text = "The dogs are barking outside."

text_file = './text_file_inp.txt'

with open(text_file, 'r') as file:
    # text = file.read().lower()
    text = file.read()

# Tokenize the text
tokens = word_tokenize(text)

# Lemmatize the tokens
lemmatized_text = ' '.join([lemmatizer.lemmatize(word) for word in tokens])

print(lemmatized_text)
