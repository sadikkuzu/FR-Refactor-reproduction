import pickle
import random

def load_dataset():
    file = open("./dataset/shuffle_dataset.pickle", "rb")
    dataset = pickle.load(file)
    file.close()
    print("dataset of length " , len(dataset) , " is loaded.....")
    return dataset

def load_features():
    # file = open("./dataset/features.pickle", "rb")
    file = open("./dataset/features_without_pp.pickle", "rb")
    features = pickle.load(file)
    file.close()
    print("features of length " , len(features) , " is loaded.....")
    # print(features[:100])
    return features

def find_features(w_features, t_words):
    words = t_words
    features = {}
    for f in w_features:
        features[f] = 0

    for f in features:
        if f in words:
            features[f] += 1
    return features


def make_featuresets(word_features):

    documents_f = open("./T&T/testing.pickle", "rb")
    testing_files = pickle.load(documents_f)
    documents_f.close()
    print(str(len(testing_files)) + " testing files loaded.....")

    testing_featureset = []

    for index in range(len(testing_files)):
        testing_featureset.append(
            [find_features(word_features, testing_files[index][2]),
             testing_files[index][1]])

    save_featuresets = open("./feature_modeling/testing_featureset.pickle", "wb")
    pickle.dump(testing_featureset, save_featuresets)
    save_featuresets.close()
    print("testing featuresets saved.....")
    print("===============>")

    for t_index in range(10):
        documents_f = open("./T&T/training" + str(t_index + 1) +".pickle", "rb")
        training_files = pickle.load(documents_f)
        documents_f.close()
        print(str(len(training_files)) + " training files loaded.....")

        training_featureset = []

        for index in range(len(training_files)):
            training_featureset.append(
                [find_features(word_features, training_files[index][2]),
                 training_files[index][1]])

        save_featuresets = open("./feature_modeling/training_featureset" + str(t_index + 1) + ".pickle","wb")
        pickle.dump(training_featureset, save_featuresets)
        save_featuresets.close()
        print("training featuresets " + str(t_index + 1) + " saved.....")
        print("===============>")


if __name__ == '__main__':
    # dataset = load_dataset()
    features = load_features()
    # saperate_training_and_testing_data(dataset)
    make_featuresets(features)

