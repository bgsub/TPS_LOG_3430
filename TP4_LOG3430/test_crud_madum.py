from crud import CRUD
import unittest
import datetime
from unittest.mock import patch

class TestCrudMadum(unittest.TestCase):
    def setUp(self):
        # ceci est l exemple de 'mock' utilisé dans le fichier test_crud.py pour le return value de read_users_file
        self.users_data = {
            "1": {
                "name": "alex@gmail.com",
                "Trust": 100,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            },
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "SpamN": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            }
        }
         # ceci est une partie de  l exemple de 'mock' utilisé dans le fichier test_crud.py pour le return value de read_groups_file
         # le groupe default n est pas ajouté pour tester le le constructeur.
        self.groups_data = {
            "1": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }
    def tearDown(self):
        pass

    
    # tests du constructeur (C) du modele MaDUM pour l' attribut groups_data
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_constructor_crud(self,mock_read_users_file,mock_read_groups_file):
        mock_read_users_file = self.users_data
        mock_read_groups_file = self.groups_data
        crud_obj = CRUD()
        
        self.assertEqual(crud_obj.get_groups_data(1, "name"), "friends")
        self.assertEqual(crud_obj.get_groups_data(1, "Trust"), 90)
        self.assertEqual(crud_obj.get_groups_data(1, "List_of_members"), ["alex@gmail.com"])
       #cas si le groupe default n est pas ajouté
        self.assertEqual(crud_obj.get_groups_data(2, "name"), "default")
        self.assertEqual(crud_obj.get_groups_data(2, "Trust"), 50)
        self.assertEqual(crud_obj.get_groups_data(2, "List_of_members"), [])
    
    # tests des rapporteurs (R) du modele maDUM pour l' attribut groups_data
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_get_groups_data(self,mock_read_users_file,mock_read_groups_file):
        mock_read_users_file = self.users_data
        mock_read_groups_file = self.groups_data
        crud_obj = CRUD()
        
        name_group_1 = crud_obj.get_groups_data(1, "name")
        trust_group_1 = crud_obj.get_groups_data(1, "Trust")
        list_members_group_1 = crud_obj.get_groups_data(1, "List_of_members")
        
        name_group_2 = crud_obj.get_groups_data(2, "name")
        trust_group_2 = crud_obj.get_groups_data(2, "Trust")
        list_members_group_2 = crud_obj.get_groups_data(2, "List_of_members")
        
        self.assertEqual(name_group_1, "friends")
        self.assertEqual(trust_group_1, 90)
        self.assertEqual(list_members_group_1, ["alex@gmail.com"])
        
        self.assertEqual(name_group_1, "default")
        self.assertEqual(trust_group_1, 50)
        self.assertEqual(list_members_group_1, [])
    
    # tests des transformateurs (T) du modele maDUM pour l' attribut groups_data
        #d1
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_add_new_group_update_groups_remove_group_remove_group_member(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud_obj = CRUD()
        crud.add_new_group("inf3430", 100, ["yanbra@polymtl.ca"])
        crud.update_groups(2, "name", "just_inf")
        crud.remove_group("1")
        crud.remove_group_member(2, "yanbra@polymtl.ca")

        self.assertEqual(crud.get_groups_data(1, "name"), False)
        self.assertEqual(crud.get_groups_data(2, "name"), "inf3430")
        self.assertEqual(crud.get_groups_data(2, "name"),"just_inf")
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), [])
        #d2
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_update_groups_add_new_group_remove_group_remove_group_member(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud_obj = CRUD()
        crud.update_groups(1, "Trust", 69)
        self.assertEqual(crud_objet.get_groups_data(1, "Trust"), 69)
        crud_obj.add_new_group("inf3430", 99, ["yanbra@polymtl.ca"])
        crud_obj.remove_group("1")
        crud_obj.remove_group_member(2, "yanbra@polymtl.ca")

        self.assertEqual(crud_obj.get_groups_data(1, "name"), False)
        self.assertEqual(crud_obj.get_groups_data(2, "name"), "inf3430")
        self.assertEqual(crud_obj.get_groups_data(2, "Trust"), 99)
        self.assertEqual(crud_obj.get_groups_data(2, "List_of_members"), [])
        #d3
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_remove_group_add_new_group_update_group_remove_group_member(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud_obj = CRUD()
        
        crud_obj.remove_group("1")
        self.assertEqual(crud_objet.get_groups_data(1, "Trust"), False)
        crud_obj.add_new_group("inf3430", 98, ["yanbra@polymtl.ca"])
        crud.update_groups(1, "Trust", 99)
        crud_obj.remove_group_member(1, "yanbra@polymtl.ca")
        self.assertEqual(crud_obj.get_groups_data(1, "name"), "inf3430")
        self.assertEqual(crud_obj.get_groups_data(1, "Trust"), 99)
        self.assertEqual(crud_obj.get_groups_data(1, "List_of_members"), [])
     #d4
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_add_new_group_remove_group_update_groups_remove_group_member(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud_obj = CRUD()
        
        crud_obj.add_new_group("inf3430", 98, ["yanbra@polymtl.ca"])
        
        crud_obj.remove_group("1")
        self.assertEqual(crud_objet.get_groups_data(1, "Trust"), False)
        crud.update_groups(2, "Trust", 99)
        crud_obj.remove_group_member(1, "yanbra@polymtl.ca")
        self.assertEqual(crud_obj.get_groups_data(2, "name"), "inf3430")
        self.assertEqual(crud_obj.get_groups_data(2, "Trust"), 99)
        self.assertEqual(crud_obj.get_groups_data(2, "List_of_members"), [])
    
    
    # tests des autres (O) du modele maDUM pour l' attribut groups_data
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_get_new_group_id(self,mock_read_users_file,mock_read_groups_file):
        mock_read_users_file = self.users_data
        mock_read_groups_file = self.groups_data
        crud_obj = CRUD()
        
        new_id = crud_obj.get_new_group_id()
        
        self.assertEqual(new_id, "3")