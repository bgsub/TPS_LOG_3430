import json
import math

from text_cleaner import TextCleaning


class EmailAnalyzer:
    """Classe pour classifier les e-mails comme spam ou non spam (ham)"""

    def __init__(self):
        self.vocab = "vocabulary.json"
        self.cleaning = TextCleaning()
        self.voc_data = {}

    def is_spam(self, subject_orig, body_orig, log_way_probs, log_way_merged_probs, stemming):
        '''
        Description: fonction pour verifier si e-mail est spam ou ham,
        en calculant les probabilites d'etre spam et ham,  de facon logarithmique ou pas
        en fonction du sujet et du texte d'email.
        Sortie: 'True' - si l'email est spam, 'False' - si email est ham.
        '''
        # Clean email's subject and body
        email_subject = self.clean_text(subject_orig, stemming)
        email_body = self.clean_text(body_orig, stemming)

        # Get the spam/ham probabilities
        p_subject_spam, p_subject_ham = self.spam_ham_subject_prob(email_subject, log_way_probs)
        p_body_spam, p_body_ham = self.spam_ham_body_prob(email_body, log_way_probs)

        # Compute the merged probabilities
        if log_way_merged_probs:
            # p_subject_spam is in decimal, so we tranform in log10
            p_spam = math.log10(p_subject_spam) * 0.6 + math.log10(p_body_spam) * 0.4
            # we retransform  in decimal
            p_spam = pow(p_spam, 10)
            # p_subject_gam is in decimal, so we tranform in log10
            p_ham = math.log10(p_subject_ham) * 0.6 + math.log10(p_body_ham) * 0.4
            # we retransform  in decimal
            p_ham = pow(p_ham, 10)
        else:
            p_spam = 0.6 * p_subject_spam + 0.4 * p_body_spam
            p_ham = 0.6 * p_subject_ham + 0.4 * p_body_ham
        # Decide is the email is spam or ham
        if p_spam > p_ham:
            return True
        else:
            return False

    def spam_ham_body_prob(self, body, log_way_probs):
        '''
        Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''
        # if we use log formula
        if log_way_probs:
            p_spam = 0.0
            p_ham = 0.0
        else:
            p_spam = 1.0
            p_ham = 1.0
        voc_data = self.load_dict()

        # Parse the text to compute the probability
        for word in body:
            # Check the spam probability
            if word in voc_data["p_body_spam"]:
                if log_way_probs:
                    p_spam += math.log10(voc_data["p_body_spam"][word])
                else:
                    p_spam *= voc_data["p_body_spam"][word]
            else:
                if log_way_probs:
                    try:
                        p_spam += 1.0 / math.log10(len(voc_data["p_body_spam"][word]) + 1.0)
                    except KeyError:
                        pass
                else:
                    p_spam *= 1.0 / (len(voc_data["p_body_spam"][word]) + 1.0)

            # Check the ham probability
            if word in voc_data["p_body_ham"]:
                if log_way_probs:
                    p_ham +=  math.log10(voc_data["p_body_ham"][word])
                else:
                    p_ham *= voc_data["p_body_ham"][word]
            else:
                if log_way_probs:
                    try:
                        p_ham += 1.0 / math.log10(len(voc_data["p_body_ham"][word]) + 1.0)
                    except KeyError:
                        pass
                else:
                    p_ham *= 1.0 / (len(voc_data["p_body_ham"][word]) + 1.0)

        # in the case of logs formula, the result is given in log, so we need to compute it in decimal after the
        # final calcul
        if log_way_probs:
            p_spam = pow(p_spam + (math.log(0.5925)), 10)
            p_ham = pow(p_ham + (math.log(0.4075)), 10)
        else:
            p_spam *= 0.5925
            p_ham *= 0.4075

        return p_spam, p_ham

    def clean_text(self, text, stemming):  # pragma: no cover
        return self.cleaning.clean_text(text, stemming)

    def spam_ham_subject_prob(self, email_subject, log_way_probs):
        '''
            Description: fonction pour calculer la probabilite
            que le sujet d'email est spam ou ham.
            Sortie: probabilite que email subject est spam, probabilite
            que email subject est ham.
            '''
        global word
        p_spam = 1.0
        p_ham = 1.0

        voc_data = self.load_dict()

        # Walk the text to compute the probability
        for word in email_subject:
            # Check the spam probability
            if word in voc_data["p_sub_spam"]:
                if log_way_probs:
                    p_spam += math.log10(voc_data["p_sub_spam"][word])
                else:
                    p_spam *= voc_data["p_sub_spam"][word]
            else:
                if log_way_probs:
                    try:
                        p_spam += 1.0 / math.log10(len(voc_data["p_sub_spam"][word]) + 1.0)
                    except KeyError:
                        pass
                else:
                    p_spam *= 1.0 / (len(voc_data["p_sub_spam"][word]) + 1.0)

        # Check the ham probability
        if word in voc_data["p_sub_ham"]:
            if log_way_probs:
                p_ham += math.log10(voc_data["p_sub_ham"][word])
            else:
                p_ham *= voc_data["p_sub_ham"][word]
        else:
            if log_way_probs:
                try:
                    p_ham += 1.0 / math.log10(len(voc_data["p_sub_ham"][word]) + 1.0)
                except KeyError:
                    pass
            else:
                p_ham *= 1.0 / (len(voc_data["p_sub_ham"][word]) + 1.0)

        # in the case of logs formula, the result is given in log, so we need to compute it in decimal after the final calcul
        if log_way_probs:
            p_spam = pow((p_spam + (math.log(0.5925))), 10)
            p_ham = pow((p_ham + (math.log(0.4075))), 10)
        else:
            p_spam *= 0.5925
            p_ham *= 0.4075

        return p_spam, p_ham

    def load_dict(self):  # pragma: no cover
        # Open vocabulary
        with open(self.vocab) as json_data:
            vocabu = json.load(json_data)

        return vocabu
