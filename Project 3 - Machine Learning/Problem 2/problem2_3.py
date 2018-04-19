import csv
import sys
import numpy as np


def linearRegression(input_file, output_file):
    features = []
    labels = []

    # Opening files in read and write modes

    input_csv = csv.reader(open(input_file, newline=''), delimiter=',')
    output_csv = csv.writer(open(output_file, 'w', newline=''), delimiter=',')

    for line in input_csv:
        features.append([1.0, float(line[0]), float(line[1])])
        labels.append(float(line[2]))

    features = np.array(features)
    labels = np.array(labels)

    # Scaling the features to normalized values
    for i in [1, 2]:
        mean = np.mean(features[:, i])
        std_deviation = np.std(features[:, i])
        features[:, i] = (features[:, i] - mean) / std_deviation

    n = features.shape[0]
    test_alphas = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.2]
    iterations = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
    conv = np.zeros((100, 10))

    for i in range(len(test_alphas)):
        beta = [0.0, 0.0, 0.0]
        alpha = test_alphas[i]
        maxIterations = iterations[i]

        for p in range(maxIterations):
            classifier = np.dot(features, beta)
            error = classifier - labels
            highest_error = np.dot(error, error) / float(2 * n)
            conv[p, i] = highest_error

            nBeta = np.copy(beta)
            for j in range(3):
                nBeta[j] = beta[j] - alpha / float(n) * np.sum(error * features[:, j])
            beta = np.copy(nBeta)

        # Write output to the file
        np.concatenate(([alpha, maxIterations], beta))
        output_csv.writerow(np.concatenate(([alpha, maxIterations], beta)))

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    linearRegression(input_file, output_file)

