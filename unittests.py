import unittest
from itertools import tee
from unittest.mock import patch
import random
import main


class TestAccountantProgram(unittest.TestCase):

    def test_check_document_existence(self):
        test_value = random.choice(main.documents)['number']
        test_case = [{"expected_result": True, "value": test_value}, {"expected_result": False, "value": 'Ase435/*'}]
        for case in test_case:
            self.assertEqual(case["expected_result"], main.check_document_existence(case["value"]),
                             "Test case 'check document existence' has failed")

    @patch('builtins.input', side_effect=['2207 876234', '11-2', '5455 028765',
                                          'Not_number', str(random.randrange(1, 600))])
    def test_get_doc_owner_name(self, number):
        new_list, new_list1 = tee(number.side_effect)
        number.side_effect = new_list1
        for i in new_list:
            res = main.get_doc_owner_name()
            test_case = None
            for j in main.documents:
                if i == j['number']:
                    test_case = j['name']
            self.assertEqual(test_case, res)

    def test_get_all_doc_owners_names(self):
        test_case = []
        for i in main.documents:
            test_case.append(i['name'])
        test_case = set(test_case)
        self.assertEqual(test_case, main.get_all_doc_owners_names(),
                         "Test case 'get_all_doc_owners_names' has failed")

    def test_remove_doc_from_shelf(self):
        test_directories = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': ['55555']}
        for i in test_directories.values():
            for j in range(len(i)):
                test_case = i[j]
                main.remove_doc_from_shelf(test_case, test_directories)
                print(test_case)
                print(test_directories)
                self.assertNotIn(test_case, test_directories)
                i.insert(j, test_case)

    def test_add_new_shelf(self):
        test_directories = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': ['55555']}
        test_case1 = str(random.randrange(int(max(list(test_directories.keys()))), 10))
        self.assertEqual((test_case1, True), main.add_new_shelf(test_directories, test_case1),
                         "Test case 'add_new_shelf' has failed")
        main.add_new_shelf(test_directories, test_case1)
        self.assertIn(str(test_case1), list(test_directories.keys()), "Test case 'add_new_shelf' has failed")
        test_directories.pop(test_case1)
        test_case2 = str(random.choice(list(test_directories.keys())))
        self.assertEqual((test_case2, False), main.add_new_shelf(test_directories, test_case2),
                         "Test case 'add_new_shelf' has failed")

    def test_append_doc_to_shelf(self):
        lst = []
        for i in main.directories.values():
            lst += i
        test_doc = ''
        while test_doc in lst or test_doc == '':
            test_doc = '{}-{}-{}'.format(str(random.randrange(100, 999)),
                                         str(random.randrange(100, 999)), str(random.randrange(100, 999)))
        shelf = str(random.choice(list(main.directories.keys())))
        main.append_doc_to_shelf(test_doc, shelf)
        self.assertIn(test_doc, main.directories[shelf])
        main.directories[shelf].remove(test_doc)
