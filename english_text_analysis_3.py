from spellchecker import SpellChecker
import re

import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

import pandas as pd

def is_english_word(word):
    synsets = wordnet.synsets(word)
    return len(synsets) > 0

def clean_text(text):
    # Remove non-ASCII characters
    # text = ''.join([char for char in text if ord(char) < 128])

    # Remove special characters and symbols
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Clean the text from symbols of transcription
    text = re.sub(r'[0-9]', '', text)  # Remove numbers
    text = re.sub(r'[.,!?;]', '', text)  # Remove punctuation marks
    text = re.sub(' i ', '', text)  # Remove 'i's as a noise of transormations of the text
    
    return text

def generate_exceptions():
    # This function is an optional one for experiments attempting to leave some common contractions in the text.
    # It is applied in the code below, however the procedure of spellchecking clean all the contractions.
    # The words like "dont" and similar are not filtered as far they are common abbreviations of correspondent
    # contraction "don't".
    # Different stages of filtering the text could be displayed by operators 'print', which are finnaly commented
    # in the script.

    # Custom list of exceptions
    exceptions = [
        "it's",
        "I'd",
        "I'll"
        "don't"
        "didn't"
        "can't",
        "couldn't",
        "wouldn't",
        "shouldn't",
        "what's",
        "you're",
        "where's",
    ]

    # Dictionary mapping numbers to words
    numbers_to_words = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
    }
    # Generate exceptions for numbers from twenty-one to ninety-nine
    for tens_place in range(2, 10):  # For numbers from twenty to ninety
        for ones_place in range(1, 10):  # For numbers from one to nine
            if ones_place == 1:
                exceptions.append(f"{numbers_to_words[tens_place]}ty-{numbers_to_words[ones_place]}")
            else:
                exceptions.append(f"{numbers_to_words[tens_place]}ty-{numbers_to_words[ones_place]}")

    return exceptions

def clean_names(text):
    names = ("Alec", "Bob", "Hurry", "Johnny", "Dick", "Amy", "Tommy", "Harry", "James", "Mary", "Lincoln", "Arris",
         "Don", "Polly", "Teddy", "Rudyard Kipling", "Margaret", "Bobbie", "Willie", "Smith", "Robert", "Pete",
         "Charles", "Erbert", "Ted", "Nelson", "Bill", "Bobby", "Nick", "Jack", "Jane", "Andy", "Freddy", "Tom",
         "Jackie", "Jim", "Emily", "Wolf", "Brown", "Kitty", "John", "Jimmy", "England", "London", "Rome", "Monday",
         "Tuesday", "Wednesday", "Father Frost", "North", "East", "West", "English", "United States", "America",
         "French", "Mr", "Miss", "ABC")

    lowercase_names = [string.lower() for string in names]
    for string in lowercase_names:
        text = re.sub(r'\b' + re.escape(string) + r'\b', '', text)
    return text

# =-=-=-=-=-=-=-=-=-=-=-=-=-
exceptions = generate_exceptions()

# Sample text with OCR mistakes and non-English letters
# text = ("Th1s is a sample text w1th s0me OCR m1stakes and non-english letters like café. "
#         "This is a hyphenated-word and it's great. I can't say enything more. "
#         "In total there are eighty-seven")

text_file = './text_file_inp.txt'

with open(text_file, 'r') as file:
    text = file.read().lower()

# Tokenize the text into words
# tokens = re.findall(r'\b[\w\']+|[.,!?;]', text)
# Words contains letters, digits, or underscores, apostrophes, and hyphens
tokens = re.findall(r'\b[\w\'-]+|[.,!?;]', text)
# Function from NLTK library yield less words. At least 'didnt' is cleaned
# tokens = word_tokenize(text)

# print(*tokens)

# Initialize the SpellChecker
spell = SpellChecker()

# Check if each word is spelled correctly
cleaned_text = []

for token in tokens:
    if token.lower() in exceptions:
        cleaned_text.append(token)  # Preserve exceptions and include them in the final text
    elif "'" in token:
        cleaned_text.append(token)  # Preserve contractions with apostrophes
    else:
        correction = spell.correction(token)  # This line is important due to OCR mistakes. Can be ommited
        if correction is not None:
            cleaned_text.append(correction)  # Check and correct the spelling if correction is not None
        else:
            cleaned_text.append(token)  # Preserve the original token if no correction is found

# Join the cleaned words back into a single text, including exceptions
cleaned_text_spelling = " ".join(cleaned_text)

cleaned_text = clean_text(cleaned_text_spelling)

# print(cleaned_text)

# Check if each word is an English word and preserve it
english_cleaned_text = []
cleaned_text_words = cleaned_text.split()  # Split the cleaned_text into a list of words

for word in cleaned_text_words:
    if is_english_word(word):
        english_cleaned_text.append(word)

# Join the cleaned English words back into a single text
english_cleaned_text = " ".join(english_cleaned_text)
# print(english_cleaned_text)

final_cleaned_text = clean_names(english_cleaned_text)
# print(final_cleaned_text)
# print(len(final_cleaned_text))

word_list = final_cleaned_text.split()
# Create a dictionary to store the order and frequency of unique words
word_data = {}
for word in word_list:
    if word not in word_data:
        word_data[word] = 1
    else:
        word_data[word] += 1

# Count the total number of unique words
total_unique_words = len(word_data)

# Sort the word_data dictionary by frequency in descending order
sorted_word_data = {k: v for k, v in sorted(word_data.items(), key=lambda item: item[1], reverse=True)}

# Create a DataFrame from the sorted_word_data dictionary
df = pd.DataFrame(sorted_word_data.items(), columns=['Word', 'Frequency'])

# Lemmatize the words using WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
df['LemmatizedWord'] = df['Word'].apply(lambda word: lemmatizer.lemmatize(word))

def get_part_of_speech(tag):
    if tag.startswith('N'):
        return 'Noun'
    elif tag.startswith('V'):
        return 'Verb'
    elif tag.startswith('R'):
        return 'Adverb'
    elif tag.startswith('J'):
        return 'Adjective'
    elif tag.startswith('PRP'):
        return 'Pronoun'
    elif tag.startswith('RB'):
        return 'Adverb'
    elif tag.startswith('IN'):
        return 'Preposition'
    elif tag.startswith('DT'):
        return 'Determiner'
    elif tag.startswith('CC'):
        return 'Conjunction'
    elif tag.startswith('PRP$'):
        return 'Possessive Pronoun'
    elif tag.startswith('CD'):
        return 'Cardinal Number'
    elif tag.startswith('JJR'):
        return 'Adjective, comparative'
    elif tag.startswith('JJ'):
        return 'Adjective'
    else:
        return 'Other'

# Get part of speech for each word
pos_tags = pos_tag(df['Word'])
df['PartOfSpeech_NLTK'] = [get_part_of_speech(tag) for (_, tag) in pos_tags]

# additional code snippet improving getting part of speech
import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Get unique words from sorted_word_data (assuming it's already sorted by frequency)
sorted_unique_words = [word for word, _ in sorted_word_data.items()]

# Create combined_text with unique words in reverse frequency order
combined_text = ' '.join(sorted_unique_words)

# print(combined_text)

# Process the combined text with the Spacy language model
doc = nlp(combined_text)

# Initialize a list to store token text and part-of-speech tags
token_pos_list = [{'Token': token.text, 'POS': token.pos_} for token in doc]

# Create a DataFrame from the list
df_spacy = pd.DataFrame(token_pos_list)

# Merge the part-of-speech tags into a single string
df['PartOfSpeech_Spacy'] = df_spacy['POS'].fillna('').str.join(' ')

# Write the DataFrame to a CSV file
df.to_csv('text_file_out_text_analysis.csv', index=False)
print("Total unique words:", total_unique_words)

# Print a message to confirm that the data has been written to the file
print('Data has been written to the file text_file_out_text_analysis.csv.')