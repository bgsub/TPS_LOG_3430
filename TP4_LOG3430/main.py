import csv
import json

from email_analyzer import EmailAnalyzer
from renege import RENEGE
from vocabulary_creator import VocabularyCreator


def evaluate(log_way_probs,log_way_merged_probs,stemming):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0
    analyzer = EmailAnalyzer()
    with open("test_set.json") as email_file:
        new_emails = json.load(email_file)

    i = 0
    email_count = len(new_emails["dataset"])

    print("Evaluating emails ")
    for e_mail in new_emails["dataset"]:
        i += 1
        print("\rEmail " + str(i) + "/" + str(email_count), end="")

        new_email = e_mail["mail"]
        subject = new_email["Subject"]
        body = new_email["Body"]
        spam = new_email["Spam"]

        # Bayes probabilities
        if (analyzer.is_spam(subject, body,log_way_probs,log_way_merged_probs,stemming)) and (spam == "true"):
            tp += 1
        if (not (analyzer.is_spam(subject, body,log_way_probs,log_way_merged_probs,stemming))) and (spam == "false"):
            tn += 1
        if (analyzer.is_spam(subject, body,log_way_probs,log_way_merged_probs,stemming)) and (spam == "false"):
            fp += 1
        if (not (analyzer.is_spam(subject, body,log_way_probs,log_way_merged_probs,stemming))) and (spam == "true"):
            fn += 1
        total += 1

    accuracyResult = "Accuracy: ", round((tp + tn) / (tp + tn + fp + fn), 2)
    precisionResult= "Precision: ", round(tp / (tp + fp), 2)
    recallResult = "Recall: ", round(tp / (tp + fn), 2)
    print("\n")
    jointString = accuracyResult + precisionResult + recallResult
    return jointString


def readCsvFile(fileName):
    csv_file = open(fileName)
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = list(csv_reader)

    return data


def execute(args1, args2, args3, args4):
    # args1 = probabilities for spam/ham
    # args2 = combinatory probabilities for spam/ham
    # args3 = vocabulary frequency
    # args4 = stemming
    vocab = VocabularyCreator()
    vocab.create_vocab(args3, args4)

    # 2. Classification des emails et initialisation de utilisateurs et groupes.
    renege = RENEGE()
    renege.classify_emails(args1,args2,args4)

    # 3. Evaluation de performance du modele avec la fonction evaluate()
    return str(evaluate(args1, args2,args4))


if __name__ == "__main__":
    # preparing test result file
    file = open('results.txt', 'w')
    # executing csv file
    data = readCsvFile('TP3_system-output-3.csv')
    data = data[7:]  # substract useless lines in csv file, we start at 7 because of headers
    testIndex = 0
    for row in data:
        rowDataResults = execute(row[0], row[1], row[2], row[3])
        file.write("Test case: " + str(testIndex))
        file.write("\n")
        file.write(rowDataResults)
        file.write("\n\n")
        testIndex += 1

    # 1. Creation de vocabulaire.
    # vocab = VocabularyCreator()
    # vocab.create_vocab()
    #
    # # 2. Classification des emails et initialisation des utilisateurs et des groupes.
    # renege = RENEGE()
    # renege.classify_emails()
    #
    # # 3. Evaluation de performance du modele avec la fonction evaluate()
    # evaluate()
