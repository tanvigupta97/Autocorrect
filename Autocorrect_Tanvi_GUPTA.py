#Author : Gupta Tanvi
#Tutorial Group : FE2

#To write a program that performs autocorrect operation
#Take an input word
#Go through corpus/database to check if it exists
#If it doesnt, offer top 10 alternative spelling suggestions

#Additional optional features
#1. Augment words from 'big.txt' with words from 'word_list.txt'
#2. Allow addition of unknown words
#3. Find the most likely word by checking word frequency and using probabilistic methods

import time
import string
tot_words = 0
word_set = set ( )
list_of_all_words = []


#Open file
#Filter words and add to a set and a list
def file_read(filename) :
    """Reads the file and stores words individually in a set and a list"""
    with open(filename,'r') as theFile:        #Opens file in read mode
        for line in theFile:
            words_line = line.split()           #list of words in each line
            for word in words_line:             #iterates through words of each line
                l = len ( word )
                if ( not (word[0].isalpha()) or not ( word[l - 1].isalpha() ) ):     #eliminates punctuators at beginning or end of word
                    word.strip(string.punctuation)
                if ( word.isalpha() ):              #checks if word is alphabetic
                    global word_set
                    global list_of_words
                    word = word.lower()
                    word_set.add( word )            #adds lowercase word to set of words to eliminate repetition
                    list_of_all_words.append(word)      #adds lowercase word to list of words to check frequency
        
#Returns integral value for difference between two words
#Compare words for different types of modifications
#The idea to compare strings for swapping, substitutions, insertions
#and deletions is derived from Levenshtein distance
def worddistance(word1,word2):
    """Returns the editing distance between two strings"""
    word_dist = 0
    l1 = len(word1)
    l2 = len(word2)
    if word1==word2:
        word_dist=0
    elif l1==l2:
        sub=swap=0        
        for i in range (0,l1):                  #swapping
            if word1==(word2[:i-1]+word2[i]+word2[i-1]+word2[i+1:]) or word2==(word1[:i-1]+word1[i]+word1[i-1]+word1[i+1:]):
                swap+=1
        word_dist += swap
        if swap == 0:
            for i in range (0,l1):              #substitution
                if not ( word1[i] == word2[i] ):
                    sub +=1
            word_dist+=sub
    else:
        dist_front = dist_back = abs(l2-l1)
        insdel = 0        
        for i in range (1,min(l1,l2)):           #insertion/deletion
            if word1==(word2[:i]+word2[i+1:]) or word2==(word1[:i]+word1[i+1:]):
                insdel+=1
        if insdel >=2:                        #to eliminate false increase in 'insdel' due to double letters
            for i in range (0,l1-1):             #for example, insdel = 2, for sugest and suggest, according to the previous loop
                if word1[i]==word1[i+1]:
                    insdel-=1
            for i in range (0,l2-1):
                if word2[i]==word2[i+1]:
                    insdel-=1    
        for i in range (0,min(l1,l2)):           #substitution at end of word
            if not(word1[i]==word2[i]):
                dist_front +=1                   
        for i in range (1,min(l1,l2)+1):         #substitution in beginning of word
            if not(word1[l1-i]==word2[l2-i]):
                dist_back +=1
        if insdel == 0:
            word_dist += min(dist_front,dist_back)
        else:
            word_dist += min(dist_front,dist_back,insdel)
    return(word_dist)

#Checks correctness of word
#Prints top suggestions for incorrect words
global fin2
def autocorrect ( input_word ):
    """Displays closest word suggestions according to word distance"""
    input_word = input_word.lower()
    sugg_words = []
    top_sugg = []
    if input_word in word_set:                  #for correct words
        print ( 'The entered word is correct' )
        global fin2
        fin2 = time.time()
    else :        
        for word in word_set:
            dist = worddistance(input_word,word)
            if dist <=5:                        #filter words with lowest word distance
                fin_word = str(dist)+ word
                sugg_words.append(fin_word)    
        if len(sugg_words)==0:                  #no close suggestions
            print("Sorry! No suggestions found.")
        else:
            sugg_words.sort()                   #for words with lowest word distance           
            for i in range(10):                 #limit top suggestions to 10
                if i >= len(sugg_words):
                    break
                else:
                    top_sugg.append(sugg_words[i])
            
            print ('\nDid you mean:')             #print top word suggestions
            ct = 0
            for elem in top_sugg:
                ct+=1
                if ct == len(top_sugg):
                    print('or ', elem[1:], '?')
                else:
                    print( elem[1:], ', ', end='')
            ch = input("\nDo you want to know the most likely word? It might take a while. (Y or N)\n")
            if ch=='y' or ch=='Y':
                most_likely = find_freq(top_sugg)   #to find most likely word
                print("\nThe most likely word is: ", most_likely[1:])
        fin2 = time.time()
        add_word(input_word)                    #to add to corpus
    
#Offers option to add word to dictionary
def add_word(new_word):
    """Offers the option to add the input word to dictionary"""
    choice = input("\nDo you want to add this word to your dictionary? (Y or N)\n")
    if choice == 'Y' or choice == 'y':
        word_set.add( new_word )
        list_of_all_words.append( new_word )
        print('The word has been added to your dictionary')

#Returns word with highest likeliness in corpus of words
#It first counts the number of occurrences of each word and divides it 
#by the total number of words, giving probability of occurring
#Then the complement is found by subtracting from 1
#this gives probability of not occurring
#Word with the lowest average of word distance and
#probability of not occurring is chosen as most likely word
#because high prob of occurring => low prob of not occurring
def find_freq(final_words):
    """Returns the word with highest number of occurrences in a list from a given input list"""
    file1 = open('big.txt','r')
    file2 = open('word_list.txt','r')
    freq_dict={}
    total_no_list = len(list_of_all_words)
    for word1 in final_words:
        cnt = 0
        for word2 in list_of_all_words:                     #counts no of occurrences
            if word1[1:]==word2:
                cnt+=1
        prob_not_occur = 1-(cnt/total_no_list)              #calculates probability of not occurring in the list of words
        tot_likely = 0.5 * (prob_not_occur + int(word1[0])) #calculates likelihood by assigning equal weightage to word distance and occurrences  
        freq_dict[word1]=tot_likely                         #stores in dictionary
    min_val=100                                             #arbitrary high value
    likely=''
    for key ,value in  freq_dict.items():
        if value<min_val:                                   #choses word with combination of lowest word distance and highest occurrences
            likely = key
            min_val = value
    file1.close()
    file2.close()
    return(likely)                                          #returns word with highest occurrences

choice1 = input("Do you want to prepare the database including 'word_list.txt'? (Y or N)\n")
ini1 = time.time()
file_read('big.txt')
if choice1 == 'Y' or choice1 == 'y':
    file_read('word_list.txt')
    fin1 = time.time()
else:
    fin1 = time.time()
tot_words = len ( word_set )
print('Wait till database is being prepared..')
print ('Database consists of ',tot_words, ' words')
print ("Database setup time = ", fin1-ini1)                 #Displays time taken to read file(s)
inp_word = input('Enter word ')
ini2 = time.time()  
autocorrect (inp_word)
print ("Response time = ", fin2-ini2)                       #Displays time taken for response by computer, including user response
                                                            
