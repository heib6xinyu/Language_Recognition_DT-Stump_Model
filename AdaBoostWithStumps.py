import math
import random
import pickle
from loadData import *
class DecisionStump:
    def __init__(self):
        self.polarity = 1
        self.feature_index = None
        self.threshold = None
        self.alpha = None

    def predict(self, X):
        predictions = []
        # Make predictions based on the threshold and polarity
        for sample in X:
            val = sample[self.feature_index]
            prediction = 1 if self.polarity * val < self.polarity * self.threshold else -1
            predictions.append(prediction)
        return predictions

class AdaBoost:
    def __init__(self, n_learners=5):
        self.n_learners = n_learners  # Number of weak learners (stumps) to use
        self.learners = []

    def fit(self, X, y):
        n_samples = len(X)
        w = [1 / n_samples for _ in range(n_samples)]  # Initialize weights

        for _ in range(self.n_learners):
            learner = DecisionStump()
            min_error = float('inf')

            # Iterate over each feature and find the best threshold
            for feature_i in range(len(X[0])):
                feature_values = [sample[feature_i] for sample in X]
                unique_values = set(feature_values)

                # Test all possible thresholds
                for threshold in unique_values:
                    p = 1
                    predictions = [1 if feature_values[i] < threshold else -1 for i in range(n_samples)]


                    # Calculate weighted error
                    missclassified = [w[i] for i in range(n_samples) if y[i] != predictions[i]]
                    error = sum(missclassified)

                    # Update polarity if error is more than 50%
                    if error > 0.5:
                        error = 1 - error
                        p = -1

                    # Store the best stump
                    if error < min_error:
                        learner.polarity = p
                        learner.threshold = threshold
                        learner.feature_index = feature_i
                        min_error = error

            # Calculate alpha (learner weight)
            EPS = 1e-10
            min_error = max(EPS, min(min_error, 1 - EPS))

            # Ensure the value inside the square root is non-negative
            value = (1.0 - min_error) / (min_error + EPS)
            learner.alpha = 0.5 * math.log(value) if value > 0 else 0

            predictions = learner.predict(X)

            # Update weights
            w = [w[i] * ((-learner.alpha * y[i] * predictions[i]) + 1) for i in range(n_samples)]
            w_sum = sum(w)
            w = [w_i / w_sum for w_i in w]  # Normalize weights

            self.learners.append(learner)

    def predict(self, X):
        final_output = [0 for _ in range(len(X))]
        # Aggregate predictions from all learners
        for learner in self.learners:
            learner_predictions = learner.predict(X)
            final_output = [final_output[i] + learner.alpha * learner_predictions[i] for i in range(len(X))]

        # Final prediction: sign of the aggregated predictions
        return [1 if prediction > 0 else -1 for prediction in final_output]

def tune_number_of_learners(X_train, y_train, X_val, y_val, learner_values):
    """
    Tunes the number of learners in the AdaBoost classifier.

    :param X_train: Training features.
    :param y_train: Training labels.
    :param X_val: Validation features.
    :param y_val: Validation labels.
    :param learner_values: List of number of learner values to try.
    :return: Best number of learners and the corresponding AdaBoost model.
    """
    best_n_learners = None
    best_accuracy = float('-inf')
    best_model = None

    for n_learners in learner_values:
        model = AdaBoost(n_learners=n_learners)
        model.fit(X_train, y_train)
        predictions = model.predict(X_val)
        accuracy = sum(1 for i in range(len(y_val)) if y_val[i] == predictions[i]) / len(y_val)

        if accuracy > best_accuracy:
            best_n_learners = n_learners
            best_accuracy = accuracy
            best_model = model

    return best_n_learners, best_accuracy, best_model



def preprocess_for_binary_classification(sample_data, target_class):
    """
    Preprocesses raw data strings for binary classification.

    :param sample_data: List of raw data strings, each containing features and a target label.
    :param target_class: The target class of interest for binary classification.
    :return: Tuple (X, y) where X is the feature matrix and y is the binary target array.
    """
    X = []
    y = []

    for line in sample_data:
        parts = line.split(':', 1)
        if len(parts) == 2:
            # Split the line into target label and features
            target_label, features_str = line.split(':', 1)
            # Convert features from string to float and strip spaces
            features = [float(feature.strip()) for feature in features_str.split(',')]
            # Append the processed data
            X.append(features)
            # Convert the target label to binary format (1 for target class, -1 for others)
            y.append(1 if target_label.strip() == target_class else -1)
        else:
            print("Skipping malformed line:", line)  # Print the malformed line and skip it

    return X, y



def train_test_split(X, y, test_size=0.2):
    combined = list(zip(X, y))
    random.shuffle(combined)
    split_idx = int(len(combined) * (1 - test_size))
    train_data, test_data = combined[:split_idx], combined[split_idx:]
    X_train, y_train = zip(*train_data)
    X_test, y_test = zip(*test_data)
    return list(X_train), list(y_train), list(X_test), list(y_test)

#def save_model_custom(model, filename):
#    with open(filename, 'w') as file:
#        for stump in model.learners:
#            file.write(f"{stump.feature_index},{stump.threshold},{stump.polarity},{stump.alpha}\n")

#def load_model_custom(filename):
#    model = AdaBoost(n_learners=0)  # Initialize with 0 learners
#    with open(filename, 'r') as file:
#        for line in file:
#            feature_index, threshold, polarity, alpha = map(float, line.strip().split(','))
#            stump = DecisionStump()
#            stump.feature_index = int(feature_index)
#            stump.threshold = threshold
#            stump.polarity = int(polarity)
#            stump.alpha = alpha
#            model.learners.append(stump)
#    return model

def save_adaboost_model(model, filename):
    with open(filename, 'wb') as file:
        pickle.dump(model, file)

def load_adaboost_model(filename):
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    return model



#data = load_data("iris.txt")
#print(data[:10])
## Assuming we're interested in classifying Iris-setosa (label 0) against other species
#X, y = preprocess_for_binary_classification(data, target_class=0)
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


## Example usage
#learner_values = [5, 10, 15]  # Example values for the number of learners
#best_n_learners, best_accuracy, best_model = tune_number_of_learners(X_train, y_train, X_test, y_test, learner_values)
#print(f"Best number of learners: {best_n_learners}")
#print("Best Accuracy:", best_accuracy)

#save_adaboost_model(best_model, 'best_ada_boost_model.pkl')
#loaded_ada_boost_model = load_adaboost_model('best_ada_boost_model.pkl')
#loaded_ada_boost_model.fit(X_train, y_train)
#predictions = loaded_ada_boost_model.predict(X_test)
#accuracy = sum(1 for i in range(len(y_test)) if y_test[i] == predictions[i]) / len(y_test)
#print(accuracy)

