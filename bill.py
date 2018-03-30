from tkinter import *
import pymysql
import random


class Bill:
    def __init__(self, aadhar_no, duration, charge, mode, car_no, amount):

        self.root = Tk()
        self.root.title('BILL')
        self.root.geometry('{}x{}'.format(450, 280))

        self.db = pymysql.connect("localhost", 'root', 'kanchan', 'test1')
        self.cursor = self.db.cursor()
        self.head = Frame(self.root)
        self.head.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.cursor.execute("select cust_name, contact, aadhar_no from customer where aadhar_no='{}';".format(aadhar_no))
        self.data = list(self.cursor.fetchall())
        self.data = [x for x in self.data[0]]
        #print(self.data)

        self.cursor.execute("select car_model from car where car_no='{}';".format(car_no))
        self.car_model = list(self.cursor.fetchall())[0][0]

        if mode == 1:
            self.pmode = "Cash"
        else:
            self.pmode = "Card"

        self.tid = random.randint(1, 10**9)

        #print(self.tid, self.car_model, duration, charge, self.pmode, aadhar_no)
        self.cursor.execute("insert into bill values('{}', '{}', '{}', '{}', '{}');".format(
            self.tid, duration, amount, self.pmode, aadhar_no))
        self.db.commit()
        self.db.close()

        Label(self.head, text='Transaction ID: ' + str(self.tid), font=("DejaVu Sans Mono", 15), width=30).grid(
            row=0, column=0, sticky=W)
        Label(self.head, text='Name: ' + str(self.data[0]), font=("DejaVu Sans Mono", 15), width=20).grid(
            row=1, column=0, sticky=W)
        Label(self.head, text='Contact: ' + str(self.data[1]), font=("DejaVu Sans Mono", 15), width=20).grid(
            row=2, column=0, sticky=W)
        Label(self.head, text='Aadhar ID: ' + str(self.data[2]), font=("DejaVu Sans Mono", 15), width=20).grid(
            row=3, column=0, sticky=W)
        Label(self.head, text='CAR: ' + str(self.car_model), font=("DejaVu Sans Mono", 15), width=20).grid(
            row=4, column=0, sticky=W)
        Label(self.head, text='Duration: ' + str(duration) + ' hrs', font=("DejaVu Sans Mono", 15), width=20).grid(
            row=5, column=0, sticky=W)
        Label(self.head, text='Charge per Hour: ' + str(charge), font=("DejaVu Sans Mono", 15), width=20).grid(
            row=6, column=0, sticky=W)
        Label(self.head, text='Payment Mode: ' + str(self.pmode), font=("DejaVu Sans Mono", 15), width=20).grid(
            row=7, column=0, sticky=W)
        Label(self.head, text='Amount: ' + str(amount), font=("DejaVu Sans Mono", 15), width=20).grid(
            row=8, column=0, sticky=W)

        self.root.mainloop()

