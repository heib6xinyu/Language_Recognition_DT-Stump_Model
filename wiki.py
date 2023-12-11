import argparse
import sys

from loadData import *
from DecisionTree import *
from AdaBoostWithStumps import *
from featureExtraction import *
def hyperparameter_tuning_process(data,sample_size= 1000):
    print(f"Processing sample size: {sample_size}")

    sampled_data = sample_data(data, sample_size)
    X, y = process_raw_data(sampled_data)
    X_train, y_train, X_test, y_test = split_data(X, y)

    ## Calculate mean and standard deviation for normalization
    #means, stds = calculate_mean_std(X_train)
    #X_train = normalize_data(X_train, means, stds)
    #X_test = normalize_data(X_test, means, stds)

    # Adjust min_samples_splits based on sample size
    min_samples_splits = [int(sample_size * p) for p in [0.01, 0.02, 0.05]]
    max_depths = [3, 4, 5]

    # Perform hyperparameter tuning
    best_max_depth, best_min_samples_split, best_accuracy, best_tree = hyperparameter_tuning(X_train, y_train, X_test, y_test, max_depths, min_samples_splits)

    print("Best Max Depth:", best_max_depth)
    print("Best Min Sample Split:", best_min_samples_split)
    print("Best Accuracy:", best_accuracy)

    model_filename = f"tree_sample_size_{sample_size}_acc_{best_accuracy}_max_dep_{best_max_depth}_min_split_{best_min_samples_split}.pkl"
    save_model_with_pickle(best_tree, model_filename)
    print(f"Model saved as '{model_filename}'")

def hyperparameter_tuning_for_adab(data, sample_size):
    
    print(f"Processing sample size: {sample_size}")
    print()
    print("Training for italian:")
    sampled_data = sample_data(data, sample_size)
    X, y = preprocess_for_binary_classification(sampled_data, "it")

    X_train, y_train, X_test, y_test = train_test_split(X, y)
    learner_values = [10, 15, 50, 100]

    best_n_learners, best_accuracy, best_ada_model = tune_number_of_learners(X_train, y_train, X_test, y_test, learner_values)
    print(f"Best number of learners: {best_n_learners}")
    print("Best Accuracy:", best_accuracy)

    model_filename = f"IT_adab_sample_size_{sample_size}_acc_{best_accuracy}_n_learners_{best_n_learners}.pkl"
    save_adaboost_model(best_ada_model, model_filename)
    print(f"Model saved as '{model_filename}'")

    X, y = preprocess_for_binary_classification(sampled_data, "nl")

    X_train, y_train, X_test, y_test = train_test_split(X, y)
    learner_values = [10, 15, 50, 100]

    best_n_learners, best_accuracy, best_ada_model = tune_number_of_learners(X_train, y_train, X_test, y_test, learner_values)
    print(f"Best number of learners: {best_n_learners}")
    print("Best Accuracy:", best_accuracy)

    model_filename = f"NL_adab_sample_size_{sample_size}_acc_{best_accuracy}_n_learners_{best_n_learners}.pkl"
    save_adaboost_model(best_ada_model, model_filename)
    print(f"Model saved as '{model_filename}'")

    X, y = preprocess_for_binary_classification(sampled_data, "en")

    X_train, y_train, X_test, y_test = train_test_split(X, y)
    learner_values = [10, 15, 50, 100]

    best_n_learners, best_accuracy, best_ada_model = tune_number_of_learners(X_train, y_train, X_test, y_test, learner_values)
    print(f"Best number of learners: {best_n_learners}")
    print("Best Accuracy:", best_accuracy)

    model_filename = f"EN_adab_sample_size_{sample_size}_acc_{best_accuracy}_n_learners_{best_n_learners}.pkl"
    save_adaboost_model(best_ada_model, model_filename)
    print(f"Model saved as '{model_filename}'")

def train_model(sample_size):
    # Load data
    data = load_data()
    print("Training Decision Tree")
    hyperparameter_tuning_process(data,sample_size)
    print()
    print("Training AdaBoost")
    hyperparameter_tuning_for_adab(data,sample_size)

    pass


def predict_multiclass(models, X):
    """
    Predicts class labels for samples using multiple AdaBoost models in a One-vs-All strategy.

    Parameters:
    models (list): A list of AdaBoost models where each model is trained to identify a specific class.
    X (list of lists): Input samples to be classified. Each sample is a list of feature values.

    Returns:
    list: Predicted class labels for each input sample. The label corresponds to the model with the highest score.

    Example:
    >>> y_pred = predict_multiclass(models, X_test)
    """

    predictions = []
    class_labels = ['it', 'nl', 'en']
    for sample in X:
        # Get the prediction score for each class
        scores = [model.predict([sample])[0] for model in models]
        # Choose the class with the highest score
        predicted_class = scores.index(max(scores))
        predictions.append(class_labels[predicted_class])
    return predictions


def predict_all(model_type, datafile):
    extract(datafile)
    X_test = []
    with open("input_feature.txt", 'r', encoding='utf-8') as infile:
        for line in infile:
            if line.strip():  # Skip empty lines
                features = [float(x.strip()) for x in line.split(',') if x.strip()]

                # Append the processed data
                X_test.append(features)

    if model_type == 'tree':
        model = load_model_with_pickle('best_tree_sample_size_3000_acc_0.8031145717463849_max_dep_4_min_split_150.pkl')  
        y_pred = []
        for x in X_test:
            y_pred.append(predict(model,x))
        with open("tree_prediction.txt", 'w', encoding='utf-8') as outfile:
            for prediction in y_pred:
                outfile.write(str(prediction) + '\n')
    elif model_type == 'stumps' or model_type == 'best':
        model_it = load_adaboost_model("IT_adab_sample_size_1500_acc_0.9566666666666667_n_learners_10.pkl")
        model_nl = load_adaboost_model("NL_adab_sample_size_1500_acc_0.83_n_learners_50.pkl")
        model_en = load_adaboost_model("EN_adab_sample_size_1500_acc_0.81_n_learners_15.pkl")
        models = [model_it,model_nl,model_en]
        y_pred = predict_multiclass(models, X_test)
        with open("stumps_prediction.txt", 'w', encoding='utf-8') as outfile:
            for prediction in y_pred:
                outfile.write(str(prediction) + '\n')
    #elif model_type == 'best':
    #    model = BestModel()  # Load or initialize your best overall model

    ## Load test cases from datafile
    ## For each test case, make a prediction using the loaded model
    ## Print out the language prediction for each test case
    #pass

def main():
    parser = argparse.ArgumentParser(description="Wiki Language Classification")
    subparsers = parser.add_subparsers(dest='command')

    # Train subparser
    train_parser = subparsers.add_parser('train')
    train_parser.add_argument('sample_data_amount', type=int, help="Amount of sample data for training, default is 1000, you can try higher number but not recommend.")

    # Predict subparser
    predict_parser = subparsers.add_parser('predict')
    predict_parser.add_argument('model_type', choices=['tree', 'stumps', 'best'])
    predict_parser.add_argument('datafile', help="Data file for making predictions")

    args = parser.parse_args()

    if args.command == 'train':
        train_model(args.sample_data_amount)
    elif args.command == 'predict':
        predict_all(args.model_type, args.datafile)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()