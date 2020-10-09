# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from nltk.tokenize import sent_tokenize, word_tokenize
import tamil, csv, re, sys
import tamil.utf8 as utf8

stats = {'total_sentences_before_processing':0, 'total_sentences_after_processing':0}


#Returns the content of a text file
def get_file_content(file_path):
    text = ""
    with open(sys.argv[1], 'r', encoding = 'utf-8') as file:
        text = file.read()
    return text

#Returns a list of sentences in order of appearance. Each sentence is a list of its words and punctuation in order of appearance.
def get_sentences(text):
    sentences = sent_tokenize(text)
    for i in range(len(sentences)): #Replace each sentence with a list of its words
        sentences[i] = word_tokenize(sentences[i])
    return sentences

#Returns true if the char is alphabetical
def is_alphabet(char):
    return char.upper().isupper()

#Returns true if the char is tamil
def is_tamil(char):
    return 2960 <= ord(char) <= 3055

#Returns true if the char is a special character
def is_special_char(char):
    return char in '|-@*&^%$#_:'

#Returns true if the char is the start of the bracket
def is_bracket(char):
    return char in '([{'

#Given a forward facing bracket in a sentence, returns the index of the next end-facing bracket. If no such bracket is found, return -1
#Precondition: front_bracket_index is the index of a forward-facing bracket in sentence, which is tokenized
def get_end_bracket(sentence, start_bracket_index):
    if sentence[start_bracket_index] == '(':
        end_bracket_type = ')'
    elif sentence[start_bracket_index] == '[':
        end_bracket_type = ']'
    elif sentence[start_bracket_index] == '{':
        end_bracket_type = '}'
    for i in range(start_bracket_index, len(sentence)):
        if sentence[i] == end_bracket_type:
            return i
    return -1

#Parse through sentence with index i for sentences without Tamil, and add the indices of sentences that do not have Tamil to sentence_remove.
def remove_sentences_without_tamil(sentences, i, sentence_remove):
    sentence_has_tamil = False
    #Mark sentences without Tamil
    for j in range(len(sentences[i])):
        for k in range(len(sentences[i][j])):
            if is_tamil(sentences[i][j][k]):
                sentence_has_tamil = True
                break
        if sentence_has_tamil:
            break
    #Delete the sentence if it has no Tamil.
    if (not sentence_has_tamil) and not i in sentence_remove:
        sentence_remove.append(i)
    return sentence_remove

#Given list "indices" of indices to remove from list, remove the elements corresponding to those indices
def remove_indices_from_list(list, indices):
    indices.reverse()
    for i in indices: #Remove all words in word_remove
        list.pop(i)
    return list


#Performs the following preprocessing of each sentence in sentences:
#   Removes any words with alphabetical characters
#   Remove words with special characters
#   Removes sentences with a length greater than 14 and less than 3 (Only counts words containing Tamil)
#   Changes numbers (with no surrounding text) to their Tamil translation
#   If end brackets are found, find the start of the bracket and remove everything in between
#   Remove sentences with no Tamil characters
#   Remove sentences containing numbers with surrounding text
def preprocess(sentences):
    sentence_remove = [] #List of sentence indexes to remove
    for i in range(len(sentences)): #Iterate over sentences
        sentence_length = 0
        word_remove = [] #List of word indexes to remove
        for j in range(len(sentences[i])): #Iterate over words
            tamil_char_count = 0 #Number of tamil characters in the word
            if sentences[i][j].isdigit(): #Check if this word is a number. If so, convert it to its Tamil translation
                sentences[i][j] = tamil.numeral.num2tamilstr_american(float(sentences[i][j]))
            for k in range(len(sentences[i][j])): #Iterate over characters
                #Removes any words with alphabetical characters, special characters, or numbers (indicating surrounding text)
                if (is_alphabet(sentences[i][j][k]) or is_special_char(sentences[i][j][k]) or sentences[i][j][k].isdigit()) and not j in word_remove:
                    word_remove.append(j)
                    break
                if is_tamil(sentences[i][j][k]): #Add to the tamil character count if the character is tamil
                    tamil_char_count += 1
            if is_bracket(sentences[i][j]): #Check if a start bracket has been found
                end_bracket_index = get_end_bracket(sentences[i], j)
                if end_bracket_index == -1: #Remove the sentence if there is no end bracket found
                    sentence_remove.append(i)
                    break
                else: #If an end bracket has been found, remove everything in between the start and end brackets
                    for k in range(j, end_bracket_index + 1):
                        if not k in word_remove:
                            word_remove.append(k)
            if tamil_char_count == len(sentences[i][j]) - 1 and (not j in word_remove) and (not i in sentence_remove): #If the word is fully Tamil, add it to the length counter and record that the sentence has tamil
                sentence_length += 1
        #Remove words with indices in word_remove from the list
        sentences[i] = remove_indices_from_list(sentences[i], word_remove)
        #Delete the sentence based on its length as calculated earlier.
        if (sentence_length > 14 or sentence_length < 3) and not i in sentence_remove:
            sentence_remove.append(i)
        #Remove sentences without Tamil
        sentence_remove = remove_sentences_without_tamil(sentences, i, sentence_remove)
    #Remove sentences with indices in sentence_remove from the list
    sentences = remove_indices_from_list(sentences, sentence_remove)
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

def main():
    if len(sys.argv) < 2:
        print("Please enter a file name.\n")
        sys.exit(1)  # abort because of error

    text = get_file_content(sys.argv[1])
    sentences = get_sentences(text)
    stats['total_sentences_before_processing'] = len(sentences)
    sentences = preprocess(sentences)
    sentences = process(sentences)
    stats['total_sentences_after_processing'] = len(sentences)

    with open('out.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([""])
        writer.writerow(["Total # of sentences before processing: ", stats['total_sentences_before_processing'], ". Total # of sentences after processing: ", stats['total_sentences_after_processing']])
        for i in range(len(sentences)):
            writer.writerow([sentences[i]])

if __name__ == "__main__":
    main()
