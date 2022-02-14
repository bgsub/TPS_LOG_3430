import json
import math
import sys
from crud import CRUD
from datetime import timezone, datetime
from text_cleaner import TextCleaning


class Criteria:
    def is_spam(self, email, subject, body, function_spamham_proba, function_merged_proba, function_text_cleaning):

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

        isSpam = self.is_spam(subject, body, function_spamham_proba, function_merged_proba, function_text_cleaning)
        return (isSpam and
                ((diff_dates < 1728000 and user_trust < 50) or  # note 20 days in unix is 1728000
                 (user_trust < 50 and avg_group_trust >= 50))
                )
        # S = P ∗ ((H ∗ U) + (U ∗ ¬G))
        # S valeur de retour
        # P isSpam
        # H is_there_less_20_days_between_first_and_last_message
        # U user_trust
        # G avg_group_trust

    def is_spam_DNF(self, email, subject, body, function_spamham_proba, function_merged_proba, function_text_cleaning):

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

        isSpam = self.is_spam(subject, body, function_spamham_proba, function_merged_proba, function_text_cleaning)
        return (isSpam and diff_dates < 1728000 and user_trust < 50 or  # note 20 days in unix is 1728000
                isSpam and user_trust < 50 and avg_group_trust >= 50
                )
        # S = P ∗ H ∗ U + P ∗ U ∗ ¬G
        # S valeur de retour
        # P isSpam
        # H is_there_less_20_days_between_first_and_last_message
        # U user_trust
        # G avg_group_trust
