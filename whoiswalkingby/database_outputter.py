import csv
import sqlite3
import logging
import names

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', filename='evaluation.log')

NUMBER_OF_CLIENT_FIELDS = 7
TEMP_CSV_FIELDNAMES = ['mac','first','last','power','packets','bssid','probed']

class DatabaseOutputter:
    def __init__(self, dictionary_array, db_file_location):
        self.conn = sqlite3.connect(db_file_location)
        self.cursor = self.conn.cursor()
        self.dictionary_array = dictionary_array

    def create_table(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS whoiswalkingby (mac_address text, easy_name text, first_seen datetime, last_seen datetime, power int, number_packets int, bssid_mac text, probed_essids text, last_ten text)')

    def update_table(self):
        self.create_table()
        for line in self.dictionary_array:
            cleaned_line = DatabaseOutputter.strip_whitespace(line)
            command = 'SELECT * FROM whoiswalkingby WHERE mac_address = "%s"' % (cleaned_line["mac"])
            select_response = self.cursor.execute(command).fetchone()
            if select_response:
                if self.needs_updating(select_response, cleaned_line):
                    self.update_item(select_response, cleaned_line)
                else:
                    logging.debug('No update needed for %s' % (cleaned_line['mac']))
            else:
                self.insert_new_item(cleaned_line)
        self.conn.commit()

    def update_item(self, response, current):
        new_last_ten = DatabaseOutputter.create_last_ten(current['last'], response[7])
        command = 'UPDATE whoiswalkingby SET '\
                  'last_seen = "%s",'\
                  'power = "%s",'\
                  'number_packets = "%s",'\
                  'probed_essids = "%s",'\
                  'last_ten = "%s"'\
                  'WHERE mac_address = "%s"'\
                  % (current['last'],
                     current['power'],
                     current['packets'],
                     current['probed'],
                     new_last_ten,
                     current['mac'])
        logging.debug(command)
        self.cursor.execute(command)

    @staticmethod
    def create_last_ten(last, last_ten):
        last_ten_array = last_ten.split(',')
        if len(last_ten_array) == 10:
            last_ten_array.pop()
        last_ten_array.insert(0,last)
        return ','.join(last_ten_array)

    @staticmethod
    def strip_whitespace(dictionary):
        keys = dictionary.keys()
        clean_dictionary = {}
        for key in keys:
            clean_dictionary[key] = dictionary[key].lstrip()
        return clean_dictionary

    def needs_updating(self, response, current):
        if response[2] != current["last"]:
            return True

    def insert_new_item(self, item):
            new_name = '_'.join(names.get_full_name().split(' ')).lower()
            insert_command = 'INSERT INTO whoiswalkingby VALUES'\
                             '("%s", "%s", "%s", "%s", "%s", "%s",'\
                             '"%s", "%s", "%s")' % (item["mac"],
                                                    new_name,
                                                    item["first"],
                                                    item["last"],
                                                    item["power"],
                                                    item["packets"],
                                                    item["bssid"],
                                                    item["probed"],
                                                    item["last"])
            logging.debug(insert_command)
            self.cursor.execute(insert_command)

