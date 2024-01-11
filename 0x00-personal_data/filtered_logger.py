#!/usr/bin/env python3
"""
Regex filter log messages for user data
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
    return f'{separator} '.join(re.split(separator, message)).strip()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """Initialize RedactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format a log message"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Get a logger object with default handlers for user data logging"""
    logger = logging.Logger('user_data', level=logging.INFO)
    # logger.propagate = False
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(streamHandler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Get a connector to a mysql db based on env variables"""
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
    """Main function to log all rows in the users table
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
    cur.close()
    db.close()


if __name__ == "__main__":
    main()
