#!/usr/bin/env python3
from nltk.tokenize import sent_tokenize, word_tokenize
import tamil, csv
import tamil.utf8 as utf8
import sys

stats = {'total_sentences_before_processing':0, 'total_sentences_after_processing':0}


#Returns the content of a text file
def get_file_content(file_path):
    text = ""
    with open(sys.argv[1], 'r', encoding = 'utf-8') as file:
        text = file.read()

    #print(text)
    text = text.replace('\ufeff', '')
    text = text.replace('\n', '')

    return text

#Returns a list of sentences in order of appearance. Each sentence is a list of its words and punctuation in order of appearance.
def get_sentences(text):
    sentences = sent_tokenize(text)
    for i in range(len(sentences) - 1, -1, -1): #Replace each sentence with a list of its words
        sentences[i] = word_tokenize(sentences[i])
    stats['total_sentences_before_processing'] = len(sentences)
    return sentences

#Performs the following preprocessing of each sentence in sentences:
#   Removes any words with alphabetical characters
#   Removes sentences with a length greater than 14 and less than 3 (Only counts words containing Tamil)
#   Changes numbers (with no surrounding text) to their Tamil translation
def preprocess(sentences):
    for i in range(len(sentences) - 1, -1, -1):
        sentence_length = 0
        for j in range(len(sentences[i]) - 1, -1, -1):
            #Check if this word contains alphabetical characters. If so, remove it
            if sentences[i][j].upper().isupper():
                sentences[i].pop(j)
                continue
            #Check if this word contains Tamil characters. If so, add it to the sentence_length counter
            has_tamil = 0
            for char in sentences[i][j]:
                if 2960 <= ord(char) <= 3055:
                    has_tamil = 1
            if has_tamil == 1:
                sentence_length += 1
            #Check if this word is a number. If so, convert it to its Tamil translation
            if sentences[i][j].isdigit():
                sentences[i][j] = tamil.numeral.num2tamilstr_american(float(sentences[i][j]))
        #Delete the sentence based on its length as calculated earlier.
        if sentence_length > 14 or sentence_length < 3:
            sentences.pop(i)
    return sentences

#Replace each set of words with a string containing the total sentence
def process(sentences):
    for i in range(len(sentences)):
        line = ""
        for j in range(len(sentences[i])):
            if sentences[i][j] in ",:.?!\';’”" or (j > 0 and sentences[i][j-1] in "‘“"):
                line = line + sentences[i][j]
            else:
                line = line + " " + sentences[i][j]
            if j == len(sentences[i]) - 1:
                line = line + "\n"
        sentences[i] = line
    return sentences

#Performs the following postprocessing of each sentence in sentences:
#   If end brackets are found, find the start of the bracket and remove everything in between
#   Remove sentences with no Tamil characters
#   Remove sentences with special characters
#   Remove sentences containing numbers with surrounding text
def postprocess(sentences):
    for i in range(len(sentences) - 1, -1, -1): #If end brackets are found, find the start of the bracket and remove everything in between
        end_bracket_location = -1
        for j in range(len(sentences[i]) - 1, -1, -1):
            end_bracket_location = sentences[i].find(')')
            if end_bracket_location != -1:
                for k in range(end_bracket_location - 1, -1, -1): #If end bracket found, search for starting bracket
                    if sentences[i][k] == '(': #If start bracket found, remove everything in between
                        sentences[i] = sentences[i][:k - 1] + sentences[i][end_bracket_location + 1:]
                        break
            else: #If no end bracket, break
                break
        #Remove sentences with no Tamil, special characters, or numbers with surrounding text
        has_tamil = 0
        for char in sentences[i]:
            if not (2960 <= ord(char) <= 3055):
                has_tamil = 1
            if 48 <= ord(char) <= 57 or char in "|-@*&^%$#_:\[\]\{\}":
                sentences.pop(i)
                has_tamil = 1
                break
        if has_tamil == 0:
            print(sentences[i])
            sentences.pop(i)
    stats['total_sentences_after_processing'] = len(sentences)
    return sentences

def main():

    if len(sys.argv) < 2:
        print("Please enter a file name.\n")
        sys.exit(1)  # abort because of error

    text = get_file_content(sys.argv[1])
    sentences = get_sentences(text)
    sentences = preprocess(sentences)
    sentences = process(sentences)
    sentences = postprocess(sentences)

    with open('out.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([""])
        writer.writerow(["Total # of sentences before processing: ", stats['total_sentences_before_processing'], ". Total # of sentences after processing: ", stats['total_sentences_after_processing']])
        for i in range(len(sentences)):
            writer.writerow([sentences[i]])

if __name__ == "__main__":
    main()
