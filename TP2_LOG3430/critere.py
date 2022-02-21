import sys
from crud import CRUD
from email_analyzer import EmailAnalyzer
from text_cleaner import TextCleaning

#fonction logique du problem et les 3 criteres (avec jeu de test)
def spam_logic_function(p, h, u, g):
    print("<{P=", p, end="")
    if h < 20:
        sys.stdout.write(", H= True")
    else:
        sys.stdout.write(", H= False")

    if u < 50:
        sys.stdout.write(", U= True")
    else:
        sys.stdout.write(", U= False")

    if not g >= 50:
        sys.stdout.write(", G= True},")
    else:
        sys.stdout.write(", G= False},")

    return p and (((h < 20) and (u < 50)) or ((u < 50) and not(g >= 50)))



def CACC():
    print("Jeu de test pour CACC : ")
    print("f1: ")
    print("{", spam_logic_function(True, 5, 5, 5), "}>")

    print("f2: ")
    print("{", spam_logic_function(False, 5, 5, 5), "}>")

    print("f3: ")
    print("{", spam_logic_function(False, 100, 500, 55), "}>")

    print("f4: ")
    print("{", spam_logic_function(True, 5, 200, 5), "}>")

    print("f5: ")
    print("{", spam_logic_function(True, 5, 200, 200), "}>")


def GICC():
    print("Jeu de test pour GICC : ")
    print("t1: ")
    print("{", spam_logic_function(True, 25, 55, 55), "}>")

    print("t2: ")
    print("{", spam_logic_function(False, 25, 55, 55), "}>")

    print("t3: ")
    print("{", spam_logic_function(True, 5, 5, 5), "}>")

    print("t4: ")
    print("{", spam_logic_function(False, 5, 100, 55), "}>")

    print("t5: ")
    print("{", spam_logic_function(True, 55, 5, 55), "}>")

    print("t6: ")
    print("{", spam_logic_function(False, 55, 5, 55), "}>")

    print("t7: ")
    print("{", spam_logic_function(False, 55, 55, 5), "}>")

def IC():
    print("Jeu de test pour IC : ")

    print("d1: ")
    print("{", spam_logic_function(True, 5, 5, 55), "}>")

    print("d2: ")
    print("{", spam_logic_function(True, 55, 55, 5), "}>")



class Criteria:
    def __init__(self):
        self.vocab = "vocabulary.json"
        self.crud = CRUD()
        self.cleaning = TextCleaning()
        self.voc_data = {}

    #implementation du spam
    def is_spam_critere(self, email, subject, body):

        user = email["From"]
        user_id = self.crud.get_user_id(user)
        user_trust = int(self.crud.get_user_data(user_id, "Trust"))

        date_of_last_seen_message = self.crud.get_user_data(user_id, "Date_of_last_seen_message")
        date_of_first_seen_message = self.crud.get_user_data(user_id, "Date_of_first_seen_message")

        date_of_last_seen_message_unix = self.crud.convert_to_unix(date_of_last_seen_message)
        date_of_first_seen_message_unix = self.crud.convert_to_unix(date_of_first_seen_message)
        diff_dates = date_of_last_seen_message_unix - date_of_first_seen_message_unix

        groups_list = str(self.crud.get_user_data(user_id, "Groups"))
        groups_len = len(groups_list)
        groups_trust_total = 0
        for group_name in groups_list:
            group_id = self.crud.get_group_id(group_name)
            groups_trust_total += int(self.crud.get_groups_data(group_id, "Trust"))

        avg_group_trust = groups_trust_total / groups_len
        analyzer = EmailAnalyzer()
        isSpam = analyzer.is_spam(subject, body)

        return (isSpam and
                ((diff_dates < 1728000 and user_trust < 50) or  # note 20 days in unix is 1728000
                 (user_trust < 50 and avg_group_trust < 50))
                )
        # S = P ∗ ((H ∗ U) + (U ∗ ¬G))
        # S valeur de retour
        # P isSpam
        # H is_there_less_20_days_between_first_and_last_message
        # U user_trust
        # G avg_group_trust

    #implementation du spam avec la forme DNF
    def is_spam_DNF(self, email, subject, body):

        user = email["From"]
        user_id = self.crud.get_user_id(user)
        user_trust = int(self.crud.get_user_data(user_id, "Trust"))

        date_of_last_seen_message = self.crud.get_user_data(user_id, "Date_of_last_seen_message")
        date_of_first_seen_message = self.crud.get_user_data(user_id, "Date_of_first_seen_message")

        date_of_last_seen_message_unix = self.crud.convert_to_unix(date_of_last_seen_message)
        date_of_first_seen_message_unix = self.crud.convert_to_unix(date_of_first_seen_message)
        diff_dates = date_of_last_seen_message_unix - date_of_first_seen_message_unix

        groups_list = str(self.crud.get_user_data(user_id, "Groups"))
        groups_len = len(groups_list)
        groups_trust_total = 0
        for group_name in groups_list:
            group_id = self.crud.get_group_id(group_name)
            groups_trust_total += int(self.crud.get_groups_data(group_id, "Trust"))

        avg_group_trust = groups_trust_total / groups_len
        analyzer = EmailAnalyzer()
        isSpam = analyzer.is_spam(subject, body)

        return (isSpam and diff_dates < 1728000 and user_trust < 50 or  # note 20 days in unix is 1728000
                isSpam and user_trust < 50 and avg_group_trust < 50
                )
        # S = P ∗ H ∗ U + P ∗ U ∗ ¬G
        # S valeur de retour
        # P isSpam
        # H is_there_less_20_days_between_first_and_last_message
        # U user_trust
        # G avg_group_trust
