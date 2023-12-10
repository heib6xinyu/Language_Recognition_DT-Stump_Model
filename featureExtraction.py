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

def count_words_ending_with_vowels(text):
    words = text.split()
    # Check the last character of each word; if it's punctuation, consider the second last character
    count = sum(1 for word in words if word[-1].lower() in vowels )
    return count

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

    for char in text:
        if char in consonants:
            current_chain_length += 1
            total_chain_length += 1
            max_chain_length = max(max_chain_length, current_chain_length)
        else:
            if current_chain_length > 0:
                chain_count += 1
            current_chain_length = 0

    # Calculate average chain length; avoid division by zero
    average_chain_length = total_chain_length / chain_count if chain_count > 0 else 0

    return max_chain_length, average_chain_length

def capitalization_pattern(text):
    words = text.split()
    total_words = len(words)
    capitalized_words = sum(1 for word in words if word.istitle())

    if total_words > 0:
        percentage_capitalized = (capitalized_words / total_words)
    else:
        percentage_capitalized = 0

    return percentage_capitalized


def main():
    parser = argparse.ArgumentParser(description="Calculate various text features for each line of text")
    parser.add_argument("language_codes", help="Comma-separated list of language codes (e.g., 'en,it,nl')")
    args = parser.parse_args()

    languages = args.language_codes.split(',')
    segment_lengths = [10, 20, 50]

    remove_punct_trans = str.maketrans('', '', string.punctuation)

    for language in languages:
        for length in segment_lengths:
            input_file = f"{language}_{length}.txt"
            output_file = f"{language}_{length}_feature.txt"

            try:
                with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
                    for line in infile:
                        line = line.translate(remove_punct_trans)
                        line = line.strip()

                        # Call your feature extraction functions here
                        vcratio = calculate_vowel_consonant_ratio(line)
                        wvc = count_words_ending_with_vowels(line)
                        mwl, awl = max_and_average_word_length(line)
                        mccl, accl = max_and_average_consonant_chain_lengths(line)
                        cp = capitalization_pattern(line)
                        if mwl <= 40 and vcratio != None:
                            outfile.write(f"{language}: {vcratio}, {wvc}, {mwl}, {awl}, {mccl}, {accl}, {cp}\n")
            except FileNotFoundError:
                print(f"The corresponding language input file {input_file} does not exist.")
                return

if __name__ == "__main__":
    main()