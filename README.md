# Language_Recognition_DT-Stump_Model

### Feature Selection

For the language detection project, I chose a set of linguistic features that capture unique aspects of languages and can be computed directly from text input. These features include:

1. **Vowel-Consonant Ratio**: This feature measures the ratio of vowels to consonants in a text segment. Different languages have characteristic vowel-to-consonant ratios, making this a useful discriminative feature. The ratio is calculated by counting vowels (including accented vowels specific to Italian and Dutch) and consonants in the text and then dividing the vowel count by the consonant count. The vowel-to-consonant ratio (vcratio) is already a normalized measure in a certain sense. It's a ratio of counts of two types of characters, making it inherently comparative. This ratio provides a measure of the balance between vowels and consonants in a text.

2. **Words Ending with Vowels**: This counts the proportion of words ending in vowels. The proportion is normalized by the total number of words in the text segment, offering insight into language structure, as some languages are more likely to have words ending in vowels. I also normalized the words count against the text segment length. Because this count could be influenced by the length of the text. Normalizing it by the total number of words in the text can provide a proportion, which is more comparable across texts of different lengths.

3. **Maximum and Average Word Length**: These features provide information about the typical word lengths in a language, which can vary significantly between languages. They are computed by measuring the lengths of all words in the text and then calculating the maximum and the average of these lengths.

4. **Maximum and Average Consonant Chain Lengths**: This measures the longest sequence of consecutive consonants and the average length of such sequences in the text. This feature captures phonetic structures unique to each language. I also normalized the words count against the text segment length. Because similar to the count of words ending with vowels, these features could be influenced by the length of the text. 


These features were chosen for their ability to capture fundamental linguistic characteristics without needing complex parsing or understanding of the text content, making them computationally efficient and broadly effective across different languages.

### Data Gathering Process

The data gathering process for the language detection project underwent several stages, evolving in response to practical considerations and the goal of optimizing the balance between data quantity, quality, and computational efficiency:

1. **Initial Approach - Wiki API**: The project initially utilized the Wikipedia API to fetch random articles and extract text segments of 10, 20, and 50 words. However, this approach was soon found to be too slow and inefficient due to the API's rate limits. I eventually reused this script to get validation data. I want to get more than enough data so I don't need to worry about imbalance class, overfitting. (Although sometime too much data will also caused overfitting.)

2. **Switch to Wiki Abstract Dumps**: To overcome the limitations of live API calls, the project shifted to using Wikipedia abstract dumps. These dumps provided a more extensive and diverse dataset, comprising summaries of articles, thus serving as a representative sample of language usage. The size of these dumps varied significantly, ranging from 400MB to 1.5GB. I used ElementTree (xml.etree.ElementTree): A built-in Python library for parsing and creating XML data.

3. **Data Quantity and Computational Considerations**: At one point, over 45,000 data segments were extracted. However, it became evident that handling such a large dataset was not only time-consuming but also did not yield proportionately better results in model accuracy. Consequently, the data count was optimized to around 3,000 segments. This number represented a "sweet spot," offering a balance between sufficient data for model training and a manageable computational load for hyperparameter tuning.

4. **Data Collection and Cleaning Integration**: To enhance efficiency, the data collection (reading from dumps) and feature extraction were combined. This integration allowed for immediate identification and exclusion of outliers or non-representative data during the feature extraction phase. For instance:
   - **Vowel-Consonant Ratio**: Segments without vowels or consonants were discarded, as they do not represent typical language structures.
   - **Maximum Word Length**: Segments with words exceeding 30 characters were eliminated, as these often turned out to be URLs or non-standard text rather than regular language usage.

Some other data cleaning code involved removing punctuation and ensuring each text segment conformed to the expected word count. Feature extraction was performed on cleaned segments. Lines that did not conform to the expected format (e.g., missing language labels) were skipped to maintain data integrity.

### Training Process 

The training process for the language detection project was comprehensive and tailored to the specifics of the chosen models: the Decision Tree and the AdaBoost with Stumps. Here's a detailed breakdown:

#### Custom Train-Test Split
- A custom function was developed for splitting the data into training and testing sets. This function was specifically designed to suit the characteristics of Decision Trees and AdaBoost Stumps.

#### Hyperparameter Tuning
- Both models underwent hyperparameter tuning to optimize their performance.
- For the Decision Tree, the focus was on tuning the maximum depth and the minimum samples split. The maximum depth was capped at the number of features, and the minimum samples split was experimented with at 1%, 2%, and 5% of the total sampled data.
- In contrast, the AdaBoost Stumps model's hyperparameter tuning involved adjusting the number of learners (stumps) used in the model.

#### Sampling and Model Selection
- The project employed a dynamic approach to determining the ideal size of training and testing datasets. This was achieved through a loop that sampled varying amounts of data within a predefined range.
- At each iteration, the sampled data underwent training with different hyperparameters. The best parameters and models were tracked, focusing on validation set accuracy as the primary metric for model effectiveness.
- Decision Tree performance was found to be suboptimal compared to AdaBoost Stumps, prompting a greater focus on the latter.

#### Challenges and Future Directions
- An attempt was made to implement model saving without using external libraries. While pickle, a built-in Python library, was initially used, the goal was to explore alternative methods for a more granular control over the serialization process.
- Saving the Decision Tree model could potentially be managed through tree traversal algorithms (DFS or BFS) and reconstructing the tree from the traversal path. However, saving the AdaBoost Stumps model posed more complexity due to its ensemble nature.
- Due to time constraints, this aspect of the project was earmarked for future exploration.

Overall, the training process was marked by a blend of custom solutions and pragmatic decision-making, with a focus on balancing model accuracy and computational efficiency. The nuanced approach to hyperparameter tuning and data sampling played a crucial role in refining the models and driving the project towards its objectives.
