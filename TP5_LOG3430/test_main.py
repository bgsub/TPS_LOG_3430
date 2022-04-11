import unittest
import json
import random
import copy
from email_analyzer import EmailAnalyzer
from vocabulary_creator import VocabularyCreator
from text_cleaner import TextCleaning
from renege import RENEGE
class TestMain(unittest.TestCase):
    #cette methode est basee sur la mathode de evaluate de main.py mais prend en parametre le nom du fichier
    # elle retourne f1
    def evaluate(self,fileName):
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        total = 0
        analyzer = EmailAnalyzer()
        with open(fileName + ".json") as email_file:
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

            if ((analyzer.is_spam(subject, body))) and (spam == "true"):
                tp += 1
            if (not (analyzer.is_spam(subject, body))) and (spam == "false"):
                tn += 1
            if ((analyzer.is_spam(subject, body))) and (spam == "false"):
                fp += 1
            if (not (analyzer.is_spam(subject, body))) and (spam == "true"):
                fn += 1
            total += 1
        
        print("")
        precision = round(tp / (tp + fp), 2)
        recall = round(tp / (tp + fn), 2)
        f1=  2 * (precision * recall) / (precision + recall)
        # evaluate return f1 now
        return f1 
   # cette fonction est basee sur evaluate de main.py mais utilise fileName en parametre et retourne f1
    def open_file(self, fileName):
        with open(fileName + "_set.json") as email_file:
            file_contents = json.load(email_file)
        return file_contents
    def write_file(self, fileName, content):
        with open(fileName, "w") as outfile:
            json.dump(content, outfile, indent=2)
            
    def cleaner(self, fileName):
        global emails
        emails = self.open_file(fileName)
        textCleaner = TextCleaning()
        # on clean up tous les mails
        for index, e_mail in enumerate(emails["dataset"]):
            text_clean = textCleaner.clean_text(e_mail["mail"]["Body"])
            emails["dataset"][index]["mail"]["Body"] = ' '.join(text_clean)
       # on reecrit les tests cleans dans le fichier test/train_clean.json
        self.write_file(fileName+ "_clean.json",emails)

    def shuffle(self, fileName):
        emails = self.open_file(fileName)
        for index, e_mail in enumerate(emails["dataset"]):
            #on tokenize dans une liste
            body_part = e_mail["mail"]["Body"].split(' ')
            for i in range(10) :
                first_word_pos = random.randint(0, len(body_part) - 1)
                second_word_pos = random.randint(0, len(body_part) - 1)
                tmp = body_part[first_word_pos] 
                body_part[first_word_pos] = body_part[second_word_pos]
                body_part[second_word_pos] = tmp
                # on detokenize
            emails["dataset"][index]["mail"]["Body"] = ' '.join(body_part)
           # on reecrit les tests cleans dans le fichier test/train_clean.json
        self.write_file(fileName + "_shuffle.json",emails)

    def triplicate(self, fileName):
        emails = self.open_file(fileName)
        #permet de copier: deepcopy nous permet une copie sans modification de l original
        emails_copy = copy.deepcopy(emails)
        emails["dataset"] += emails["dataset"]
        emails["dataset"] += emails_copy["dataset"]
        self.write_file(fileName + "_x3.json",emails)
        
    def duplicate(self, fileName) :
        emails= self.open_file(fileName)
        for index, e_mail in enumerate(emails["dataset"]):
            body = e_mail["mail"]["Body"]
            body_part = body + body
            emails["dataset"][index]["mail"]["Body"] = body_part
        self.write_file(fileName + "_words.json",emails)

    def setUp(self):
        # on metamorphose le fichier test_json
        self.cleaner("test")
        self.shuffle("test")
        self.triplicate("test")
        self.duplicate("test")
        # on metamorphose le fichier train_json
        self.cleaner("train")
        self.shuffle("train")
        self.triplicate("train")
        self.duplicate("train")
    def training(self):
        vocab = VocabularyCreator("train_set")
        vocab.create_vocab()
        renege = RENEGE("train_set")
        renege.classify_emails()
    
    def test_test_clean(self):
        print("")
        print("Testing_test_clean")
        self.training() 
        f1_initial=self.evaluate("test_set")
        f1_final=self.evaluate("test_clean")
        print("f1 initial : " + str(f1_initial))
        print("f1 final : " + str(f1_final))
        self.assertTrue(((f1_initial / f1_final) < 1.03) and ((f1_initial / f1_final) > 0.97))
   
    def test_test_triplicate(self):
        print("")
        print("Test_test_triplicate")
        self.training()
        f1_initial=self.evaluate("test_set")
        f1_final= self.evaluate("test_x3")
        print("f1 initial : " + str(f1_initial))
        print("f1 final : " + str(f1_final))
        self.assertTrue(((f1_initial / f1_final) < 1.03) and ((f1_initial / f1_final) > 0.97))
     
    def test_test_shuffle(self):
        print("")
        print("Testing_test_shuffle")
        self.training() 
        f1_initial=self.evaluate("test_set")
        f1_final=self.evaluate("test_shuffle")
        print("f1 initial : " + str(f1_initial))
        print("f1 final : " + str(f1_final))
        self.assertTrue(((f1_initial / f1_final) < 1.03) and ((f1_initial / f1_final) > 0.97))
        
    def test_test_duplicate(self):
        print("")
        print("Testing_test_duplicate")
        self.training() 
        f1_initial=self.evaluate("test_set")
        f1_final=self.evaluate("test_words")
        print("f1 initial : " + str(f1_initial))
        print("f1 final : " + str(f1_final))
        self.assertTrue(((f1_initial / f1_final) < 1.03) and ((f1_initial / f1_final) > 0.97))
        
    def test_train_cleaner(self):
        print("")
        print("Testing_train_clean")
        self.training() 
        f1_initial=self.evaluate("train_set")
        f1_final=self.evaluate("train_clean")
        print("f1 initial : " + str(f1_initial))
        print("f1 final : " + str(f1_final))
        self.assertTrue(((f1_initial / f1_final) < 1.03) and ((f1_initial / f1_final) > 0.97))