import sys
import csv

def pla(input_file, output_file):
    features = []
    labels = []

    input_csv = csv.reader(open(input_file, newline=''), delimiter=',')
    output_csv = csv.writer(open(output_file, 'w', newline=''), delimiter=',')
    for line in input_csv:
        features.append([float(line[0]), float(line[1]), 1.0])
        labels.append(float(line[2]))

    print(features, labels)

    weights = [0.0, 0.0, 0.0]
    check = True
    while check:
        old_weights = weights
        for index in range(len(features)):
            x = features[index]
            y = labels[index]
            classifier = sum([x[i] * weights[i] for i in range(3)])

            if classifier * y <= 0:
                weights = [weights[i] + y * x[i] for i in range(3)]

        output_csv.writerow(weights)

        if old_weights == weights:
            check = False


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    pla(input_file, output_file)