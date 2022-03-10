from os import rename

day_of_month=[31,28,31,30,31,30,31,31,30,31,30,31]
day_of_month_leap=[31,29,31,30,31,30,31,31,30,31,30,31]
days=365
count=0

for i in range(1901,2001):
    if((i%4==0 and i%100!=0) or i%400==0):
        print(i,"是闰年")
        for j in day_of_month_leap:
            days+=j
            if(days%7==6):
                count+=1
    else:
        print(i,"不是闰年")
        for j in day_of_month:
            days+=j
            if(days%7==6):
                count+=1
print(days)
print(count)

rename('2.py','2.py')