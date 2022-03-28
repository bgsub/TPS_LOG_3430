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
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud_obj = CRUD()        
        crud_obj.groups_data = self.groups_data
          
        self.assertEqual(crud_obj.get_groups_data(1, "name"), "friends")
        self.assertEqual(crud_obj.get_groups_data(1, "Trust"), 90)
        self.assertEqual(crud_obj.get_groups_data(1, "List_of_members"), ["alex@gmail.com"])
       #cas si le groupe default n'existe pas
        self.assertEqual(crud_obj.get_groups_data(2, "name"), False)
        self.assertEqual(crud_obj.get_groups_data(2, "Trust"), False)
        self.assertEqual(crud_obj.get_groups_data(2, "List_of_members"), False)
       
    
    # tests des rapporteurs (R) du modele maDUM pour l' attribut groups_data
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_get_groups_data(self):
        #mock_read_users_file = self.users_data
        #mock_read_groups_file = self.groups_data
        crud_obj = CRUD()
        crud_obj.groups_data = self.groups_data

        name_group_1 = crud_obj.get_groups_data(1, "name")
        trust_group_1 = crud_obj.get_groups_data(1, "Trust")
        list_members_group_1 = crud_obj.get_groups_data(1, "List_of_members")
        
        self.assertEqual(name_group_1, "friends")
        self.assertEqual(trust_group_1, 90)
        self.assertEqual(list_members_group_1, ["alex@gmail.com"])
        
        
      # tests des rapporteurs (R) du modele maDUM pour l' attribut groups_data
    def test_get_groups_data(self):
    
        crud_obj = CRUD()
        crud_obj.groups_data = {"0": {"name": "default", "Trust": 50, "List_of_members": []}}

        crud_obj.groups_data = {"0": {"name": "default", "Trust": 50, "List_of_members": []}}
        name_group_2 = crud_obj.get_groups_data(2, "name")
        trust_group_2 = crud_obj.get_groups_data(2, "Trust")
        list_members_group_2 = crud_obj.get_groups_data(2, "List_of_members")
  
        
        self.assertEqual(name_group_2, False)
        self.assertEqual(trust_group_2, False)
        self.assertEqual(list_members_group_2, False)
    
    # tests des transformateurs (T) du modele maDUM pour l' attribut groups_data
        #d1
    def test_add_new_group_update_groups_remove_group_remove_group_member(self):
        crud_obj = CRUD()
        crud_obj.groups_data = {"0": {"name": "default", "Trust": 50, "List_of_members": []}}
        #ajout user dans user.json
        crud_obj.add_new_user("yanbra@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("datphi@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("someone@polymtl.ca","1998-07-09")
      

        crud_obj.add_new_group("Newgroup",50,["datphi@polymtl.ca"])
        self.assertEqual(crud_obj.get_groups_data(1, "name"), "Newgroup")

        crud_obj.update_groups(1, "name", "just_inf")
        self.assertEqual(crud_obj.get_groups_data(1, "name"),"just_inf")

        crud_obj.remove_group(1)
        self.assertEqual(crud_obj.get_groups_data(1, "name"), False)

        crud_obj.remove_group_member(1, "datphi@polymtl.ca")
        self.assertEqual(crud_obj.get_groups_data(1, "List_of_members"), False)
    
        #d2
    def test_update_groups_add_new_group_remove_group_remove_group_member(self):
        crud_obj = CRUD()
        crud_obj.groups_data = {"0": {"name": "default", "Trust": 50, "List_of_members": []}}
        #ajout user dans user.json
        crud_obj.add_new_user("yanbra@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("datphi@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("someone@polymtl.ca","1998-07-09")
      

        crud_obj.update_groups(1, "name", "just_inf")
        self.assertEqual(crud_obj.get_groups_data(1, "name"),False)
        
        crud_obj.add_new_group("Newgroup",50,["datphi@polymtl.ca"])
        self.assertEqual(crud_obj.get_groups_data(1, "name"), "Newgroup")

        crud_obj.remove_group(1)
        self.assertEqual(crud_obj.get_groups_data(1, "name"), False)

        crud_obj.remove_group_member(1, "datphi@polymtl.ca")
        self.assertEqual(crud_obj.get_groups_data(1, "List_of_members"), False)
        #d3

    def test_remove_group_add_new_group_update_group_remove_group_member(self):
        
        crud_obj = CRUD()
        crud_obj.groups_data.clear
        crud_obj.groups_data = {"0": {"name": "default", "Trust": 50, "List_of_members": []}}
        #ajout user dans user.json
        crud_obj.add_new_user("yanbra@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("datphi@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("someone@polymtl.ca","1998-07-09")
      
        crud_obj.remove_group(1)
        self.assertEqual(crud_obj.get_groups_data(1, "name"), False)
        
        crud_obj.add_new_group("Newgroup",50,["datphi@polymtl.ca"])
        self.assertEqual(crud_obj.get_groups_data(1, "name"), "Newgroup")
        
        crud_obj.update_groups(1, "name", "just_inf")
        self.assertEqual(crud_obj.get_groups_data(1, "name"),"just_inf")

        crud_obj.remove_group_member(1, "datphi@polymtl.ca")
        self.assertEqual(crud_obj.get_groups_data(1, "List_of_members"), [])
        
     #d4
    def test_add_new_group_remove_group_update_groups_remove_group_member(self):
        crud_obj = CRUD()
        crud_obj.groups_data.clear

        crud_obj.groups_data = {"0": {"name": "default", "Trust": 50, "List_of_members": []}}
        #ajout user dans user.json
        crud_obj.add_new_user("yanbra@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("datphi@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("someone@polymtl.ca","1998-07-09")
      
        crud_obj.add_new_group("Newgroup",50,["datphi@polymtl.ca"])
        self.assertEqual(crud_obj.get_groups_data(1, "name"), "Newgroup")
        
        crud_obj.remove_group(1)
        self.assertEqual(crud_obj.get_groups_data(1, "name"), False)
        
        crud_obj.update_groups(1, "name", "just_inf")
        self.assertEqual(crud_obj.get_groups_data(1, "name"),False)

        crud_obj.remove_group_member(1, "datphi@polymtl.ca")
        self.assertEqual(crud_obj.get_groups_data(1, "List_of_members"), False)
        
    #d5
    def test_update_groups_remove_group_add_new_group_remove_group_member(self):
        crud_obj = CRUD()
        
        crud_obj.groups_data = {"0": {"name": "default", "Trust": 50, "List_of_members": []}}
        #ajout user dans user.json
        crud_obj.add_new_user("yanbra@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("datphi@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("someone@polymtl.ca","1998-07-09")
        
        crud_obj.update_groups(1, "name", "just_inf")
        self.assertEqual(crud_obj.get_groups_data(1, "name"),False)
      
        crud_obj.remove_group(1)
        self.assertEqual(crud_obj.get_groups_data(1, "name"), False)
        
        crud_obj.add_new_group("Newgroup",50,["datphi@polymtl.ca"])
        self.assertEqual(crud_obj.get_groups_data(1, "name"), "Newgroup")

        crud_obj.remove_group_member(1, "datphi@polymtl.ca")
        self.assertEqual(crud_obj.get_groups_data(1, "List_of_members"), [])
        crud_obj.remove_group(1)
        
        
    #d6
    def test_remove_group_update_groups_add_new_group_remove_group_member(self):
        crud_obj = CRUD()
        
        crud_obj.groups_data = {"0": {"name": "default", "Trust": 50, "List_of_members": []}}
        #ajout user dans user.json
        crud_obj.add_new_user("yanbra@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("datphi@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("someone@polymtl.ca","1998-07-09")
        
        crud_obj.remove_group(1)
        self.assertEqual(crud_obj.get_groups_data(1, "name"), False)
        
        
        crud_obj.update_groups(1, "name", "just_inf")
        self.assertEqual(crud_obj.get_groups_data(1, "name"),False)
      
        crud_obj.add_new_group("Newgroup",50,["datphi@polymtl.ca"])
        self.assertEqual(crud_obj.get_groups_data(1, "name"), "Newgroup")

        crud_obj.remove_group_member(1, "datphi@polymtl.ca")
        self.assertEqual(crud_obj.get_groups_data(1, "List_of_members"), [])
        crud_obj.remove_group(1)
        
    #d7
    def test_remove_group_member_update_groups_add_new_group_remove_group(self):
        crud_obj = CRUD()
        
        crud_obj.groups_data = {"0": {"name": "default", "Trust": 50, "List_of_members": []}}
        #ajout user dans user.json
        crud_obj.add_new_user("yanbra@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("datphi@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("someone@polymtl.ca","1998-07-09")
        
        crud_obj.remove_group_member(1, "datphi@polymtl.ca")
        self.assertEqual(crud_obj.get_groups_data(1, "List_of_members"), False)
        
        crud_obj.update_groups(1, "name", "just_inf")
        self.assertEqual(crud_obj.get_groups_data(1, "name"),False)
        
        crud_obj.add_new_group("Newgroup",50,["datphi@polymtl.ca"])
        self.assertEqual(crud_obj.get_groups_data(1, "name"), "Newgroup")
        
        crud_obj.remove_group(1)
        self.assertEqual(crud_obj.get_groups_data(1, "name"), False)
        
        
    #d8
    def test_update_groups_remove_group_member_add_new_group_remove_group(self):
        crud_obj = CRUD()
        
        crud_obj.groups_data = {"0": {"name": "default", "Trust": 50, "List_of_members": []}}
        #ajout user dans user.json
        crud_obj.add_new_user("yanbra@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("datphi@polymtl.ca","1998-07-09")
        crud_obj.add_new_user("someone@polymtl.ca","1998-07-09")
        
        crud_obj.update_groups(1, "name", "just_inf")
        self.assertEqual(crud_obj.get_groups_data(1, "name"),False)
        
        crud_obj.remove_group_member(1, "datphi@polymtl.ca")
        self.assertEqual(crud_obj.get_groups_data(1, "List_of_members"), False)
        
        crud_obj.add_new_group("Newgroup",50,["datphi@polymtl.ca"])
        self.assertEqual(crud_obj.get_groups_data(1, "name"), "Newgroup")
        
        crud_obj.remove_group(1)
        self.assertEqual(crud_obj.get_groups_data(1, "name"), False)
        
    
        
    
    
    
    # tests des autres (O) du modele maDUM pour l' attribut groups_data
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_get_new_group_id(self,mock_read_users_file,mock_read_groups_file):
        mock_read_users_file = self.users_data
        mock_read_groups_file = self.groups_data
        crud_obj = CRUD()
        
        new_id = crud_obj.get_new_group_id()
        
        self.assertEqual(new_id, "1")