import math
import pickle
from loadData import *
class Node:
    def __init__(self, feature_index=None, threshold=None, value=None, left=None, right=None):
        self.feature_index = feature_index  # Index of feature to split on
        self.threshold = threshold  # Threshold value for the split
        self.value = value  # Class label for leaf nodes
        self.left = left  # Left subtree
        self.right = right  # Right subtree

def entropy(y):
    # Calculate entropy for a set of labels
    classes = set(y)
    entropy_value = 0.0
    for cls in classes:
        p = sum([(label == cls) for label in y]) / len(y)
        if p > 0:
            entropy_value -= p * math.log2(p)
    return entropy_value

def split_dataset(X, y, feature_index, threshold):
    # Split dataset based on a feature and threshold
    left_X, left_y, right_X, right_y = [], [], [], []
    for i in range(len(X)):
        if X[i][feature_index] <= threshold:
            left_X.append(X[i])
            left_y.append(y[i])
        else:
            right_X.append(X[i])
            right_y.append(y[i])
    return left_X, left_y, right_X, right_y

def build_tree(X, y, depth=0, max_depth=None, min_samples_split=2):
    # Base case: max depth reached or not enough samples to split
    if max_depth is not None and depth >= max_depth or len(y) < min_samples_split:
        return Node(value=max(set(y), key=y.count))

    num_features = len(X[0])
    best_feature, best_threshold, best_score, best_sets = None, None, float('inf'), None

    for feature_index in range(num_features):
        feature_values = set([entry[feature_index] for entry in X])
        for threshold in feature_values:
            left_X, left_y, right_X, right_y = split_dataset(X, y, feature_index, threshold)
            if len(left_y) < min_samples_split or len(right_y) < min_samples_split:
                continue  # Skip splits that don't satisfy the minimum sample split criterion

            impurity = len(left_y) * entropy(left_y) + len(right_y) * entropy(right_y)
            if impurity < best_score:
                best_feature, best_threshold, best_score, best_sets = feature_index, threshold, impurity, (left_X, left_y, right_X, right_y)

    if best_score == float('inf'):
        return Node(value=max(set(y), key=y.count))

    left = build_tree(*best_sets[0:2], depth=depth + 1, max_depth=max_depth, min_samples_split=min_samples_split)
    right = build_tree(*best_sets[2:4], depth=depth + 1, max_depth=max_depth, min_samples_split=min_samples_split)
    return Node(feature_index=best_feature, threshold=best_threshold, left=left, right=right)


def print_tree(node, depth=0):
    # Print the decision tree
    if node.value is not None:
        print('  ' * depth, 'Predict:', node.value)
    else:
        print('  ' * depth, f'Feature {node.feature_index} <= {node.threshold}')
        print_tree(node.left, depth + 1)
        print_tree(node.right, depth + 1)



# Function to predict a single data point using the decision tree
def predict(tree, data_point):
    if tree.value is not None:
        return tree.value
    else:
        if data_point[tree.feature_index] <= tree.threshold:
            return predict(tree.left, data_point)
        else:
            return predict(tree.right, data_point)

def hyperparameter_tuning(X_train, y_train, X_val, y_val, max_depth_values, min_samples_split_values):
    best_max_depth = None
    best_min_samples_split = None
    best_accuracy = float('-inf')
    best_tree = None

    for max_depth in max_depth_values:
        for min_samples_split in min_samples_split_values:
            tree = build_tree(X_train, y_train, max_depth=max_depth, min_samples_split=min_samples_split)
            predictions = [predict(tree, x) for x in X_val]
            accuracy = sum(1 for i in range(len(y_val)) if y_val[i] == predictions[i]) / len(y_val)

            if accuracy > best_accuracy:
                best_max_depth = max_depth
                best_min_samples_split = min_samples_split
                best_accuracy = accuracy
                best_tree = tree

    return best_max_depth, best_min_samples_split, best_accuracy, best_tree

#def serialize_tree(node):
#    if node is None:
#        return 'None,None,None,'

#    # Serialize the current node
#    node_data = f'{node.feature_index},{node.threshold},{node.value},'
#    # Serialize left and right subtrees
#    left_subtree = serialize_tree(node.left)
#    right_subtree = serialize_tree(node.right)

#    return node_data + left_subtree + right_subtree

#def save_tree_to_file(tree, filename):
#    tree_string = serialize_tree(tree)  # Directly serialize the tree node passed
#    with open(filename, 'w') as file:
#        file.write(tree_string)

#def deserialize_tree(data_list):
#    print(data_list)
#    if data_list[0] == 'None':
#        print("no child or leaf with class")
#        print(data_list[:3])
#        # It's a leaf node with a class prediction
#        if data_list[2] != 'None':
#            value = int(data_list[2])
#            data_list.pop(0)  # Remove 'None' for feature_index
#            data_list.pop(0)  # Remove 'None' for threshold
#            data_list.pop(0)  # Remove value
#            print("leaf with class")
#            print(value)
#            return Node(value=value)
#        # No further child node
#        else:
#            print("no child")
#            data_list.pop(0)  # Remove 'None' for feature_index
#            data_list.pop(0)  # Remove 'None' for threshold
#            data_list.pop(0)  # Remove 'None' for value
#            return None
    
#    # Extract node data for non-leaf nodes
#    feature_index = int(data_list[0])
#    threshold = float(data_list[1])
#    data_list.pop(0)  # Remove feature_index
#    data_list.pop(0)  # Remove threshold
#    data_list.pop(0)  # Remove 'None' for value

#    # Create a new internal node
#    node = Node(feature_index=feature_index, threshold=threshold)
#    print(node.value)
#    # Recursively build the left and right subtrees
#    node.left = deserialize_tree(data_list)
#    node.right = deserialize_tree(data_list)

#    return node

#def load_tree_from_file(filename):
#    with open(filename, 'r') as file:
#        tree_string = file.read()
#    data_list = tree_string.split(',')
#    return deserialize_tree(data_list)

def save_model_with_pickle(model, filename):
    with open(filename, 'wb') as file:
        pickle.dump(model, file)

def load_model_with_pickle(filename):
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    return model

#from sklearn.datasets import load_iris
#from sklearn.model_selection import train_test_split

## Load the Iris dataset
#iris = load_iris()
#X = iris.data
#y = iris.target

## Split the dataset into training and validation sets
#X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

## Define hyperparameter ranges to tune
#max_depths = [2, 3, 4, 5]
#min_samples_splits = [2, 3, 4]

## Perform hyperparameter tuning
#best_max_depth, best_min_samples_split, best_accuracy, best_tree= hyperparameter_tuning(X_train, y_train, X_val, y_val, max_depths, min_samples_splits)

#print("Best Max Depth:", best_max_depth)
#print("Best Min Sample Split:", best_min_samples_split)
#print("Best Accuracy:", best_accuracy)
#print_tree(best_tree)
##save_tree_to_file(best_tree, "best_tree.txt")
##tree = load_tree_from_file("best_tree.txt")
#save_model_with_pickle(best_tree, 'best_tree.pkl')
#loaded_tree = load_model_with_pickle('best_tree.pkl')
#print_tree(loaded_tree)

#data = load_data()
#sampled_data = sample_data(data, 10000)
#X,y = process_raw_data(sampled_data)
#X_train, y_train, X_test, y_test = split_data(X, y)
#means, stds = calculate_mean_std(X_train)
#X_train = normalize_data(X_train, means, stds)
#X_test = normalize_data(X_test, means, stds)
#max_depths = [3, 4, 5]
#min_samples_splits = [100, 200, 500]
#best_max_depth, best_min_samples_split, best_accuracy, best_tree= hyperparameter_tuning(X_train, y_train, X_test, y_test, max_depths, min_samples_splits)
#print("Best Max Depth:", best_max_depth)
#print("Best Min Sample Split:", best_min_samples_split)
#print("Best Accuracy:", best_accuracy)
#print_tree(best_tree)