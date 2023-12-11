# -*- coding: utf-8 -*-

import json
import random
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


def extract_and_process_segments(input_json, output_file, language, segment_lengths, max_data_points):
    # Read the JSON file containing abstracts
    with open(input_json, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        abstracts = [item['abstract'] for item in data]

    random.shuffle(abstracts)
    remove_punct_trans = str.maketrans('', '', string.punctuation)

    data_counters = {length: 0 for length in segment_lengths}

                
    with open(output_file, "w", encoding="utf-8") as outfile:
        for abstract in abstracts:
            words = abstract.split()
            for length in segment_lengths:
                if len(words) >= length and data_counters[length] < max_data_points:
                    segment = ' '.join(words[:length])
                    processed_segment = segment.translate(remove_punct_trans).strip()

                    # Perform feature extraction
                    vcratio = calculate_vowel_consonant_ratio(processed_segment)
                    if vcratio is None:
                        continue  
                    mwl, awl = max_and_average_word_length(processed_segment)
                    if mwl > 30:
                        continue
                    wvc = count_words_ending_with_vowels_normalized(processed_segment)
                    mwl, awl = max_and_average_word_length(processed_segment)
                    mccl, accl = max_and_average_consonant_chain_lengths(processed_segment)

                    # Write features to output file
                    outfile.write(f"{language}: {vcratio}, {wvc}, {mwl}, {awl}, {mccl}, {accl}\n")
                    data_counters[length] += 1

                # Check if we have collected enough data for each length
                if all(count >= max_data_points for count in data_counters.values()):
                    return  # Stop processing further data
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text segments and perform feature extraction.")
    parser.add_argument("input_json", help="Input JSON file containing abstracts")
    parser.add_argument("output_file", help="Output file for extracted features")
    parser.add_argument("language", help="Language code (e.g., 'en')")
    parser.add_argument("max_data_points", type=int, help="Maximum number of data points to collect")

    args = parser.parse_args()

    extract_and_process_segments(args.input_json, args.output_file, args.language, [50, 20, 10], args.max_data_points)
