import pandas as pd
import re

# Read the text file and convert the text to lowercase
text_file = './text_file_inp.txt'
with open(text_file, 'r') as file:
    text = file.read().lower()

# Create a DataFrame with the text data
df = pd.DataFrame({'text': [text]})

# Define a function to clean and preprocess the text
def clean_text(text):
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Remove stopwords or other unwanted elements (you can add your custom logic here)
    # For example, removing common English stopwords
    stopwords = set(['the', 'and', 'is', 'in', 'it', 'to', 'of', 'for', 'with', 'this'])
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text

# Apply the clean_text function to preprocess the text in the DataFrame
df['cleaned_text'] = df['text'].apply(clean_text)

# Print the original text and the cleaned text
print("Original Text:")
print(df['text'].iloc[0])
print("\nCleaned Text:")
print(df['cleaned_text'].iloc[0])

with open('text_file_out_clean_text_pandas.txt', 'w') as file:
    file.write('Original Text:')
    file.write(df['text'].iloc[0])
    file.write("\nCleaned Text:\n")
    file.write(df['cleaned_text'].iloc[0])
print('Data has been written to text_file_out_clean_text_pandas.txt file.')