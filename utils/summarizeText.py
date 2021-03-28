'''
    contentCurator.py

    Uses tf-idf weighting to summarize content
    tf-idf evaluates how relevant a word is to a document
    
    tf - Term Frequency (Measures the frequency of a word in a document)
    idf - Inverse Document Frequency (Dimishes the weight and measures the informativeness of terms)
'''

import math
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords

def frequencyTable(text):
    stop_words = stopwords.words('english')
    tokenized_words = word_tokenize(text)
    ps = PorterStemmer()

    frequency_table = {}
    for word in tokenized_words:
        word = ps.stem(word)
        if word in stop_words:
            continue
        if word in frequency_table:
            frequency_table[word] += 1
        else:
            frequency_table[word] = 1
    
    return frequency_table

def frequencyMatrix(sentences):
    frequency_matrix = {}
    stop_words = stopwords.words('english')
    ps = PorterStemmer()

    for sentence in sentences:
        frequency_table = {}
        tokenized_words = word_tokenize(sentence)

        for word in tokenized_words:
            word = word.lower()
            word = ps.stem(word)
            if word in stop_words:
                continue
            if word in frequency_table:
                frequency_table[word] += 1
            else:
                frequency_table[word] = 1
        
        frequency_matrix[sentence[:15]] = frequency_table
    
    return frequency_matrix

def tfMatrix(frequency_matrix):
    tf_matrix = {}

    for sentence, frequency_table in frequency_matrix.items():
        tf_table = {}
        sentence_length = len(frequency_table)

        for word, count in frequency_table.items():
            tf_table[word] = count / sentence_length
        
        tf_matrix[sentence] = tf_table
    
    return tf_matrix

def documentsPerWords(frequency_matrix):
    word_doc_table = {}

    for sentence, frequency_table in frequency_matrix.items():
        for word, count in frequency_table.items():
            if word in word_doc_table:
                word_doc_table[word] += 1
            else:
                word_doc_table[word] = 1
    
    return word_doc_table

def idfMatrix(frequency_matrix, count_doc_per_words, total_documents):
    idf_matrix = {}

    for sentence, frequency_table in frequency_matrix.items():
        idf_table = {}

        for word in frequency_table.keys():
            idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))
        
        idf_matrix[sentence] = idf_table
    
    return idf_matrix

def tfidfMatrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sentence1, f_table1), (sentence2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):
        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(), f_table2.items()):  
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[sentence1] = tf_idf_table

    return tf_idf_matrix

def scoreSentences(tf_idf_matrix):
    sentence_value = {}

    for sentence, frequency_table in tf_idf_matrix.items():
        total_score_per_sentence = 0

        count_words_in_sentence = len(frequency_table)
        for word, score in frequency_table.items():
            total_score_per_sentence += score

        sentence_value[sentence] = total_score_per_sentence / count_words_in_sentence

    return sentence_value

def averageScore(sentence_value):
    sum_val = 0
    for entry in sentence_value:
        sum_val += sentence_value[entry]

    # Average value of a sentence from original summary_text
    average = (sum_val / len(sentence_value))

    return average

def generate(sentences, sentence_value, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:15] in sentence_value and sentence_value[sentence[:15]] >= (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary

def summarize(text):
    sentences = sent_tokenize(text)
    total_documents = len(sentences)

    frequency_matrix = frequencyMatrix(sentences)
    tf_matrix = tfMatrix(frequency_matrix)
    count_doc_per_words = documentsPerWords(frequency_matrix)
    idf_matrix = idfMatrix(frequency_matrix, count_doc_per_words, total_documents)
    tf_idf_matrix = tfidfMatrix(tf_matrix, idf_matrix)
    sentence_scores = scoreSentences(tf_idf_matrix)
    threshold = averageScore(sentence_scores)
    summary = generate(sentences, sentence_scores, 1.0 * threshold)

    return summary