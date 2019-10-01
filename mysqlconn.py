#!/usr/bin/env python3

import mysql.connector
from mysql.connector import errorcode


class DatabaseConnector:
    def __init__(self, username, password, database, host, port=3306):
        self.db_config = {
            'user': username,
            'password': password,
            'database': database,
            'host': host,
            'port': port,
            'raise_on_warnings': True
        }
        self.db_conn = None
        self.db_cursor = None
        self.db_name = 'foxearth'
        self.db_table_name = 'devices'
        self.__connect_to_server()

    def __check_dbname(self):
        if self.db_config['database'] == self.db_name:
            return True
        else:
            print('[Error: please set correct database name <foxearth>]')
            return False

    def __create_db(self):
        try:
            self.db_cursor.execute("CREATE DATABASE IF NOT EXISTS foxearth")
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        else:
            print('[Info: create database OK.]')

    def __create_table(self):
        try:
            self.db_cursor.execute("CREATE TABLE IF NOT EXISTS foxearth.devices (device_type VARCHAR(20), "
                                   "device_name VARCHAR(20), mac_address VARCHAR(12), ip_address VARCHAR(15), "
                                   "network_mask VARCHAR(15), UNIQUE(device_name, mac_address))")
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        else:
            print('[Info: create table OK.]')

    def __show_databases(self):
        self.db_cursor.execute("SHOW DATABASES")
        for x in self.db_cursor:
            print(x)

    def add_device(self, device_type, device_name, mac_address, ip_address, network_mask):
        db_table_name = self.db_name + '.' + self.db_table_name
        sql = "INSERT INTO {}(device_type, device_name, mac_address, ip_address, network_mask) " \
              "VALUES(%s, %s, %s, %s, %s)".format(db_table_name)
        arg = (device_type, device_name, mac_address, ip_address, network_mask)
        try:
            self.db_cursor.execute(sql, arg)
            self.db_conn.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

    def __connect_to_server(self):
        if self.__check_dbname():
            try:
                self.db_conn = mysql.connector.connect(**self.db_config)
                self.db_cursor = self.db_conn.cursor()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("[Database error: wrong user name or password!]")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("[Database error: database does not exist!]")
                    self.db_config['database'] = ''
                    self.db_conn = mysql.connector.connect(**self.db_config)
                    self.db_cursor = self.db_conn.cursor()
                    self.__create_db()
                    print("[Database error: table does not exist!]")
                    self.__create_table()
                else:
                    print(err)


# Class usage;
#   db = DatabaseConnector(username, password, database_name, hostname, port=3306)

'''
db = DatabaseConnector('root', 'pleomax', 'foxearth', '127.0.0.1')
db.add_device('boiler', 'boiler in kitchen', 'ac220bc8666d', '192.168.1.133', '255.255.255.0')
db.add_device('dlink-ip-camera', 'camera in garage', 'ea157bc5318a', '192.168.1.221', '255.255.0.0')
'''
