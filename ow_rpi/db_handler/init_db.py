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

import db_handler as db
import yaml

def get_config():
    with open("ow_rpi/config/db_config.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

if __name__ == '__main__':
    """
    db.init_measure('temperature', -273.15, 200)
    db.init_measure('pressure', 800, 1300)
    db.init_measure('luminosity', 0, 150000)
    db.init_measure('humidity', 0, 5000)
    db.init_measure('ultraviolet', 0, 5000)
    db.init_measure('infrared', 0, 5000)
    """
    config = get_config()
    measures = config['measures'].split(" ")
    for i in range(config['number_of_pi']):
        for m in measures:
            db.init_measure(i,m)
