import re
from collections import Counter

file = open('access_log')
data = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', file.read())
file.close()
for ip in Counter(data).most_common(10):
    print(ip[0])
