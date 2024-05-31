#!/usr/bin/env python3
"""
A function that returns the log message obfuscated
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (list): List of strings representing all fields to obfuscate.
        redaction (str): String representing by what the field will be obfuscated.
        message (str): String representing the log line.
        separator (str): String representing by which character is separating all fields in the log line.

    Returns:
        str: The obfuscated log message.
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}", message)


if __name__ == '__main__':
    main()
