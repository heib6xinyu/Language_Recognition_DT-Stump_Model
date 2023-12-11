# -*- coding: utf-8 -*-

import argparse
import string
vowels = "aeiouAEIOU\u00E0\u00E8\u00E9\u00EC\u00ED\u00F2\u00F3\u00F9\u00FA\u00C0\u00C8\u00C9\u00CC\u00CD\u00D2\u00D3\u00D9\u00DA"

def calculate_vowel_consonant_ratio(text):
    vowel_count = 0
    consonant_count = 0

    for char in text:
        if char.isalpha():
            if char in vowels:
                vowel_count += 1
            else:
                consonant_count += 1

    if consonant_count == 0:
        if vowel_count == 0:
            return None  # Handle cases where there are no vowels or consonants.
        return float('inf')  # Handle cases where there are no consonants.

    ratio = vowel_count / consonant_count
    return ratio

def count_words_ending_with_vowels_normalized(text):
    words = text.split()
    word_count = len(words)
    vowel_ending_count = sum(1 for word in words if word[-1] in vowels)
    return vowel_ending_count / word_count if word_count > 0 else 0

def max_and_average_word_length(text):
    words = text.split()
    if not words:  # Check if the text is empty or has no words
        return 0, 0

    word_lengths = [len(word) for word in words]
    max_word_length = max(word_lengths)
    average_word_length = sum(word_lengths) / len(words)

    return max_word_length, average_word_length

def max_and_average_consonant_chain_lengths(text):
    consonants = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
    max_chain_length = 0
    total_chain_length = 0
    current_chain_length = 0
    chain_count = 0
    total_chars = len(text)

    for char in text:
        if char in consonants:
            current_chain_length += 1
            total_chain_length += 1
            max_chain_length = max(max_chain_length, current_chain_length)
        else:
            if current_chain_length > 0:
                chain_count += 1
            current_chain_length = 0

    average_chain_length = total_chain_length / total_chars if total_chars > 0 else 0
    normalized_max_chain_length = max_chain_length / total_chars if total_chars > 0 else 0

    return normalized_max_chain_length, average_chain_length

def extract(data_file):
    input_file = data_file
    output_file = "input_feature.txt"
    remove_punct_trans = str.maketrans('', '', string.punctuation)

    try:
        with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
            for line in infile:
                line = line.translate(remove_punct_trans)
                line = line.strip()

                # Call your feature extraction functions here
                vcratio = calculate_vowel_consonant_ratio(line)
                wvc = count_words_ending_with_vowels_normalized(line)
                mwl, awl = max_and_average_word_length(line)
                mccl, accl = max_and_average_consonant_chain_lengths(line)

                outfile.write(f"{vcratio}, {wvc}, {mwl}, {awl}, {mccl}, {accl}\n")
    except FileNotFoundError:
        print(f"The corresponding language input file {input_file} does not exist.")
        return

extract("langtest.txt")