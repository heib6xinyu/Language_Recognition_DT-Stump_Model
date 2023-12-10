import argparse

def calculate_vowel_consonant_ratio(text):
    vowels = "AEIOUaeiou"
    vowel_count = 0
    consonant_count = 0

    for char in text:
        if char.isalpha():
            if char in vowels:
                vowel_count += 1
            else:
                consonant_count += 1

    if consonant_count == 0:
        return float('inf')  # Handle cases where there are no consonants.

    ratio = vowel_count / consonant_count
    return ratio

def main():
    parser = argparse.ArgumentParser(description="Calculate vowel-to-consonant ratio for each line of text")
    parser.add_argument("input_file", help="Input text file with one text segment per line")
    parser.add_argument("output_file", help="Output text file to save the calculated ratios")
    args = parser.parse_args()

    with open(args.input_file, "r", encoding="utf-8") as infile, open(args.output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            line = line.strip()
            ratio = calculate_vowel_consonant_ratio(line)
            outfile.write(f"{line}: {ratio}\n")

if __name__ == "__main__":
    main()