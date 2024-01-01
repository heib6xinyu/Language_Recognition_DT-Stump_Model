# Multi-Language Detection Using Decision Tree and AdaBoost Stumps

## Overview
This project aims to develop models capable of identifying the language of a given text segment. Focusing on English, Dutch, and Italian languages, I've implemented a Decision Tree and an AdaBoost with Stumps model. The project includes custom functions for data collecting and handling, feature extraction, and model training and evaluation.

## How to Run
Make sure you have Python installed on your system. Clone the repository and navigate to the project directory.

### To Train the Models:
```bash
python wiki.py train <sample_data_amount>
```

### To Predict Using the Models:
```bash
python wiki.py predict <model_type> <datafile>
```
- `model_type` can be 'tree', 'stumps', or 'best'.
- `datafile` is the name of the file containing test cases.
  
## Data Gathering and Processing
Data was sourced from Wikipedia abstract dumps, offering a substantial and diverse dataset. I extracted segments of 10, 20, and 50 words, optimizing data quantity for computational efficiency.

### Data Collection Highlights:
- Initial use of the Wikipedia API, later shifted to wiki abstract dumps for larger data volumes.
- Optimal data count settled at around 3,000 segments for manageable computation and effective training.
- Data cleaning integrated with feature extraction, discarding non-representative segments.
  
### Detailed Explaination

The data gathering process for the language detection project underwent several stages, evolving in response to practical considerations and the goal of optimizing the balance between data quantity, quality, and computational efficiency:

1. **Initial Approach - Wiki API**: The project initially utilized the Wikipedia API to fetch random articles and extract text segments of 10, 20, and 50 words. However, this approach was soon found to be too slow and inefficient due to the API's rate limits. I eventually reused this script to get validation data. I want to get more than enough data so I don't need to worry about imbalance class, overfitting. (Although sometime too much data will also caused overfitting.)

2. **Switch to Wiki Abstract Dumps**: To overcome the limitations of live API calls, the project shifted to using Wikipedia abstract dumps. These dumps provided a more extensive and diverse dataset, comprising summaries of articles, thus serving as a representative sample of language usage. The size of these dumps varied significantly, ranging from 400MB to 1.5GB. I used ElementTree (xml.etree.ElementTree): A built-in Python library for parsing and creating XML data.

3. **Data Quantity and Computational Considerations**: At one point, over 45,000 data segments were extracted. However, it became evident that handling such a large dataset was not only time-consuming but also did not yield proportionately better results in model accuracy. Consequently, the data count was optimized to around 3,000 segments. This number represented a "sweet spot," offering a balance between sufficient data for model training and a manageable computational load for hyperparameter tuning.

4. **Data Collection and Cleaning Integration**: To enhance efficiency, the data collection (reading from dumps) and feature extraction were combined. This integration allowed for immediate identification and exclusion of outliers or non-representative data during the feature extraction phase. For instance:
   - **Vowel-Consonant Ratio**: Segments without vowels or consonants were discarded, as they do not represent typical language structures.
   - **Maximum Word Length**: Segments with words exceeding 30 characters were eliminated, as these often turned out to be URLs or non-standard text rather than regular language usage.

Some other data cleaning code involved removing punctuation and ensuring each text segment conformed to the expected word count. Feature extraction was performed on cleaned segments. Lines that did not conform to the expected format (e.g., missing language labels) were skipped to maintain data integrity.


## Features
The following features were computed from the input:
- **Vowel-Consonant Ratio**: Ratio of vowels to consonants in a segment.
- **Words Ending with Vowels**: Proportion of words ending in vowels.
- **Word Length Metrics**: Maximum and average word lengths.
- **Consonant Chain Lengths**: Maximum and average lengths of consecutive consonants.

### Detail Explaination

For the language detection project, I chose a set of linguistic features that capture unique aspects of languages and can be computed directly from text input. These features include:

1. **Vowel-Consonant Ratio**: This feature measures the ratio of vowels to consonants in a text segment. Different languages have characteristic vowel-to-consonant ratios, making this a useful discriminative feature. The ratio is calculated by counting vowels (including accented vowels specific to Italian and Dutch) and consonants in the text and then dividing the vowel count by the consonant count. The vowel-to-consonant ratio (vcratio) is already a normalized measure in a certain sense. It's a ratio of counts of two types of characters, making it inherently comparative. This ratio provides a measure of the balance between vowels and consonants in a text.

2. **Words Ending with Vowels**: This counts the proportion of words ending in vowels. The proportion is normalized by the total number of words in the text segment, offering insight into language structure, as some languages are more likely to have words ending in vowels. I also normalized the words count against the text segment length. Because this count could be influenced by the length of the text. Normalizing it by the total number of words in the text can provide a proportion, which is more comparable across texts of different lengths.

3. **Maximum and Average Word Length**: These features provide information about the typical word lengths in a language, which can vary significantly between languages. They are computed by measuring the lengths of all words in the text and then calculating the maximum and the average of these lengths.

4. **Maximum and Average Consonant Chain Lengths**: This measures the longest sequence of consecutive consonants and the average length of such sequences in the text. This feature captures phonetic structures unique to each language. I also normalized the words count against the text segment length. Because similar to the count of words ending with vowels, these features could be influenced by the length of the text. 


These features were chosen for their ability to capture fundamental linguistic characteristics without needing complex parsing or understanding of the text content, making them computationally efficient and broadly effective across different languages.

## Model Training and Hyperparameter Tuning
We implemented custom train-test split functions tailored to the models' characteristics and conducted extensive hyperparameter tuning.

#### Sampling and Model Selection
- The project employed a dynamic approach to determining the ideal size of training and testing datasets. This was achieved through a loop that sampled varying amounts of data within a predefined range.
- At each iteration, the sampled data underwent training with different hyperparameters. The best parameters and models were tracked, focusing on validation set accuracy as the primary metric for model effectiveness.
- Decision Tree performance was found to be suboptimal compared to AdaBoost Stumps, prompting a greater focus on the latter.


### Decision Tree
- Hyperparameters: Maximum depth (capped at the number of features) and minimum samples split (1%, 2%, 5% of data).
- Found to be less effective than AdaBoost Stumps.
- Test accuracies - decision tree:
Dutch: 10/15
Italian: 15/15
English: 0/15


### AdaBoost with Stumps
- Hyperparameters: Number of learners (stumps).
- Showed promising results compared to the Decision Tree.
- Test accuracies - adaboost:
Dutch: 7/15
Italian: 15/15
English: 13/15

### General Training Process
- Dynamic data sampling for training and testing.
- Best models selected based on validation set accuracy.



## Future Work
- Improve the efficiency of the data collection process.
- Investigate library-based language feature extraction methods to address the bias towards the English language observed in the Decision Tree model.
Further refine data collection and processing.
- Explore advanced methods for model serialization beyond Python’s pickle library.



