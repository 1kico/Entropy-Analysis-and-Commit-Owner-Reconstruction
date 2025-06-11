import os
import math
import re
from collections import Counter

def clean_text(text):
  
    #cleans the input text by removing punctuation and numbers
    #keeping only letters (including Albanian characters like ë and ç).
    
    # Only keep letters (including ë and ç), remove everything else
    cleaned = re.sub(r"[^a-zA-Zëç]", "", text.lower())
    return cleaned

def generate_ngrams(text, n):


    if n == 0:
        #treat each character as its own n-gram
        return list(text)
    
    if len(text) < n:
        # Not enough text to form even one n-gram
        return []
    
    ngrams = []
    # create n-grams using the sliding window method
    # slide a window of size n over the text to extract n-grams
    for i in range(len(text) - n + 1):
        ngrams.append(text[i:i+n])
    
    return ngrams

def calculate_entropy(text, n):
  
    # calculates the entropy for n-grams in the text.
    if n == 0:
        # uniform distribution over unique characters
        unique_chars = set(text)
        if not unique_chars:
            return 0.0
        prob = 1.0 / len(unique_chars)
        return -len(unique_chars) * prob * math.log2(prob)
    
    elif n == 1:
        # entropy for single characters
        if not text:
            return 0.0
        total = len(text)
        char_counts = Counter(text)
        entropy = 0.0
        for count in char_counts.values():
            prob = count / total
            entropy -= prob * math.log2(prob)
        return entropy
    
    else:
        if len(text) < n:
            return 0.0
        
        context_counts = Counter() # count occurrences of each context (n-1 gram)
        next_char_given_context = {} # dictionary to hold next character counts given each context
        
        for i in range(len(text) - n + 1): # iterate through the text to extract n-grams
            context = text[i:i + n - 1] 
            next_char = text[i + n - 1] 
            
            context_counts[context] += 1 
            
            if context not in next_char_given_context: # initialize the context if not already present
                next_char_given_context[context] = Counter() # iount occurrences of next characters given the context
            next_char_given_context[context][next_char] += 1 #
        
        # calculate the weighted average of the entropy for each context
        total_contexts = sum(context_counts.values())
        conditional_entropy = 0.0
        
        for context, context_count in context_counts.items(): 
            context_prob = context_count / total_contexts
            
            # entropy for this specific context
            context_entropy = 0.0
            total_next_chars = sum(next_char_given_context[context].values()) 
            
            for next_char_count in next_char_given_context[context].values(): 
                next_char_prob = next_char_count / total_next_chars 
                context_entropy -= next_char_prob * math.log2(next_char_prob) 
            
            conditional_entropy += context_prob * context_entropy
        
        return conditional_entropy

def analyze_text_file(file_path):

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_text = file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return

    
    cleaned_text = clean_text(raw_text)
    
    print(f"\nAnalyzing: {file_path}")
    print(f"Original text length: {len(raw_text)} characters")
    print(f"Cleaned text length: {len(cleaned_text)} characters")
    print()
    
    # analyze n-grams from size 0 to 10
    for n in range(11):
        entropy = calculate_entropy(cleaned_text, n)
        ngrams = generate_ngrams(cleaned_text, n)
        

        
        freq_dist = Counter(ngrams) 
        total = len(ngrams) 
        unique_count = len(freq_dist)
        
        print(f"\n[{n}-gram Analysis]")
        print(f"Entropy: {entropy:.6f} bits")
        print(f"Total n-grams: {total}")
        print(f"Unique n-grams: {unique_count}")
        
        # show the 5 most frequent n-grams
        print("Most frequent:")
        most_common = freq_dist.most_common(5) # get the 5 most common n-grams
        for i, (token, count) in enumerate(most_common, 1):
            display_token = f"'{token}'" if n > 0 else token 
            print(f"  {i}. {display_token}: {count}")
        
        # show the 5 least frequent n-grams
        print("Least frequent:")
        all_items = freq_dist.most_common()
        least_common = all_items[-5:] if len(all_items) >= 5 else all_items
        
        for i, (token, count) in enumerate(reversed(least_common), 1):
            display_token = f"'{token}'" if n > 0 else token
            print(f"  {i}. {display_token}: {count}")

def main():
 
    # path to the folder containing your text files
    data_directory = "C:\\Users\\sheha\\OneDrive\\Desktop\\Algorithms Assignment II\\Part1\\data"
    
    # check if the data directory exists
    if not os.path.exists(data_directory):
        print(f"Directory '{data_directory}' not found.")
        return
    
    # find all .txt files in the directory
    text_files = []
    try:
        for filename in os.listdir(data_directory): 
            if filename.lower().endswith(".txt"): # check if the file is a text file
                text_files.append(os.path.join(data_directory, filename)) # construct full path for each text file
    except Exception as e:
        print(f"Error accessing directory '{data_directory}': {e}")
        return
    
    if not text_files:
        print(f"No .txt files found in '{data_directory}' directory.")
        return
    
    print(f"Found {len(text_files)} text file(s) to analyze:")
    for file_path in text_files:
        print(f"  - {os.path.basename(file_path)}") 
    
    # analyze each text file
    for file_path in text_files:
        analyze_text_file(file_path)
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()