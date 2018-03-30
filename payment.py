from tkinter import *
import pymysql
import bill


class Payment:
    def insert_into_table(self):
        #print(self.a_no, self.duration, self.charge, self.var1.get(), self.v3.get())
        #print(self.v3.get(), self.e2.get())
        self.cursor.execute("update customer set check_out_date='{}', check_out_time='{}' where aadhar_no='{}';".format(self.e1.get(), self.e2.get(), self.a_no))
        self.cursor.execute("delete from car_to_customer where aadhar_no='{}';".format(self.a_no))
        self.cursor.execute(" update car set available='yes' where car_no='{}';".format(self.v3.get()))
        self.db.commit()
        self.db.close()
        self.root.destroy()
        bill.Bill(self.a_no, self.duration, self.charge, self.var1.get(), self.v3.get(), self.total)

    
    def show(self, val):

        self.cursor.execute("select charges_per_hour from car where car_no='{}'".format(self.v3.get()))
        self.charge = list(self.cursor.fetchall())[0][0]
        l1 = Label(self.amount, text='Charge per hours = {}'.format(self.charge), font=("DejaVu Sans Mono", 15), width=20).grid(
            row=0, column=0, sticky=W)
        self.cursor.execute("select aadhar_no from car_to_customer where car_no='{}';".format(self.v3.get()))
        self.a_no = list(self.cursor.fetchall())[0][0]
        self.cursor.execute("select check_in_date, check_in_time from customer where aadhar_no='{}';".format(self.a_no))
        data = list(self.cursor.fetchall())
        check_in = [x for x in data[0]]
        #print(check_in)
        check_out = [self.e1.get(), self.e2.get()]
        #print(check_out)
        years = int(check_out[0][:4]) - int(check_in[0][:4])
        months = int(check_out[0][5:7]) - int(check_in[0][5:7])
        days = int(check_out[0][8:]) - int(check_in[0][8:])
        hrs = int(check_out[1][:2]) - int(check_in[1][:2])
        minutes = int(check_out[1][3:]) - int(check_in[1][3:])
        if minutes < 0:
            hrs -= 1
            minutes = 60 - minutes
        if hrs < 0:
            days -= 1
            hrs = 24 - hrs
        #print('years, months, days', years, months, days, hrs, minutes)
        self.duration = str((years * 365 + months * 30 + days) * 24 + hrs) + ':' + str(minutes)
        self.total = ((years * 365 + months * 30 + days) * 24 + hrs) * self.charge + (minutes*self.charge)/60
        self.total = "%.2f" % self.total
        Label(self.amount, text='Duration = {} hrs'.format(self.duration), font=("DejaVu Sans Mono", 15), width=20).grid(
            row=1, column=0, sticky=W)
        Label(self.amount, text='AMOUNT Generated = {}'.format(self.total), font=("DejaVu Sans Mono", 15), width=26).grid(
            row=2, column=0, sticky=W)

    def __init__(self):

        self.a_no = ''
        self.db = pymysql.connect("localhost", 'root', 'kanchan', 'test1')
        self.cursor = self.db.cursor()
        self.cursor.execute("select sysdate();")
        data = list(self.cursor.fetchall())
        date_time = str(data[0][0]).split()

        self.cursor.execute("select car_no from car where available='no';")
        data = list(self.cursor.fetchall())
        numbers = [x[0] for x in data]
        #print("inside:", numbers)

        self.root = Tk()
        self.root.title('Payment')
        self.root.geometry('{}x{}'.format(450, 280))

        self.head_f = Frame(self.root)
        self.head_f.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.v3 = StringVar(self.head_f)
        self.v3.set("Select Car Number")
        select = Label(self.head_f, text='Car No', font=("DejaVu Sans Mono", 15), width=6).grid(row=0, column=0, sticky=W)
        if numbers:
            self.car_no = OptionMenu(self.head_f, self.v3, *numbers, command=self.show)
        else:
            self.car_no = OptionMenu(self.head_f, self.v3, [])
        self.car_no.grid(row=0, column=1, sticky=W)

        checkout = Label(self.head_f, text='CHECK OUT', font=("DejaVu Sans Mono", 15), width=10).grid(row=1, column=1)

        date = Label(self.head_f, text='Date', font=("DejaVu Sans Mono", 15), width=4).grid(row=2, column=0, sticky=W)
        self.e1 = Entry(self.head_f, font=('DejaVu Sans Mono', 11), width=12)
        self.e1.grid(row=2, column=1, sticky=W)
        self.e1.insert(0, date_time[0])

        time = Label(self.head_f, text='Time', font=("DejaVu Sans Mono", 15), width=4).grid(row=2, column=2, sticky=W)
        self.e2 = Entry(self.head_f, font=('DejaVu Sans Mono', 11), width=8)
        self.e2.grid(row=2, column=3, sticky=W)
        self.e2.insert(0, date_time[1][:-3])

        mode = Label(self.head_f, text="Payment Mode", font=('DejaVu Sans Mono', 15), width=12).grid(row=3, column=0, sticky=W)

        self.var1 = IntVar()
        self.var1.set(1)
        c1 = Radiobutton(self.head_f, text='Cash', variable=self.var1, value=1)
        c1.grid(row=3, column=1, sticky=W)
        c2 = Radiobutton(self.head_f, text='Card', variable=self.var1, value=0)
        c2.grid(row=3, column=2, sticky=W)

        self.amount = Frame(self.root)
        self.amount.place(relx=0.5, rely=0.7, anchor=S)

        self.pay = Button(self.root, text='PAY', command=self.insert_into_table)
        self.pay.place(relx=0.5, rely=0.9, anchor=S)

        self.root.mainloop()


if __name__ == "__main__":
    Payment()