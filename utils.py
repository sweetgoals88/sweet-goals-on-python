from control_variables import KEY_FILE_LOCATION
import string
import datetime as dt

def dates_differ(first: dt.datetime | None, second: dt.datetime | None):
    '''
    Checks if two dates are different, without taking seconds into
    account. For example, 8:11:53 is considered the same as 8:11:01
    '''
    if first is None: return second is not None
    if second is None: return True

    if first.year != second.year: return True
    if first.month != second.month: return True
    if first.day != second.day: return True
    if first.hour != second.hour: return True
    if first.minute != second.minute: return True

    return False

def get_device_key():
    with open(KEY_FILE_LOCATION, "r") as key_file:
        key = key_file.readline()
        if len(key) != 128:
            raise Exception("The key is not 128 characters long; it was corrupted")
        if any(character not in string.hexdigits for character in key):
            raise Exception("The key is not a hexadecimal string; it was corrupted")
        return key
