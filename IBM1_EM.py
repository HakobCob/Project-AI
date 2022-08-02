import numpy as np
from datetime import datetime
import math
import Utils


def expectation_maximization(tagalog_word_dict,english_word_dict,tagalog_sentences,english_sentences):
    total_tagalog_ocurrences = len(tagalog_word_dict)
    total_eng_occurrences = len(english_word_dict)

    # IBM1 Expectaion Maximization algorithm :
    translate_eng_tagalog_matrix = np.full((len(tagalog_word_dict), len(english_word_dict)), 1 / len(english_word_dict),dtype=float)
    translate_eng_tagalog_matrix_prev = np.full((len(tagalog_word_dict), len(english_word_dict)), 1,dtype=float)

    cnt_iter = 0
    while not Utils.is_converged(translate_eng_tagalog_matrix,translate_eng_tagalog_matrix_prev,cnt_iter) :
        cnt_iter += 1
        translate_eng_tagalog_matrix_prev = translate_eng_tagalog_matrix.copy()
        total_eng_tagalog = np.full((len(tagalog_word_dict), len(english_word_dict)), 0, dtype=float)
        total_f = np.full((len(english_word_dict)),0, dtype=float)

        for marker_tur, tagalog_sen in enumerate(tagalog_sentences): #for all sentence pairs (e,f) do
            #compute normalization
            tagalog_sen_words = tagalog_sen.split(" ")
            s_total = np.full((len(tagalog_sen_words)),0,dtype=float)

            for marker_word in range(len(tagalog_sen_words)): #for all words e in e do
                tagalog_word = tagalog_sen_words[marker_word]
                s_total[marker_word] = 0
                eng_sen_words = english_sentences[marker_tur].split(" ")

                for eng_word in eng_sen_words: #for all words f in f do
                    if eng_word == '' :
                        continue 
                    marker_tagalog_in_dict =tagalog_word_dict[tagalog_word]
                    marker_eng_in_dict = english_word_dict[eng_word]
                    s_total[marker_word] += translate_eng_tagalog_matrix[marker_tagalog_in_dict][marker_eng_in_dict]
                #end for
            #end for

            #collect counts
            tagalog_sen_words = tagalog_sen.split(" ")

            for marker_word in range(len(tagalog_sen_words)): #for all words e in e do
                tagalog_word = tagalog_sen_words[marker_word]
                eng_sen_words = english_sentences[marker_tur].split(" ")

                for eng_word in eng_sen_words: #for all words f in f do
                    if eng_word == '' :
                        continue
                    marker_tagalog_in_dict =tagalog_word_dict[tagalog_word]
                    marker_eng_in_dict = english_word_dict[eng_word]
                    total_eng_tagalog[marker_tagalog_in_dict][marker_eng_in_dict] += translate_eng_tagalog_matrix[marker_tagalog_in_dict][marker_eng_in_dict] / s_total[marker_word]
                    total_f[marker_eng_in_dict] += translate_eng_tagalog_matrix[marker_tagalog_in_dict][marker_eng_in_dict] / s_total[marker_word]
                #end for
            #end for
        #end for

        #estimate probabilities
        for eng_marker in  range(total_eng_occurrences): #for all foreign words f do

            for tagalog_marker in range(total_tagalog_ocurrences): #for all English words e do

                if total_eng_tagalog[tagalog_marker][eng_marker] != 0 :
                    translate_eng_tagalog_matrix[tagalog_marker][eng_marker] = total_eng_tagalog[tagalog_marker][eng_marker] / total_f[eng_marker]

            #end for
            
        #end for

    #end while

    print("EM Algorithm Converged in ",(cnt_iter-1)," iterations")
    return translate_eng_tagalog_matrix


def get_translation_prob(e,f,t,e_dict,f_dict):
    const = Utils.const
    l_e = len(e)
    l_f = len(f)
    res = const / math.pow((l_f+1),l_e)
    for j in range(l_e):
        e_word = e[j]
        if e_word in e_dict:
            e_j = e_dict[e_word]
        else:
            print("word '"+ e_word +"' is not found in target language dictionary")
            continue
            #return 0

        sum = 0
        for i in range(l_f):
            f_word = f[i]

            if f_word in f_dict:
                f_i = f_dict[f_word]
                sum += t[e_j][f_i]
            else:
                print("word '" + f_word  +"' is not found in source language dictionary")

        res *= sum

    return res