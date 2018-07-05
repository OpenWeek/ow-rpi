import datetime
import time

datetimeformat = "%Y-%m-%d %H:%M:%S"

def timestamp_to_date(now):
    """Fonction qui transforme une date de format <timestamp POSIX> en format <datetimeformat> (declare a la ligne 4).

    Args:
        now: une date sous format <timestamp POSIX>.

    Return:
        Retourne la date sous le format <datetimeformat>.

    """
    return datetime.datetime.fromtimestamp(int(now)).strftime(datetimeformat)
    
def date_to_timestamp(date, format = datetimeformat):
    """Fonction qui transforme une date de format <format> en format <timestamp POSIX>.

    Args:
        date: une date sous format <format>.
        format: le format de la date, par defaut le format <datetimeformat> (declare a la ligne 4).

    Return:
        Retourne la date sous le format <timestamp POSIX>.

    """
    return int(time.mktime(datetime.datetime.strptime(date, datetimeformat).timetuple()))

def timestamp_to_isoformat(now):
    """Fonction qui transforme une date de format <timestamp POSIX> en format <ISO 8601>.

    Args:
        date: une date sous format <timestamp POSIX>.

    Return:
        Retourne la date sous le format <ISO 8601>.

    """
    return datetime.datetime.fromtimestamp(int(now)).isoformat()
    
def isoformat_to_timestamp(date):
    """Fonction qui transforme une date de format <ISO 8601> en format <timestamp POSIX>.

    Args:
        date: une date sous format <ISO 8601>.

    Return:
        Retourne la date sous le format <timestamp POSIX>.

    """
    return int(time.mktime(datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').timetuple()))

