import csv
import logging
import names
import tempfile

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', filename='evaluation.log')

NUMBER_OF_CLIENT_FIELDS = 7
TEMP_CSV_FIELDNAMES = ['mac','first','last','power','packets','bssid','probed']

class AirodumpParser:

    def __init__(self, source_file):
        self.source_file = source_file
        self.csv_array = []
        self.dict_array = []
        self.temp_csv = tempfile.NamedTemporaryFile(mode='w+')

    def read_source_csv(self):
        with open(self.source_file) as source_csv:
            for row in source_csv:
                if len(row.split(',')) == NUMBER_OF_CLIENT_FIELDS:
                    self.csv_array.append(row)

    def write_temp_csv(self):
        with open(self.temp_csv.name, 'w+') as temp_csv_file:
            for line in self.csv_array:
                temp_csv_file.write(line)

    def create_csv_dictionaries(self):
        self.read_source_csv()
        self.write_temp_csv()
        with open(self.temp_csv.name) as csvfile:
            csv_dictionary = csv.DictReader(csvfile, fieldnames=TEMP_CSV_FIELDNAMES)
            for row in csv_dictionary:
                self.dict_array.append(row)
        logging.debug("Discovered %s clients." % (len(self.dict_array)))
        return self.dict_array
