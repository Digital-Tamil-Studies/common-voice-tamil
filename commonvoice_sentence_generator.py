#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import pandas as pd
import nltk
import tamil
import re
import os
import glob
from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation
nltk.download('punkt')


# In[2]:


# Symbols list that needs to be removed from sentences
special_symbols = set(punctuation)
special_symbols.remove("!")
special_symbols.remove(",")
special_symbols.remove("?")
special_symbols.remove(".")
special_symbols.add("”")
special_symbols.add("“")
special_symbols.add("‘")
special_symbols.add("’")
special_symbols.add("★")


# In[3]:


# Sentence word length range
MIN_WORDS_LENGTH = 3
MAX_WORDS_LENGTH = 14


# In[4]:


# gets path to the text file, cleans it according to rule and returns stats and valid sentences
def get_commonvoice_sentences(text_file_path, work_title):
    stats = {'work_title': work_title}
    text = get_file_content(text_file_path)
    sentences = sent_tokenize(text)
    
    # Drop book's standard headers and footers
    sentences = drop_header_and_footers(sentences)
    stats['total_sentences_before_processing'] = len(sentences)
    
    valid_sentences = []
    for sentence in sentences:
        # Remove any words within brackets
        sentence = re.sub('\(.*?\)','', sentence)
        
        # Remove extra white spaces
        sentence = re.sub("\s\s+", " ", sentence)

        # Remove special chracters
        sentence_without_symbols = remove_special_characters(sentence, special_symbols)

        # Drop sentences if they contain English characters
        result =  bool(re.search("[a-zA-Z]", sentence_without_symbols))
        if result == True:
            continue
                
        # Drop sentences if they contain number within a word
        sentence_without_symbols = convert_num_to_tamil_string(sentence_without_symbols)
        if sentence_without_symbols == False:
            continue  
        
        # Drop too short and too long sentences
        sentence_length = get_sentence_length_without_punctuation(sentence_without_symbols)
        if (sentence_length > MAX_WORDS_LENGTH or sentence_length < MIN_WORDS_LENGTH):
            continue
            
        sentence_without_symbols = clean_up_sentence(sentence_without_symbols)

        sentence_dic = {"work_title": work_title, "sentence": sentence_without_symbols, "sentence_length": sentence_length}
        valid_sentences.append(sentence_dic)
    
    # Drop duplicte sentences
    valid_sentences_df = pd.DataFrame(valid_sentences)
    valid_sentences_df = valid_sentences_df.drop_duplicates(subset='sentence', keep="first")
        
    stats['total_sentences_after_processing'] = valid_sentences_df.shape[0]
    return stats, valid_sentences_df


# In[5]:


#Returns the content of a text file
def get_file_content(text_file_path):
    text = ""
    with open(text_file_path, 'r', encoding = 'utf-8') as file:
        text = file.read()
    return text


# In[6]:


def drop_header_and_footers(sentences):
    header_flag = False
    footer_flag = False
    
    # Tamil Wikisource
    book_content_sentences = []
    for sentence in sentences:
        if "உலகளாவிய பொதுக் கள உரிமம்" in sentence: 
            header_flag = True
        
        if "More details about this collaboration" in sentence:  
            header_flag = False
        
        if "இந்த மின்னூலைப் பற்றி" in sentence:  
            footer_flag = True
        
        if header_flag == False and footer_flag == False:
            book_content_sentences.append(sentence)
    return book_content_sentences


# In[7]:


# Given a sentence, it removes all symbols in the special_symbols list
def remove_special_characters(sentence, special_symbols):
    sentence = sentence.translate({ord(p): " " for p in special_symbols})
    return sentence


# In[8]:


# If a word in any sentence is a digit, it converts it to a tamil string
# If there a digit within a word, it returns False
def convert_num_to_tamil_string(sentence):
    num_within_word = False
    tokens = word_tokenize(sentence)
    for i, word in enumerate(tokens):
        if word.strip().isdigit():
            num_as_string = tamil.numeral.num2tamilstr_american(float(word))
            num_as_string = re.sub("\s\s+", " ", num_as_string)
            tokens[i] = num_as_string
        else:
            any_number = re.compile(r"[+-]?\d+(?:\.\d+)?")
            if any_number.search(word) is not None:
                num_within_word = True
                break
       
    if num_within_word == True:
        return False
    else:
        sentence = ' '.join([str(w) for w in tokens]) 
        return sentence


# In[9]:


# Given a sentence, calculates the word length without punctuation
def get_sentence_length_without_punctuation(sentence):
    sentence_without_punctuation = remove_special_characters(sentence, set(punctuation))
    words_without_punctuation = word_tokenize(sentence_without_punctuation)
    sentence_length = len(words_without_punctuation)
    return sentence_length


# In[10]:


# Remove extra spaces before punctuation
def clean_up_sentence(sentence):
    sentence = sentence.replace(" ,", ",")
    sentence = sentence.replace(" .", ".")
    sentence = sentence.replace(" ?", "?")
    sentence = sentence.strip()
    return sentence


# In[11]:


source_texts = "/home/nat/Desktop/code/tamil/open_tamil_texts/collections/tamil_wikisource/data"
extracted_sentences = "cleaned_sentences"


# In[12]:


source_files = glob.glob(source_texts + "/*.txt")


# In[13]:


run_report = []
for source_file in source_files:
    base_name = os.path.basename(source_file)
    work_title = base_name.replace(".txt", "")
    print("processing " + work_title)
    result = get_commonvoice_sentences(source_file, work_title)
    run_report.append(result[0])
        
    valid_sentences_df = result[1]
    valid_sentences_df.to_csv(extracted_sentences + "/" + work_title + ".csv", index=False)


# In[14]:


run_report_df = pd.DataFrame(run_report)
run_report_df


# In[15]:


# Total number of sentences
total_cv_sentences = run_report_df["total_sentences_after_processing"].sum()
print("Total common voice sentences: " + str(total_cv_sentences))


# In[16]:


# Percentage
percent_converted_sentences = 100 * (run_report_df["total_sentences_after_processing"].sum() / run_report_df["total_sentences_before_processing"].sum())


# In[17]:


print("Total common voice sentences as percentage of the original: " + str(percent_converted_sentences))


# In[18]:


run_report_df.to_csv("tamil_wikisource_run_report.csv", index=False)


# In[ ]:





# In[ ]:




