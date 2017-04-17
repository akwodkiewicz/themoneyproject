import os, sys, datetime
import csv

groceries_keywords = ['ZABKA', 'LIDL', 'CARREFOUR', 'BIEDRONKA', 'SKLEP']
coffee_keywords = ['COFFEE', 'CAFE', 'COSTA', 'STARBUCKS', 'AMREST',
 'GREEN', 'NERO', 'TCHIBO', 'COFEINA']
uber_keywords = ['UBER']
diningout_keywords = ['MCDONALDS', 'BURGER', 'KFC', 'BINH MINH', 'PHO', 
'PIZZA','BURGER KING', 'NORTH', 'FISH', 'RESTAURACJA', 'CUKIERNIA', 'BAR', 
'POLECAM', 'TACAMOLE', 'FOOD', 'QUANG']
transport_keywords = ['BILET', 'BILETY', 'INTERCITY.PL', 'SKYCASH']

indices = (0, 15, 2, 6)

def find_category(result):
    if any(word.casefold() in result.casefold() for word in groceries_keywords):
        return 'Groceries'
    elif any(word.casefold() in result.casefold() for word in coffee_keywords):
        return 'Coffee'
    elif any(word.casefold() in result.casefold() for word in uber_keywords):
        return 'Uber'
    elif any(word.casefold() in result.casefold() for word in diningout_keywords):
        return 'Dining Out'
    elif any(word.casefold() in result.casefold() for word in transport_keywords):
        return 'Transport'

def do_ING_magic(line, writer):
    if len(line)>0:
        try:
            result = [line[i] for i in indices] 
            print('result: {}'.format(result) )
            result[0] = datetime.datetime.strptime(result[0], "%d.%m.%Y").strftime("%Y-%m-%d")
            print('result 0: {}'.format(result[0]) )
            result[3] = result[3].replace(',', '.')
            print('result 3: {}'.format(result[0]) )            
            if result[3] == "":
                result[3] = line[8].replace(',','.')
            result[1] = find_category(result[2])
            print(result)
            writer.writerow(result)
        except:
            pass

def csv_convert(filename):
    print("Let's begin")
    with open(filename, 'r') as f_in:
        with open(os.path.splitext(filename)[0]+"new.csv", 'w') as f_out:
            reader = csv.reader(f_in, delimiter=';')
            writer = csv.writer(f_out, delimiter=',')
            #writer.writerow(['Date','Category','Memo','Amount'])
            for line in reader:
                do_ING_magic(line, writer)
            return os.path.splitext(filename)[0]+"new.csv"