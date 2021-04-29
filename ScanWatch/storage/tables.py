from typing import List, Optional


class Table:
    """
    This class represent a table in a database. All columns names are dynamic attributes
    @DynamicAttrs
    This class is used to describe the tables that will be used to in the database
    """

    def __init__(self, name: str, columns_names: List[str], columns_sql_types: List[str],
                 primary_key: Optional[str] = None, primary_key_sql_type: Optional[str] = None):
        """
        Initialise a Table instance

        :param name: name of the table
        :type name: str
        :param columns_names: names of the columns (except primary column)
        :type columns_names: List[str]
        :param columns_sql_types: sql types of the previous columns
        :type columns_sql_types: List[str]
        :param primary_key: name of the primary key (None, if no primary key is needed)
        :type primary_key: Optional[str]
        :param primary_key_sql_type: sql type of the primary key (None, if no primary key is needed)
        :type primary_key_sql_type: Optional[str]
        """
        self.name = name
        self.columns_names = columns_names
        self.columns_sql_types = columns_sql_types
        self.primary_key = primary_key
        self.primary_key_sql_type = primary_key_sql_type

        for column_name in self.columns_names:
            try:
                value = getattr(self, column_name)
                raise ValueError(f"the name {column_name} conflicts with an existing attribute of value {value}")
            except AttributeError:
                setattr(self, column_name, column_name)

        if self.primary_key is not None:
            setattr(self, self.primary_key, self.primary_key)