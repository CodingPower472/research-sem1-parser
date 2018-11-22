
import serial
import time

ser = serial.Serial('/dev/cu.usbmodem14101')
file = open('data.csv', 'a+')

def write_value(red, green, blue, reaction_time):
    data_point_str = red + ',' + green + ',' + blue + ',' + reaction_time + '\n'
    file.write(data_point_str)
    print('Added.')

while True:
    data = ser.read()
    time.sleep(1)
    data_remaining = ser.inWaiting()
    data += ser.read(data_remaining)
    data = str(data)
    lines = data.split('\\r\\n')
    red = 0
    blue = 0
    green = 0
    diff = 0
    for line in lines:
        if line.startswith('b\'RGB:'):
            open_paren = line.find('(')
            close_paren = line.find(')')
            numbers_str = line[open_paren + 1:close_paren]
            numbers_splitted = numbers_str.split(',')
            red = numbers_splitted[0].strip()
            blue = numbers_splitted[1].strip()
            green = numbers_splitted[2].strip()
        elif line.startswith('Differential:'):
            colon_index = line.find(':')
            ms_index = line.find('ms')
            diff_str = line[colon_index + 1:ms_index].strip()
            diff = diff_str
    if red and blue and green and diff:
        response = input('Would you like to add data point RGB(%s, %s, %s): %sms? (Y/n) ' % (red, blue, green, diff)).strip().lower()
        if response != 'no' and response != 'n':
            print('Ok, adding.')
            write_value(red, green, blue, diff)
            # edit file now as opposed to when the program is ended
            file.close()
            file = open('data.csv', 'a+')
        else:
            print('Ok, not adding.')
