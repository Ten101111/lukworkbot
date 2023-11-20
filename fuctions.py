import datetime

import gspread

gc = gspread.service_account(filename='lukwork-55d4146f976b.json')
sh = gc.open('LukWork')
worksheet0 = sh.get_worksheet(0)
employees = worksheet0.col_values(2)
while '' in employees:
    employees.remove('')

employees = employees[1:]

import datetime as dt
from calendar import monthrange
long = monthrange(dt.datetime.now().year, dt.datetime.now().month)[1]

pt1 = worksheet0.row_values(3)[:4+long]
pt2 = worksheet0.row_values(3)[35:]
names = pt1+pt2
data = worksheet0.row_values(4)

first = dict(zip(names, data))
print(first)
sp = []

for i in range(len(employees)):
    part_1 = worksheet0.row_values(4+i*4)[:4+long]
    part_2 = worksheet0.row_values(4+i*4)[35:]
    a = dict(zip(names, part_1+part_2))
    sp.append(a)

night = []
for i in range(len(employees)):
    part_1 = worksheet0.row_values(5 + i * 4)[:4 + long]
    part_2 = worksheet0.row_values(5 + i * 4)[35:]
    b = dict(zip(names, part_1+part_2))
    night.append(b)


key = sp[0].keys()

nums = list(range(1,5))
nums_str = list(map(str,nums))

def chass(spisok):
    if str(spisok)[-1] == '1':
        return 'час'
    elif str(spisok)[-1] in nums_str:
        return 'часа'
    else:
        return 'часов'

def dnya(spisok):
    if spisok == 1 or spisok in [21,25] or spisok == 31:
        return 'день'
    elif spisok in [2,5]:
        return 'дня'
    else:
        return 'дней'

def closest(n, sp):
    return min(filter(lambda x: x > n, sp), default=None)

today = datetime.datetime.now().day