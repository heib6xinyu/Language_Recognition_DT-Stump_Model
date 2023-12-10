import json
import random
import argparse

def extract_segments(input_json, output_10, output_20, output_50):
    # Read the JSON file containing abstracts
    with open(input_json, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        abstracts = [item['abstract'] for item in data]

    # Shuffle the list of abstracts
    random.shuffle(abstracts)

    # Initialize counters for each segment length
    segments_10 = []
    segments_20 = []
    segments_50 = []

    # Extract segments based on word count criteria
    for abstract in abstracts:
        words = abstract.split()
        if len(words) >= 50:
            segment = ' '.join(words[:50])
            segments_50.append(segment)
        elif len(words) >= 20:
            segment = ' '.join(words[:20])
            segments_20.append(segment)
        elif len(words) >= 10:
            segment = ' '.join(words[:10])
            segments_10.append(segment)

        # Check if we have reached 5000 segments for each length
        if len(segments_10) == 5000 and len(segments_20) == 5000 and len(segments_50) == 5000:
            break

    # Save segments to separate text files
    with open(output_10, 'w', encoding='utf-8') as file:
        file.write('\n'.join(segments_10))

    with open(output_20, 'w', encoding='utf-8') as file:
        file.write('\n'.join(segments_20))

    with open(output_50, 'w', encoding='utf-8') as file:
        file.write('\n'.join(segments_50))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text segments from JSON file.")
    parser.add_argument("input_json", help="Input JSON file containing abstracts")
    parser.add_argument("output_10", help="Output file for 10-word segments")
    parser.add_argument("output_20", help="Output file for 20-word segments")
    parser.add_argument("output_50", help="Output file for 50-word segments")
    args = parser.parse_args()

    extract_segments(args.input_json, args.output_10, args.output_20, args.output_50)
