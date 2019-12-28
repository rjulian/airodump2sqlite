import logging
import names

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(process)d - %(levelname)s - %(message)s')

class AirodumpDataHandler:

    def __init__(self, dictionary_array, database_handler):
        self.dictionary_array = dictionary_array
        self.database_handler = database_handler

    def needs_updating(self, response, current):
        if response[3] != current["last"]:
            return True

    def update_data(self):
        for line in self.dictionary_array:
            cleaned_line = AirodumpDataHandler.strip_whitespace(line)
            mac_data = self.database_handler.lookup_mac(cleaned_line['mac'])
            if mac_data:
                if self.needs_updating(mac_data, cleaned_line):
                    cleaned_line['last_ten'] = AirodumpDataHandler.create_last_ten(cleaned_line['last'], mac_data[8])
                    self.database_handler.update_item(mac_data, cleaned_line)
                else:
                    logging.debug('No update needed for %s' % (cleaned_line['mac']))
            else:
                cleaned_line['easy_name'] = '_'.join(names.get_full_name().split(' ')).lower()
                self.database_handler.insert_new_item(cleaned_line)

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


