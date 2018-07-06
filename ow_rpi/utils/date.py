# Openweek Raspberry pi's weather station
# Copyright c 2018  Maxime Postaire, Lucas Ody, Maxime Franco,
# Nicolas Rybowski, Benjamin De Cnuydt, Quentin Delmelle, Colin Evrard,
# Antoine Vanderschueren.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
    return int(time.mktime(datetime.datetime.strptime(date, format).timetuple()))

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

