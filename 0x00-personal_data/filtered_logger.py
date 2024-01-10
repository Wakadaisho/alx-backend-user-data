#!/usr/bin/env python3
"""
Regex filter log messages
"""

import re
import logging
import mysql.connector
from os import getenv
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')
FIELDS = ('name', 'email', 'phone', 'ssn', 'password',
          'ip', 'last_login', 'user_agent')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """Redact sensitive fields from a message"""
    for field in fields:
        message = re.sub(f"(?<={field})=.+?{separator}",
                         f"={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return logging.Formatter(self.FORMAT).format(record)


def get_logger() -> logging.Logger:
    """Redact sensitive fields from a message"""
    logger = logging.Logger('user_data', level=logging.INFO)
    # logger.propagate = False
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(streamHandler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Get a connector to a mysql db"""
    user = getenv("PERSONAL_DATA_DB_USERNAME")
    password = getenv("PERSONAL_DATA_DB_PASSWORD")
    host = getenv("PERSONAL_DATA_DB_HOST")
    database = getenv("PERSONAL_DATA_DB_NAME")
    cnx = mysql.connector.connect(user=user,
                                  password=password,
                                  host=host,
                                  database=database)
    return cnx


def main() -> None:
    """Main function
    """
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users")
    results = cur.fetchall()
    logger = get_logger()
    for row in results:
        message = ''.join([f"{FIELDS[i]}={row[i]};"
                           for i in range(len(row))])
        logger.info(message)


if __name__ == "__main__":
    main()
