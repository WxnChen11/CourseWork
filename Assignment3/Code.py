'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 18, 2015.
'''

import math
import time
import os
os.chdir("C:/Users/Wenxin/Documents/School/University/2015Fall/CSC180/Assignment3")


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    
    sum = 0.0
    
    if len(vec1) > len(vec2):
        for key in vec2:
            if key in vec1:
                sum += vec1[key] * vec2[key]
    else:
        for key in vec1:    
            if key in vec2:
                sum += vec1[key] * vec2[key]
    
    return sum/(norm(vec1)*norm(vec2))

def build_semantic_descriptors(sentences):
    
    d = {}
    words_ignore = []
    
    for i in range(len(sentences)):
        for z in range(len(sentences[i])):
            word = sentences[i][z]
            if word not in words_ignore:
                if word not in d:
                    d[word] = {}
                for j in range(len(sentences[i])):
                    compliment_word = sentences[i][j]
                    if compliment_word != word:
                        if compliment_word not in d[word]:
                            d[word][compliment_word] = 1
                        else:
                            d[word][compliment_word] += 1
                            
            words_ignore += [word]
        words_ignore = []
        
        
    return d

def build_semantic_descriptors_from_files(filenames):
    
    text = ""
    res = []
    
    for i in range(len(filenames)):
        f = open(filenames[i], "r", encoding="utf-8-sig")
        str = f.read()
        
        L = [',', '-', ':', ';', '"', "'"]
        
        for i in range(len(L)):
            str = str.replace(L[i], " ")
            
        str = str.replace("?" , ".")
        str = str.replace("!" , ".")
            
        text += str + " "
    
    text = text.lower()
    sentences = text.split(".")
    #print(sentences)
    
    i = 0
    t = 0
    #str[i] = str[i].split() may speed this up
    while i< len(sentences):
        # words = sentences[i].split()
        # if words:
        #     #print(words)
        #     res += [[]]
        #     #print(res)
        #     for z in range(len(words)):
        #         #print(z)
        #         #print(words)
        #         res[t].append(words[z])
        #     t += 1
        # i += 1
        
        sentences[i] = sentences[i].split()
        if sentences[i]:
            #print(words)
            res += [[]]
            #print(res)
            for z in range(len(sentences[i])):
                #print(z)
                #print(words)
                res[t].append(sentences[i][z])
            t += 1
        i += 1
            
    return build_semantic_descriptors(res)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    
    highest_score = -100    
    cur_word = ""
    
    if word not in semantic_descriptors:
        return choices[0]
    
    for i in range(len(choices)):
        if choices[i] in semantic_descriptors:
            score = similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[i]])
            if score > highest_score:
                highest_score = score
                cur_word = choices[i]
        
        else:
            if highest_score < -1:
                highest_score = -1
                cur_word = choices[i]
    
    
    return cur_word


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    
    f = open(filename, "r", encoding="utf-8")
    str = f.read()
    #print(str)
    str = str.split("\n")
    #print(str)
    list = []
    for i in range(len(str)):
        str[i] = str[i].split()
    
    correct = 0.0
    total = 0.0
    for i in range(len(str)):
        if most_similar_word(str[i][0], str[i][2:], semantic_descriptors, similarity_fn) == str[i][1]:
            correct += 1
        
        total += 1
    
    return correct*100/total
            
    
#####

man = {"i": 3, "am": 3, "a": 2, "sick": 1, "spiteful": 1, "an": 1, "unattractive": 1}
liver = {"i": 1, "believe": 1, "my": 1, "is": 1, "diseased": 1}

print(cosine_similarity(man, liver)*(math.sqrt(130)))

print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))

# print(build_semantic_descriptors([["i", "am", "a", "sick", "man"],
# ["i", "am", "a", "spiteful", "man"],
# ["i", "am", "an", "unattractive", "man"],
# ["i", "believe", "my", "liver", "is", "diseased"],
# ["however", "i", "know", "nothing", "at", "all", "about", "my",
# "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]))

t = time.time()
print(run_similarity_test("test2.txt", build_semantic_descriptors_from_files(["warandpeace.txt"]), cosine_similarity))
print(time.time() - t)





