import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(process)d - %(levelname)s - %(message)s')

class DatabaseHandler:
    def __init__(self, db_file_location):
        self.conn = sqlite3.connect(db_file_location)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        create_command = 'CREATE TABLE IF NOT EXISTS whoiswalkingby ('\
                         'mac_address text, '\
                         'easy_name text, '\
                         'first_seen datetime, '\
                         'last_seen datetime, '\
                         'power int, '\
                         'number_packets int, '\
                         'bssid_mac text, '\
                         'probed_essids text, '\
                         'last_ten text)'
        self.cursor.execute(create_command)

    def insert_new_item(self, item):
            insert_command = 'INSERT INTO whoiswalkingby VALUES'\
                             '("%s", "%s", "%s", "%s", "%s", "%s",'\
                             '"%s", "%s", "%s")' % (item["mac"],
                                                    item["easy_name"],
                                                    item["first"],
                                                    item["last"],
                                                    item["power"],
                                                    item["packets"],
                                                    item["bssid"],
                                                    item["probed"],
                                                    item["last"])
            self.run_sql(insert_command)

    def lookup_mac(self, mac_address):
        select_command = 'SELECT * FROM whoiswalkingby WHERE mac_address = "%s"' % (mac_address)
        return self.cursor.execute(select_command).fetchone()

    def run_sql(self, command):
        logging.debug(command)
        self.cursor.execute(command)
        self.conn.commit()

    def update_item(self, response, item):
        update_command = 'UPDATE whoiswalkingby SET '\
                  'last_seen = "%s",'\
                  'power = "%s",'\
                  'number_packets = "%s",'\
                  'probed_essids = "%s",'\
                  'last_ten = "%s"'\
                  'WHERE mac_address = "%s"'\
                  % (item['last'],
                     item['power'],
                     item['packets'],
                     item['probed'],
                     item['last_ten'],
                     item['mac'])
        self.run_sql(update_command)


