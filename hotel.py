# Case-study Hotel
# Developers:   Fyodorov M. (50%),
#               Ruchkina K. (35%)
#               Grishaev G. (35%)
import datetime
import random

roomTypesList = [('одноместный', 2900), ('двухместный', 2300),('полулюкс', 3200),('люкс', 4100)]
comfortList = [('стандарт', [1.0, 'без питания']), ('стандарт_улучшенный', [1.2, 'завтрак']),
               ('апартамент', [1.5, 'Полупансион'])]
foodList = [('без питания', 0), ('завтрак', 280),('Полупансион', 1000)]


class Room:
    def __init__(self, number, roomType, comfort, capacity):
        self.number = number
        self.roomType = roomType
        self.comfort = comfort
        self.capacity = capacity
        self.calendar = {}
        datePrev = datetime.date(2019, 12, 31)
        for i in range(366):
            datePrev += datetime.timedelta(days=1)
            self.calendar[datePrev] = 'free'
        self.base_cost = dict(roomTypesList)[self.roomType] * dict(comfortList)[self.comfort][0]

    def check_free(self, dateStart, nights):
        tmp = dateStart.split('.')
        dateStart = datetime.date(int(tmp[2]), int(tmp[1]), int(tmp[0]))
        for i in range(0, int(nights)):
            dateCheck = dateStart + datetime.timedelta(days=i)
            if self.calendar[dateCheck] != 'free':
                break
        else:
            return True
        return False


    def get_cost(self, clientsNumber):
        foodType = dict(comfortList)[self.comfort][1]
        return(self.base_cost + (dict(foodList)[foodType] * int(clientsNumber)))

    def booking(self, dateStart, nights):
        tmp = dateStart.split('.')
        dateStart = datetime.date(int(tmp[2]), int(tmp[1]), int(tmp[0]))
        for i in range(0, int(nights)):
            dateBook = dateStart + datetime.timedelta(days=i)
            self.calendar[dateBook] = 'book'


class BookingRecord:
    def __init__(self, dateBooking, fio, peopleAmount, dateIn, nights, money,full):
        self.dateBooking = dateBooking
        self.fio = fio
        self.peopleAmount = peopleAmount
        self.dateIn = dateIn
        self.nights = nights
        self.money = money
        self.status = 'new'
        self.full = full

class Hotel:
    prib = 0
    ubit = 0
    def __init__(self):
        self.rooms = []
        self.bookingRecords = []
        with open("fund.txt") as f:
            rooms = f.readlines()
        for room in rooms:
            room_info = room.split()
            tmpRoom = Room(number = room_info[0], roomType=room_info[1], comfort=room_info[3], capacity=int(room_info[2]))
            self.rooms.append(tmpRoom)
        with open('booking.txt') as f:
            bookings = f.readlines()
        for b in bookings:
            book_info = b.strip().split()
            fio_full = book_info[1] + book_info[2] + book_info[3]
            tmpBook = BookingRecord(dateBooking=book_info[0], fio=fio_full, peopleAmount=book_info[4],
                                    dateIn=book_info[5], nights=book_info[6], money=book_info[7],full = b)
            self.bookingRecords.append(tmpBook)
    def check_rooms(self, clientsNumber, dateStart, nights, maxCost):
        # сначала проверяем свободные комнаты
        freeRooms = []
        for room in self.rooms:

            if (int(room.capacity) >= int(clientsNumber)) and (room.check_free(dateStart, nights)) and (room.get_cost(int(clientsNumber)) <= int(maxCost)):
                freeRooms.append(room)
        return freeRooms

    def booking_room(self, clientsNumber, dateStart, nights, maxCost):
        rooms = self.check_rooms(clientsNumber, dateStart, nights, maxCost)
        if rooms:
            r = random.randint(1,4)
            maxi = 0
            for i in rooms:
                if maxi < i.base_cost:
                    maxi = i.base_cost
                    roomForBooking = i
            print('Найдена:', 'Номер', roomForBooking.number, roomForBooking.roomType, roomForBooking.comfort,
                  'рассчитан на', roomForBooking.capacity, 'чел.', 'фактически', clientsNumber,
                  dict(comfortList)[roomForBooking.comfort][1], 'стоимость:',int(nights)*(roomForBooking.base_cost  + (
                dict(foodList)[dict(comfortList)[roomForBooking.comfort][1]]) * int(clientsNumber)))

            if r != 4:
                # меняем календарь
                roomForBooking.booking(dateStart, nights)
                self.prib += int(nights) * (roomForBooking.base_cost + (dict(foodList)[dict(comfortList)[roomForBooking.comfort][1]] * int(clientsNumber)))
                # возвращаем обратно информацию об успешном бронировании
                return True
            else:
                print('Клиент отказался от варианта.','_____________________________________________________',sep = '\n')
                self.ubit += int(nights) * (roomForBooking.base_cost + (dict(foodList)[dict(comfortList)[roomForBooking.comfort][1]] * int(clientsNumber)))
                return False

        else:
            print('нет доступных номеров','_____________________________________________________',sep = '\n')
            self.ubit += int(maxCost)
            return False

    def booking_rooms(self):
        prib = 0
        date_u = self.bookingRecords[0].dateBooking
        for book in self.bookingRecords:
            if date_u != book.dateBooking:
                self.get_rooms(date_u)
                date_u = book.dateBooking
            print(book.full)
            if self.booking_room(book.peopleAmount, book.dateIn, book.nights, book.money) == True:
                book.status = 'book'
                print('Клиент согласен. Номер забронирован','_____________________________________________________',sep = '\n')
            else:
                book.status = 'reject'
        self.get_rooms(date_u)

    def get_rooms(self,date_check):
        k1 = [0,0]
        k2 = [0,0]
        k3 = [0,0]
        k4 = [0,0]
        for room in self.rooms:
            if room.roomType == 'одноместный':
                if room.check_free(date_check,1):
                    k1[0] += 1
                else:
                    k1[1] += 1
            if room.roomType == 'двухместный':
                if room.check_free(date_check, 1):
                    k2[0] += 1
                else:
                    k2[1] += 1
            if room.roomType == 'полулюкс':
                if room.check_free(date_check, 1):
                    k3[0] += 1
                else:
                    k3[1] += 1
            if room.roomType == 'люкс':
                if room.check_free(date_check, 1):
                    k4[0] += 1
                else:
                    k4[1] += 1
        print('Итог за',date_check)
        print('Количество занятых комнат',k1[1] + k2[1] + k3[1] + k4[1])
        print('Количество свободных комнат', k1[0] + k2[0] + k3[0] + k4[0])
        print('Занятость по категориям:')
        print('Одноместных',k1[1],'из',k1[0] + k1[1])
        print('Двухместных', k2[1], 'из', k2[0] + k2[1])
        print('Полулюкс', k3[1], 'из', k3[0] + k3[1])
        print('Люкс', k4[1], 'из', k4[0] + k4[1])
        print('Процент загруженности',((k1[1] + k2[1] + k3[1] + k4[1])/(sum(k1) + sum(k2) + sum(k3) + sum(k4)))*100)
        print('Доход за прошедшее время',self.prib)
        print('Убытки за прошедшее время',self.ubit)
        print('____________________________________')
h1 = Hotel()
h1.booking_rooms()
