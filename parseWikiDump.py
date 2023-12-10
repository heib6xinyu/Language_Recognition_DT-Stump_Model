import xml.etree.ElementTree as ET
import json
import argparse

def parse_abstracts(xml_file):
    abstracts = []

    tree = ET.parse(xml_file)
    root = tree.getroot()

    for doc in root.iter('doc'):
        title = doc.find('title').text.strip()
        url = doc.find('url').text.strip()
        abstract_element = doc.find('abstract')
        if abstract_element is not None and abstract_element.text is not None:
            abstract = abstract_element.text.strip()
        else:
            abstract = ""
        abstract_data = {
            'title': title,
            'url': url,
            'abstract': abstract
        }

        abstracts.append(abstract_data)

    return abstracts

def save_abstracts_to_json(abstracts, json_file):
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(abstracts, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse XML file and save abstracts to JSON')
    parser.add_argument('xml_file', type=str, help='Input XML file name')
    parser.add_argument('json_file', type=str, help='Output JSON file name')
    args = parser.parse_args()

    abstracts = parse_abstracts(args.xml_file)
    save_abstracts_to_json(abstracts, args.json_file)
