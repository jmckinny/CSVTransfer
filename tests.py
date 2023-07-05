import configparser
import unittest
import main
import sys


class MyTestCase(unittest.TestCase):
    def test_valid_file_names(self):
        names1: list[str] = ["example_files/example.csv", "example_files/example2.csv"]
        names2: list[str] = ["example_files/example2.csv", "example_files/example3.csv"]
        names3: list[str] = ["example_files/example.csv", "example_files/example.csv"]

        self.assertTrue(main.valid_file_names(names1))
        self.assertTrue(main.valid_file_names(names2))
        self.assertTrue(main.valid_file_names(names3))

    def test_invalid_file_names(self):
        names1: list[str] = ["does_not_exist.file", "example_files/example.csv"]
        names2: list[str] = ["example_files/example2.csv", "venv"]

        self.assertFalse(main.valid_file_names(names1))
        self.assertFalse(main.valid_file_names(names2))

    def test_parse_csv(self):
        parsed_csv: list[main.Row] = main.parse_csv("example_files/example.csv", 0, [])
        expected_parsed_csv: list[main.Row] = [
            {"Name": "John Smith", "Date of birth": "3/24/1989", "Social Security Number": "123456",
             "Employment Status": "Employed", "Favorite Color": "Red"},
            {"Name": "Joe Bob", "Date of birth": "1/23/4567", "Social Security Number": "987654321",
             "Employment Status": "Unemployed", "Favorite Color": "Orange"},
            {"Name": "Emily Wayne", "Date of birth": "5/31/2000", "Social Security Number": "1234321",
             "Employment Status": "Unknown", "Favorite Color": "Yellow"},
            {"Name": "First Last", "Date of birth": "1/1/1970", "Social Security Number": "234111",
             "Employment Status": "Unknown", "Favorite Color": "Green"}
        ]

        self.assertEqual(expected_parsed_csv, parsed_csv)

    def test_parse_csv2(self):
        parsed_csv: list[main.Row] = main.parse_csv("example_files/example2.csv", 0, [])
        expected_parsed_csv: list[main.Row] = [
            {"name": "First Last", "ssn": "234111", "fav color": "", "state of residence": "Ohio"},
            {"name": "", "ssn": "987654321", "fav color": "Orange", "state of residence": "Texas"},
            {"name": "John Smith", "ssn": "123456", "fav color": "", "state of residence": "Michigan"},
            {"name": "", "ssn": "1234321", "fav color": "", "state of residence": ""}
        ]

        self.assertEqual(expected_parsed_csv, parsed_csv)

    def test_parse_csv3(self):
        parsed_csv: list[main.Row] = main.parse_csv("example_files/example3.csv", 1, [0, 6, 5])
        expected_parsed_csv: list[main.Row] = [
            {"social security": "", "d.o.b": "", "last name, first name": "Bob, Joe", "employment status": "employed",
             "favorite color": "Teal", "hobbies": "Tennis", "comments": ""},
            {"social security": "1234321", "d.o.b": "5/31/2000", "last name, first name": "Wayne, Emily",
             "employment status": "", "favorite color": "Red", "hobbies": "", "comments": "No comment"},
            {"social security": "234111", "d.o.b": "1/1/1970", "last name, first name": "Last, First",
             "employment status": "employed", "favorite color": "Magenta", "hobbies": "Deliberate misinformation",
             "comments": "Mr. Unix Epoch"}
        ]

        self.assertEqual(expected_parsed_csv, parsed_csv)

    def test_parse_csv4(self):
        parsed_csv: list[main.Row] = main.parse_csv("example_files/example3.csv", 1, [0, 2, 5])
        expected_parsed_csv: list[main.Row] = [
            {"social security": "1234321", "d.o.b": "5/31/2000", "last name, first name": "Wayne, Emily",
             "employment status": "", "favorite color": "Red", "hobbies": "", "comments": "No comment"},
            {"social security": "234111", "d.o.b": "1/1/1970", "last name, first name": "Last, First",
             "employment status": "employed", "favorite color": "Magenta", "hobbies": "Deliberate misinformation",
             "comments": "Mr. Unix Epoch"},
            {"social security": "565", "d.o.b": "", "last name, first name": "", "employment status": "employed",
             "favorite color": "Royal purple", "hobbies": "No hobby", "comments": ""}
        ]

        self.assertEqual(expected_parsed_csv, parsed_csv)

    def test_get_constants_from_file(self):
        main.CONFIG_FILE_NAME = "example_files/config_example.ini"
        config: configparser.ConfigParser = main.get_config_constants()
        expected_constants: dict = {
            "defaults": {
                "header_row_num": "0",
                "ignored_row(s)": "-1"
            },
            "sources": {
                "source1": "example_files/example.csv",
                "source3": "example_files/example3.csv",
            },
            "source1": {
                "target_column(s)": "Favorite Color",
                "column_name(s)": "favorite color",
                "match_by": "Social Security Number",
                "match_by_name(s)": "social security",
                "header_row_num": "0",
                "ignored_row(s)": "-1"
            },
            "source3": {
                "target_column(s)": "favorite color",
                "column_name(s)": "",
                "match_by": "social security",
                "match_by_name(s)": "",
                "header_row_num": "1",
                "ignored_row(s)": "0,5"
            },
            "output": {
                "file_name": "output.csv",
                "unmatched_file_name": "",
                "dialect": "excel"
            },
            "source_rules": {},
            "field_rules": {}
        }

        self.assertConfigEquals(expected_constants, config)

    def test_get_constants_from_nonexistent_file(self):
        main.CONFIG_FILE_NAME = "does_not_exist_for_test_to_work.ini"
        with self.assertRaises(SystemExit):
            main.get_config_constants()

    def test_get_constants_missing_constants(self):  # Give same inputs for the function call and the test inputs
        main.CONFIG_FILE_NAME = "example_files/empty_config.ini"

        with self.assertRaises(SystemExit):
            main.get_config_constants()

    def test_get_constants_missing_constants2(self):
        main.CONFIG_FILE_NAME = "example_files/empty_config2.ini"

        with self.assertRaises(SystemExit):
            main.get_config_constants()

    def test_get_constants_missing_constants3(self):
        main.CONFIG_FILE_NAME = "example_files/empty_config3.ini"

        with self.assertRaises(SystemExit):
            main.get_config_constants()

    def test_write_to_csv(self):
        sample_data: list[main.Row] = [
            {"Name": "John Deer", "Occupation": "Landscaping"},
            {"Name": "Test", "Occupation": "None"},
            {"Name": "Batman", "Occupation": "Hero"}
        ]
        main.write_csv("test_outputs/test_output.csv", sample_data, dialect="excel")

        with open("test_outputs/test_output.csv") as f:
            lines = f.readlines()

        expected_lines = [
            "Name,Occupation\n",
            "John Deer,Landscaping\n",
            "Test,None\n",
            "Batman,Hero\n"
        ]

        self.assertEqual(expected_lines, lines)

    def test_transfer_data(self):
        source: list[main.Row] = [
            {"x": "1", "x^2": "1", "x^3": "1"},
            {"x": "2", "x^2": "4", "x^3": "8"},
            {"x": "3", "x^2": "9", "x^3": "27"},
            {"x": "4", "x^2": "16", "x^3": "64"},
            {"x": "5", "x^2": "25", "x^3": "125"}
        ]
        target: list[main.Row] = [
            {"t": "1", "func1": "2", "func2": "4"},
            {"t": "2", "func1": "4", "func2": ""},
            {"t": "3", "func1": "6", "func2": "88"},
            {"t": "4", "func1": "8", "func2": ""},
            {"t": "5", "func1": "10", "func2": "3"},
            {"t": "6", "func1": "13", "func2": ""},
            {"t": "7", "func1": "19", "func2": "2"}
        ]
        target_columns: dict[str: str] = {"x^2": "func2"}
        source_match_by: str = "x"
        target_match_by: str = "t"

        main.transfer_data(source, target, target_columns, source_match_by, target_match_by)

        expected_target = [
            {"t": "1", "func1": "2", "func2": "1"},
            {"t": "2", "func1": "4", "func2": "4"},
            {"t": "3", "func1": "6", "func2": "9"},
            {"t": "4", "func1": "8", "func2": "16"},
            {"t": "5", "func1": "10", "func2": "25"},
            {"t": "6", "func1": "13", "func2": ""},
            {"t": "7", "func1": "19", "func2": "2"}
        ]

        self.assertEqual(expected_target, target)

    def test_transfer_data2(self):
        source: list[main.Row] = [
            {"Song": "Power Slam", "Rating": "8/10"},
            {"Song": "Mirror of the World", "Rating": "9/10"},
            {"Song": "Freesia", "Rating": "10/10"},
            {"Song": "Nobody", "Rating": "10/10"},
            {"Song": "HEAVY DAY", "Rating": "11/10"}
        ]
        target: list[main.Row] = [
            {"song": "Alone Infection", "rating": "9/10"},
            {"song": "Requiem", "rating": "10/10"},
            {"song": "HEAVY DAY", "rating": "9/10"},
            {"song": "505", "rating": "10/10"}
        ]
        target_columns: dict[str: str] = {"Rating": "rating"}
        source_match_by: str = "Song"
        target_match_by: str = "song"
        unmatched_out_name: str = "test_outputs/unmatched_transfer2.csv"

        main.transfer_data(source, target, target_columns, source_match_by, target_match_by,
                           unmatched_output=unmatched_out_name, dialect="excel")

        with open(unmatched_out_name) as f:
            unmatched_lines: list[str] = f.readlines()

        expected_target = [
            {"song": "Alone Infection", "rating": "9/10"},
            {"song": "Requiem", "rating": "10/10"},
            {"song": "HEAVY DAY", "rating": "11/10"},
            {"song": "505", "rating": "10/10"}
        ]

        expected_unmatched_lines: list[str] = [
            "Rating,Song\n",
            "8/10,Power Slam\n",
            "9/10,Mirror of the World\n",
            "10/10,Freesia\n",
            "10/10,Nobody\n"
        ]

        self.assertEqual(expected_target, target)
        self.assertEqual(expected_unmatched_lines, unmatched_lines)

    def test_transfer_data3(self):
        source: list[dict] = [
            {"File Name": "abc.def", "File Format": "def", "File Size": "300kB", "Marked For Deletion": "True"},
            {"File Name": "important_data.csv", "File Format": "csv", "File Size": "20MB",
             "Marked For Deletion": "False"},
            {"File Name": "funny.jpg", "File Format": "jpg", "File Size": "40MB", "Marked For Deletion": "False"},
            {"File Name": "info.txt", "File Format": "txt", "File Size": "10kB", "Marked For Deletion": "False"},
            {"File Name": "music.mp3", "File Format": "mp3", "File Size": "400MB", "Marked For Deletion": "False"}
        ]
        target: list[dict] = [
            {"Name": "proj.c", "Size": "89B", "Owner": "npp", "Last Changed": "5/30/23", "Delete?": "n"},
            {"Name": "funny.jpg", "Size": "500TB", "Owner": "me", "Last Changed": "1/20/23", "Delete?": ""},
            {"Name": "music.mp3", "Size": "0B", "Owner": "you", "Last Changed": "3/2/03", "Delete?": ""},
            {"Name": "important_data.csv", "Size": "40GB", "Owner": "root", "Last Changed": "2/2/20", "Delete?": ""},
            {"Name": "new_file", "Size": "1B", "Owner": "Simon Cowell", "Last Changed": "6/1/23", "Delete?": ""}
        ]
        target_columns: dict[str: str] = {"File Size": "Size", "Marked For Deletion": "Delete?"}
        source_match_by: str = "File Name"
        target_match_by: str = "Name"
        unmatched_out_name = "test_outputs/unmatched_transfer3.csv"

        main.transfer_data(source, target, target_columns, source_match_by, target_match_by, unmatched_out_name)

        with open(unmatched_out_name) as f:
            unmatched_lines: list[str] = f.readlines()

        expected_target: list[dict] = [
            {"Name": "proj.c", "Size": "89B", "Owner": "npp", "Last Changed": "5/30/23", "Delete?": "n"},
            {"Name": "funny.jpg", "Size": "40MB", "Owner": "me", "Last Changed": "1/20/23", "Delete?": "False"},
            {"Name": "music.mp3", "Size": "400MB", "Owner": "you", "Last Changed": "3/2/03", "Delete?": "False"},
            {"Name": "important_data.csv", "Size": "20MB", "Owner": "root", "Last Changed": "2/2/20",
             "Delete?": "False"},
            {"Name": "new_file", "Size": "1B", "Owner": "Simon Cowell", "Last Changed": "6/1/23", "Delete?": ""}
        ]
        expected_unmatched_lines: list[str] = [
            "File Size,Marked For Deletion,File Name\n",
            "300kB,True,abc.def\n",
            "10kB,False,info.txt\n"
        ]

        self.assertEqual(expected_target, target)
        self.assertEqual(expected_unmatched_lines, unmatched_lines)

    def test_everything_together(self):
        main.CONFIG_FILE_NAME = "example_files/config_example.ini"
        config: configparser.ConfigParser = main.get_config_constants()
        parsed_source: list[main.Row] = main.parse_csv(config["source"]["file_name"],
                                                       config.getint("source", "header_row_num"),
                                                       main.parse_ignored_rows(config["source"]["ignored_rows"]))
        parsed_target: list[main.Row] = main.parse_csv(config["target"]["file_name"],
                                                       config.getint("target", "header_row_num"),
                                                       main.parse_ignored_rows(config["target"]["ignored_rows"]))
        main.transfer_data(parsed_source, parsed_target, main.parse_target_columns(config),
                           config["source"]["match_by"], config["target"]["match_by"])
        main.write_csv(f'test_outputs/{config["output"]["file_name"]}', parsed_target,
                       config["output"]["dialect"])

        with open(f'test_outputs/{config["output"]["file_name"]}') as f:
            lines = f.readlines()

        expected_constants = {
            "defaults": {
                "header_row_num": "0",
                "ignored_rows": "-1"
            },
            "source": {
                "file_name": "example_files/example.csv",
                "target_column(s)": "Favorite Color",
                "match_by": "Social Security Number",
                "header_row_num": "0",
                "ignored_rows": "-1"
            },
            "target": {
                "file_name": "example_files/example3.csv",
                "target_column(s)": "favorite color",
                "match_by": "social security",
                "header_row_num": "1",
                "ignored_rows": "0,5"
            },
            "output": {
                "file_name": "output.csv",
                "unmatched_file_name": "",
                "dialect": "excel"
            },
            "field_rules": {}
        }

        expected_lines = [
            "social security,d.o.b,\"last name, first name\",employment status,favorite color,hobbies,comments\n",
            ",,\"Bob, Joe\",employed,Teal,Tennis,\n",
            "1234321,5/31/2000,\"Wayne, Emily\",,Yellow,,No comment\n",
            "234111,1/1/1970,\"Last, First\",employed,Green,Deliberate misinformation,Mr. Unix Epoch\n",
            "565,,,employed,Royal purple,No hobby,\n"
        ]

        self.assertEqual(expected_lines, lines)
        self.assertConfigEquals(expected_constants, config)

    def test_everything_together2(self):
        main.CONFIG_FILE_NAME = "example_files/config_example2.ini"
        config: configparser.ConfigParser = main.get_config_constants()
        parsed_source: list[main.Row] = main.parse_csv(config["source"]["file_name"],
                                                       config.getint("source", "header_row_num"),
                                                       main.parse_ignored_rows(config["source"]["ignored_rows"]))
        parsed_target: list[main.Row] = main.parse_csv(config["target"]["file_name"],
                                                       config.getint("target", "header_row_num"),
                                                       main.parse_ignored_rows(config["target"]["ignored_rows"]))
        main.transfer_data(parsed_source, parsed_target, main.parse_target_columns(config),
                           config["source"]["match_by"], config["target"]["match_by"],
                           f'test_outputs/{config["output"]["unmatched_file_name"]}', config["output"]["dialect"],
                           config["field_rules"])
        main.write_csv(f'test_outputs/{config["output"]["file_name"]}', parsed_target,
                       config["output"]["dialect"])

        with open(f'test_outputs/{config["output"]["file_name"]}') as f:
            lines = f.readlines()

        with open(f'test_outputs/{config["output"]["unmatched_file_name"]}') as f:
            unmatched_lines = f.readlines()

        expected_constants = {
            "defaults": {
                "header_row_num": "0",
                "ignored_rows": "-1"
            },
            "source": {
                "file_name": "example_files/example3.csv",
                "target_column(s)": "employment status,favorite color",
                "match_by": "social security",
                "header_row_num": "1",
                "ignored_rows": "0,6,5"
            },
            "target": {
                "file_name": "example_files/example.csv",
                "target_column(s)": "Employment Status,Favorite Color",
                "match_by": "Social Security Number",
                "header_row_num": "0",
                "ignored_rows": "-1"
            },
            "output": {
                "file_name": "output2.csv",
                "unmatched_file_name": "unmatched2.csv",
                "dialect": "unix"
            },
            "field_rules": {
                "employment status": r"^(([eE]|[uU]ne)mployed)$",
                "social security": r"^\d+$"
            }
        }

        expected_lines = [
            '"Name","Date of birth","Social Security Number","Employment Status","Favorite Color"\n',
            '"John Smith","3/24/1989","123456","Employed","Red"\n',
            '"Joe Bob","1/23/4567","987654321","Unemployed","Orange"\n',
            '"Emily Wayne","5/31/2000","1234321","Unknown","Yellow"\n',
            '"First Last","1/1/1970","234111","employed","Magenta"\n'
        ]

        expected_unmatched_lines = [
            '"employment status","favorite color","social security"\n',
            '"employed","Teal",""\n',
            '"","Red","1234321"\n',
        ]

        self.assertEqual(expected_lines, lines)
        self.assertEqual(expected_unmatched_lines, unmatched_lines)
        self.assertConfigEquals(expected_constants, config)

    def assertConfigEquals(self, expected_config: dict[str: dict[str: str]], config: configparser.ConfigParser):
        self.assertEqual(len(expected_config.keys()), len(config.sections()))

        for section in expected_config.keys():
            self.assertEqual(len(expected_config[section].keys()), len(config[section].keys()))
            for key in expected_config[section].keys():
                self.assertEqual(expected_config[section][key], config[section][key])


if __name__ == '__main__':
    unittest.main()
