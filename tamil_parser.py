#!/usr/bin/env python3
from nltk.tokenize import sent_tokenize, word_tokenize
import tamil, csv
import tamil.utf8 as utf8
import sys

def main():

    if len(sys.argv) < 2:
        print("Please enter a file name.\n")
        sys.exit(1)  # abort because of error

    text = ""
    with open(sys.argv[1], 'r', encoding = 'utf-8') as file:
        text = file.read()

    #print(text)
    text = text.replace('\ufeff', '')
    text = text.replace('\n', '')

    sentences = sent_tokenize(text)

    total_sentences = len(sentences)
    sentences_gt_14 = 0
    sentences_lt_3 = 0


    for i in range(len(sentences) - 1, -1, -1): #Replace each sentence with a list of its words
        sentences[i] = word_tokenize(sentences[i])

    for i in range(len(sentences)): #Remove any words with alphabetical characters
        for j in range(len(sentences[i]) - 1, -1, -1):
            if sentences[i][j - 1].upper().isupper():
                sentences[i].pop(j - 1)

    for i in range(len(sentences) - 1, -1, -1): #Remove sentences with a length less than 1
        if len(sentences[i - 1]) < 1:
            sentences.pop(i - 1)

    for i in range(len(sentences) - 1, -1, -1): #Remove sentences with a length greater than 14 and less than 3. Only count words that contain Tamil.
        sentence_length = 0
        for j in range(len(sentences[i - 1])):
            has_tamil = 0
            for char in sentences[i - 1][j]:
                if 2960 <= ord(char) <= 3055:
                    has_tamil = 1
            if has_tamil == 1:
                sentence_length += 1
        if sentence_length > 14 or sentence_length < 3:
            sentences.pop(i - 1)
            if sentence_length > 14:
                sentences_gt_14 += 1
            if sentence_length < 3:
                sentences_lt_3 += 1

    for i in range(len(sentences)): #Change numbers to their Tamil translation
        for j in range(len(sentences[i])):
            if sentences[i][j].isdigit():
                sentences[i][j] = tamil.numeral.num2tamilstr_american(float(sentences[i][j]))

    for i in range(len(sentences)): #Replace each set of words with a string containing the total sentence
        line = ""
        for j in range(len(sentences[i])):
            if sentences[i][j] in ",:.?!\';’”" or (j > 0 and sentences[i][j-1] in "‘“"):
                line = line + sentences[i][j]
            else:
                line = line + " " + sentences[i][j]
            if j == len(sentences[i]) - 1:
                line = line + "\n"
        sentences[i] = line

    for i in range(len(sentences) - 1, -1, -1): #If end brackets are found, find the start of the bracket and remove everything in between
        end_bracket_location = -1
        for j in range(len(sentences[i - 1]) - 1, -1, -1):
            end_bracket_location = sentences[i-1].find(')')
            if end_bracket_location != -1:
                for k in range(end_bracket_location - 1, -1, -1): #If end bracket found, search for starting bracket
                    if sentences[i - 1][k] == '(': #If start bracket found, remove everything in between
                        sentences[i - 1] = sentences[i - 1][:k - 1] + sentences[i - 1][end_bracket_location + 1:]
                        break
            else: #If no end bracket, break
                break

    for i in range(len(sentences) - 1, -1, -1): #Remove sentences with no Tamil characters
        has_tamil = 0
        for char in sentences[i - 1]:
            if 2960 <= ord(char) <= 3055:
                has_tamil = 1
        if has_tamil == 0:
            sentences.pop(i - 1)

    for i in range(len(sentences) - 1, -1, -1): #Remove sentences with special characters
        for char in sentences[i - 1]:
            if char in "|-@*&^%$#_:":
                sentences.pop(i - 1)
                break

    for i in range(len(sentences) - 1, -1, -1): #Remove sentences containing numbers in a date format (after other numbers have been converted to Tamil)
        has_num = 0
        for char in sentences[i - 1]:
            if 48 <= ord(char) <= 57:
                has_num = 1
        if has_num == 1:
            sentences.pop(i - 1)

    with open('out.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([""])
        writer.writerow(["Of " + str(total_sentences) + " sentences, " + str(sentences_gt_14) + " of them contained over 14 words and were removed. " + str(sentences_lt_3) + " of them contained less than 3 words and were removed."])
        for i in range(len(sentences)):
            writer.writerow([sentences[i]])

if __name__ == "__main__":
    main()
