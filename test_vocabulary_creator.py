from vocabulary_creator import VocabularyCreator
import unittest
import json
from unittest.mock import patch

from vocabulary_creator import VocabularyCreator
import unittest
from unittest.mock import patch

class TestVocabularyCreator(unittest.TestCase):
    def setUp(self):
        self.mails = {
            "dataset": [
                {
                "mail": {
                    "Subject": "first time python",
                    "From": "profde@polymtl.ca",
                    "Date": "2022-01-21",
                    "Body": "hello, world !",
                    "Spam": "false",
                    "File": "enronds//enron1/ham/4536.2022-01-21.GP.Ham.txt"
                }
                },
                {
                "mail": {
                    "Subject": " hella spam",
                    "From": "spam-email@fraude.com",
                    "Date": "2020-02-30",
                    "Body": "hey hey sugar !",
                    "Spam": "true",
                    "File": "enronds//enron420/spam/0559.2020-02-30.GP.spam.txt"
                }
            }]
        } # données pour mocker "return_value" du "load_dict"
        self.clean_subject_spam = ['hella spam']  # données pour mocker "return_value" du "clean_text"
        self.clean_body_spam = ['hey hey sugar']  # données pour mocker "return_value" du "clean_text"
        self.clean_subject_ham = ['first time python']  # données pour mocker "return_value" du "clean_text"
        self.clean_body_ham = ['hello, world']  # données pour mocker "return_value" du "clean_text"
        self.vocab_expected = {
            'p_sub_spam': {'hey hey sugar': 1},
            'p_sub_ham': {'hey hey sugar': 1},
            'p_body_spam': {'hey hey sugar': 1},
            'p_body_ham': {'hey hey sugar': 1}
        }  # vocabulaire avec les valeurs de la probabilité calculées correctement

    def tearDown(self):
        pass

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    @patch("vocabulary_creator.VocabularyCreator.clean_text")
    @patch("vocabulary_creator.VocabularyCreator.write_data_to_vocab_file")
    def test_create_vocab_spam_Returns_vocabulary_with_correct_values(
        self, mock_write_data_to_vocab_file, mock_clean_text, mock_load_dict
    ):
        """Description: Tester qu'un vocabulaire avec les probabilités calculées
        correctement va être retourné. Il faut mocker les fonctions "load dict"
         (utiliser self.mails comme une simulation de valeur de retour),"clean text"
         (cette fonction va être appelée quelques fois, pour chaque appel on
         va simuler une valeur de retour differente, pour cela il faut utiliser
         side_effect (voir l'exemple dans l'énonce)) et
         "write_data_to_vocab_file" qui va simuler "return True" au lieu
         d'écrire au fichier "vocabulary.json".
         if faut utiliser self.assertEqual(appel_a_create_vocab(), self.vocab_expected)
        """
        mock_clean_text.return_value = self.clean_body_spam
        mock_load_dict.return_value = self.mails
        mock_write_data_to_vocab_file.return_value = True
        vocabulary_creator = VocabularyCreator()
        vocabulary_creator.create_vocab()
        self.assertEqual(vocabulary_creator.voc_data, self.vocab_expected)
        pass

    ###########################################
    #               CUSTOM TEST               #
    ###########################################