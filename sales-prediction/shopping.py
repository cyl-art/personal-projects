import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open('shopping.csv') as f:
        reader = csv.reader(f)
        next(reader)
        data = []
        data.append([])  # list for evidence
        data.append([])  # list for labels
        count = 0  # ensuring that we don't include headings
        for row in reader:
            if count == 0:
                count += 1
            if count >= 1:
                data[0].append(row[:17])
                data[1].append(row[17])
        # traversing evidence
        for evidence in data[0]:
            # converting to ints
            evidence[0] = int(evidence[0])
            evidence[2] = int(evidence[2])
            evidence[4] = int(evidence[4])
            # month
            evidence[10] = month_string_to_number(evidence[10])
            evidence[11] = int(evidence[11])
            evidence[12] = int(evidence[12])
            evidence[13] = int(evidence[13])
            evidence[14] = int(evidence[14])
            # visitor_type
            evidence[15] = 1 if evidence[15] == 'Returning_Visitor' else 0
            # weekend
            evidence[16] = 1 if evidence[16] == 'TRUE'else 0
            # converting to floats
            evidence[1] = float(evidence[1])
            evidence[3] = float(evidence[3])
            evidence[5] = float(evidence[5])
            evidence[6] = float(evidence[6])
            evidence[7] = float(evidence[7])
            evidence[8] = float(evidence[8])
            evidence[9] = float(evidence[9])
        # traversing labels
        for index, label in enumerate(data[1]):
            if label == 'TRUE':
                data[1][index] = 1
            else:
                data[1][index] = 0
        data = tuple(data)
        return data

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    return model.fit(evidence, labels)

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_labels_sensitivity = 0
    true_labels_specificity = 0
    for true_label in labels:
        if true_label == 1:
            true_labels_sensitivity += 1
        else:
            true_labels_specificity += 1
    predicted_labels_sensitivity = 0
    predicted_labels_specificity = 0
    for predicted_label, true_label in zip(predictions, labels):
        if predicted_label == true_label and true_label == 1:
            predicted_labels_sensitivity += 1
        if predicted_label == true_label and true_label == 0:
            predicted_labels_specificity += 1
    sensitivity = predicted_labels_sensitivity / true_labels_sensitivity
    specificity = predicted_labels_specificity / true_labels_specificity
    return sensitivity, specificity
def month_string_to_number(string):
    m = {
        'jan': 0,
        'feb': 1,
        'mar': 2,
        'apr':3,
         'may':4,
         'jun':5,
         'jul':6,
         'aug':7,
         'sep':8,
         'oct':9,
         'nov':10,
         'dec':11
        }
    s = string.strip()[:3].lower()
    out = m[s]
    return out


if __name__ == "__main__":
    main()

