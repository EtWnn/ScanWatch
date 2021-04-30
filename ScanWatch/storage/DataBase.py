from enum import Enum
from typing import List, Tuple, Optional, Any, Union
import sqlite3

from ScanWatch.storage.tables import Table
from ScanWatch.utils.LoggerGenerator import LoggerGenerator
from ScanWatch.utils.paths import get_data_path


class SQLConditionEnum(Enum):
    """
    Enumeration for SQL comparison operator

    https://www.techonthenet.com/sqlite/comparison_operators.php
    """
    equal = '='
    greater_equal = '>='
    greater = '>'
    lower = '<'
    lower_equal = '<='
    diff = '!='


class DataBase:
    """
    This class will be used to interact with sqlite3 databases without having to generates sqlite commands
    """

    def __init__(self, name: str):
        """
        Initialise a DataBase instance

        :param name: name of the database
        :type name: str
        """
        self.name = name
        self.logger = LoggerGenerator.get_logger(self.name)
        self.save_path = get_data_path() / f"{name}.db"
        self.db_conn = None
        self.db_cursor = None
        self.connect()

    def connect(self):
        """
        Connect to the sqlite3 database

        :return: None
        :rtype: None
        """
        self.db_conn = sqlite3.connect(self.save_path)
        self.db_cursor = self.db_conn.cursor()

    def close(self):
        """
        Close the connection with the sqlite3 database

        :return: None
        :rtype: None
        """
        self.db_conn.close()

    def _fetch_rows(self, execution_cmd: str) -> List[Tuple]:
        """
        Execute a command to fetch some rows and return them

        :param execution_cmd: the command to execute
        :type execution_cmd: str
        :return: list of the table's rows selected by the command
        :rtype: List[Tuple]
        """
        rows = []
        try:
            self.db_cursor.execute(execution_cmd)
        except sqlite3.OperationalError:
            return rows
        while True:
            row = self.db_cursor.fetchone()
            if row is None:
                break
            rows.append(row)
        return rows

    def get_row_by_key(self, table: Table, key_value) -> Optional[Tuple]:
        """
        Get the row identified by a primary key value from a table

        :param table: table to fetch the key from
        :type table: Table
        :param key_value: value of the primary key
        :type key_value: Any
        :return: the raw row of of the table
        :rtype: Optional[Tuple]
        """
        if table.primary_key is None:
            raise ValueError(f"table {table.name} has no explicit primary key")
        conditions_list = [(table.primary_key, SQLConditionEnum.equal, key_value)]
        rows = self.get_conditions_rows(table, conditions_list=conditions_list)
        if len(rows):
            return rows[0]

    def get_conditions_rows(self, table: Table,
                            selection: Union[str, List[str]] = '*',
                            conditions_list: Optional[List[Tuple[str, SQLConditionEnum, Any]]] = None,
                            order_list: Optional[List[str]] = None) -> List[Tuple]:
        """
        Select rows with optional conditions and optional order

        :param table: table to select the rows from
        :type table: Table
        :param selection: list of column or SQL type selection
        :type selection: Union[str, List[str]]
        :param conditions_list: list of conditions to select the row
        :type conditions_list: Optional[List[Tuple[str, SQLConditionEnum, Any]]]
        :param order_list: List of SQL type order by
        :type order_list: Optional[List[str]]
        :return: the selected rows
        :rtype: List[Tuple]
        """
        if isinstance(selection, List):
            selection = ','.join(selection)
        if conditions_list is None:
            conditions_list = []
        if order_list is None:
            order_list = []
        execution_cmd = f"SELECT {selection} from {table.name}"
        execution_cmd = self._add_conditions(execution_cmd, conditions_list=conditions_list)
        execution_cmd = self._add_order(execution_cmd, order_list=order_list)
        return self._fetch_rows(execution_cmd)

    def get_all_rows(self, table: Table) -> List[Tuple]:
        """
        Get all the rows of a table

        :param table: table to get the rows from
        :type table: Table
        :return: all the rows of the table
        :rtype: List[Tuple]
        """
        return self.get_conditions_rows(table)

    def add_row(self, table: Table, row: Tuple, auto_commit: bool = True, update_if_exists: bool = False):
        """
        Add a row to a table

        :param table: table to add a row to
        :type table: Table
        :param row: values to add to the database
        :type row: Tuple
        :param auto_commit: if the database state should be saved after the changes
        :type auto_commit:  bool
        :param update_if_exists: if an integrity error is raised and this parameter is true,
            will update the existing row
        :type update_if_exists: bool
        :return: None
        :rtype: None
        """
        row_s = ", ".join(f"'{v}'" for v in row)
        row_s = f'({row_s})'
        execution_order = f"INSERT INTO {table.name} VALUES {row_s}"
        try:
            self.db_cursor.execute(execution_order)
            if auto_commit:
                self.commit()
        except sqlite3.OperationalError:
            self.create_table(table)
            self.db_cursor.execute(execution_order)
            if auto_commit:
                self.commit()
        except sqlite3.IntegrityError as err:
            if update_if_exists:
                self.update_row(table, row, auto_commit)
            else:
                existing_row = self.get_row_by_key(table, row[0])
                msg = f"tried to insert {row} in the table {table.name} but the row is occupied: {existing_row}"
                self.logger.error(msg)
                raise err

    def add_rows(self, table: Table, rows: List[Tuple], auto_commit: bool = True, update_if_exists: bool = False):
        """
        Add several rows to a table

        :param table: table to add a row to
        :type table: Table
        :param rows: list of values to add to the database
        :type rows: List[Tuple]
        :param auto_commit: if the database state should be saved after the changes
        :type auto_commit:  bool
        :param update_if_exists: if an integrity error is raised and this parameter is true,
            will update the existing row
        :type update_if_exists: bool
        :return: None
        :rtype: None
        """
        for row in rows:
            self.add_row(table, row, auto_commit=False, update_if_exists=update_if_exists)
        if auto_commit:
            self.commit()

    def update_row(self, table: Table, row: Tuple, auto_commit=True):
        """
        Update the value of a row in a table

        :param table: table to get updated
        :type table: Table
        :param row: values to update
        :type row: Tuple
        :param auto_commit: if the database state should be saved after the changes
        :type auto_commit:  bool
        :return: None
        :rtype: None
        """
        row_s = ", ".join(f"{n} = {v}" for n, v in zip(table.columns_names, row))
        execution_order = f"UPDATE {table.name} SET {row_s} WHERE {table.primary_key} = {row[0]}"
        self.db_cursor.execute(execution_order)
        if auto_commit:
            self.commit()

    def create_table(self, table: Table):
        """
        Create a table in the database

        :param table: Table instance with the config of the table to create
        :type table: Table
        :return: None
        :rtype: None
        """
        create_cmd = self.get_create_cmd(table)
        self.db_cursor.execute(create_cmd)
        self.db_conn.commit()

    def drop_table(self, table: Union[Table, str]):
        """
        Delete a table from the database

        :param table: table or table name to drop
        :type table: Union[Table, str]
        :return: None
        :rtype: None
        """
        if isinstance(table, Table):
            table = table.name
        execution_order = f"DROP TABLE IF EXISTS {table}"
        self.db_cursor.execute(execution_order)
        self.db_conn.commit()

    def drop_all_tables(self):
        """
        Drop all the tables existing in the database

        :return: None
        :rtype: None
        """
        tables_desc = self.get_all_tables()
        for table_desc in tables_desc:
            self.drop_table(table_desc[1])
        self.commit()

    def get_all_tables(self) -> List[Tuple]:
        """
        Return all the tables existing in the database

        :return: tables descriptions
        :rtype: List[Tuple]
        """
        cmd = "SELECT * FROM sqlite_master WHERE type='table';"
        return self._fetch_rows(cmd)

    def commit(self):
        """
        Submit and save the database state

        :return: None
        :rtype: None
        """
        self.db_conn.commit()

    @staticmethod
    def _add_conditions(execution_cmd: str, conditions_list: List[Tuple[str, SQLConditionEnum, Any]]):
        """
        Add a list of condition to an SQL command

        :param execution_cmd: SQL command without 'WHERE' statement
        :type execution_cmd: str
        :param conditions_list: List of condition to add to the SQL command
        :type conditions_list: List[Tuple[str, SQLConditionEnum, Any]]
        :return: the augmented command
        :rtype: str
        """
        if len(conditions_list):
            add_cmd = ' WHERE'
            for column_name, condition, value in conditions_list:
                add_cmd = add_cmd + f" {column_name} {condition.value} '{value}' AND"
            return execution_cmd + add_cmd[:-4]
        else:
            return execution_cmd

    @staticmethod
    def _add_order(execution_cmd: str, order_list: List[str]):
        """
        Add an order specification to an SQL command

        :param execution_cmd: SQL command without 'ORDER BY' statement
        :type execution_cmd: str
        :param order_list: SQL order
        :type order_list: List[str]
        :return: the augmented command
        :rtype: str
        """
        if len(order_list):
            add_cmd = ' ORDER BY'
            for column_name in order_list:
                add_cmd = add_cmd + f" {column_name},"
            return execution_cmd + add_cmd[:-1] + ' ASC'
        else:
            return execution_cmd

    @staticmethod
    def get_create_cmd(table: Table) -> str:
        """
        Return the command in string format to create a table in the database

        :param table: Table instance with the config if the table to create
        :type table: Table
        :return: execution command for the table creation
        :rtype: str
        """
        cmd = ""
        if table.primary_key is not None:
            cmd = f"[{table.primary_key}] {table.primary_key_sql_type} PRIMARY KEY, "
        for arg_name, arg_type in zip(table.columns_names, table.columns_sql_types):
            cmd = cmd + f"[{arg_name}] {arg_type}, "
        return f"CREATE TABLE {table.name}\n({cmd[:-2]})"
