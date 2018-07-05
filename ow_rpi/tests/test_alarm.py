from ow_rpi.alarm.db_alarm import *

init_db()

generate_alarm(0,"temperature", 1530807202, 14)
generate_alarm(0,"temperature", 1530807202, 16)
generate_alarm(0,"temperature", 1530807202, 21)
generate_alarm(0,"temperature", 1530807202, 23)
mytest = [(1530807202, u'temperature', 14.0, 0, u'2'), (1530807202, u'temperature', 16.0, 0, u'1'), (1530807202, u'temperature', 21.0, 0, u'1'), (1530807202, u'temperature', 23.0, 0, u'2')]
values = get_log_all("temperature")
ok = True
for i in range(len(values)):
	for j in range(len(values[i])):
		if mytest[i][j] != values[i][j]:
			ok = False
			
print ok
