from tkinter import *
import pymysql


class Rental:

    def insert_cust(self):
        #print(self.entry1.get(), self.entry4.get(), self.entry5.get(), self.entry2.get(), self.entry3.get(), self.v3.get())
        self.cursor.execute("insert into customer(cust_name, check_in_date, check_in_time, contact, aadhar_no) \
                       values('{}', '{}', '{}', '{}', '{}');".format(self.entry1.get(), self.entry4.get(), self.entry5.get(), self.entry2.get(), self.entry3.get()))
        self.cursor.execute("insert into car_to_customer values('{}', '{}');".format(self.v3.get(), self.entry3.get()))
        self.cursor.execute("update car set available='no' where car_no='{}';".format(self.v3.get()))
        self.db.commit()
        self.db.close()
        self.root.destroy()

    def car_model(self, val):
        self.cursor.execute("select car_model from car where car_type={} and available='yes';".format(val))
        data = list(self.cursor.fetchall())
        models = [x[0] for x in data]
        #print("inside:", models)
        self.v2 = StringVar(self.car_details)
        self.v2.set("Select model")
        self.modelname.grid_forget()
        model = Label(self.car_details, text='Model', font=("DejaVu Sans Mono", 15), width=5).grid(row=2, column=2, sticky=W)
        self.modelname = OptionMenu(self.car_details, self.v2, *models, command=self.car_number)
        self.modelname.grid(row=2, column=3, sticky=W)

    def car_number(self, val):
        #print('car choodsn', val)
        if val:
            self.cursor.execute("select car_no from car where car_model='{}';".format(val))
            data = list(self.cursor.fetchall())
            numbers = [x[0] for x in data]
            #print("inside:", numbers)
            self.car_no.grid_forget()
            self.v3 = StringVar(self.car_details)
            self.v3.set(numbers[0])
            carno = Label(self.car_details, text='Car No', font=("DejaVu Sans Mono", 15), width=6).grid(row=3, column=0, sticky=W)
            self.car_no = OptionMenu(self.car_details, self.v3, *numbers)
            self.car_no.grid(row=3, column=1)
            
    def __init__(self):
        self.db = pymysql.connect("localhost", 'root', 'kanchan', 'test1')
        self.cursor = self.db.cursor()
        self.cursor.execute("select sysdate();")
        data = list(self.cursor.fetchall())
        date_time = str(data[0][0]).split()

        self.root = Tk()
        self.root.title('BookDesk')
        self.root.geometry('{}x{}'.format(450, 300))
    
        head_f = Frame(self.root)
        head_f.pack(side=TOP)
    
        driver_detail = Frame(self.root)
        driver_detail.pack(side=TOP)
    
        head = Label(head_f, text='BOOKING')
        head.config(width=50, font=("DejaVu Sans Mono", 18))
        head.pack()
    
        name = Label(driver_detail, text='NAME', font=("DejaVu Sans Mono", 15), width=8)
        name.grid(row=0, column=0, sticky=W)

        self.entry1 = Entry(driver_detail, font=('DejaVu Sans Mono', 11))
        self.entry1.grid(row=0, column=1)
    
        contact = Label(driver_detail, text='CONTACT No', font=("DejaVu Sans Mono", 15), width=14).grid(row=1, column=0, sticky=W)
        self.entry2 = Entry(driver_detail, font=('DejaVu Sans Mono', 11))
        self.entry2.grid(row=1, column=1)
    
        aadharid = Label(driver_detail, text='AADHAR ID', font=("DejaVu Sans Mono", 15), width=13).grid(row=2, column=0, sticky=W)
        self.entry3 = Entry(driver_detail, font=('DejaVu Sans Mono', 11))
        self.entry3.grid(row=2, column=1)
    
        driver = Label(driver_detail, text="DRIVER", font=('DejaVu Sans Mono', 15), width=10).grid(row=3, column=0, sticky=W)

        self.var1 = IntVar()
        self.var1.set(1)
        c1 = Radiobutton(driver_detail, text='Yes', variable=self.var1, value=1)
        c1.grid(row=3, column=1, sticky=W)
        c2 = Radiobutton(driver_detail, text='No', variable=self.var1, value=0)
        c2.grid(row=3, column=2, sticky=W)

        self.car_details = Frame(self.root)
        self.car_details.pack(side=BOTTOM)
    
        checkin = Label(self.car_details, text='CHECK IN', font=("DejaVu Sans Mono", 15), width=8).grid(row=0, column=1)
    
        date = Label(self.car_details, text='Date', font=("DejaVu Sans Mono", 15), width=4).grid(row=1, column=0, sticky=W)
        self.entry4 = Entry(self.car_details, font=('DejaVu Sans Mono', 11), width=12)
        self.entry4.grid(row=1, column=1, sticky=W)
        self.entry4.insert(0, date_time[0])
    
        time = Label(self.car_details, text='Time', font=("DejaVu Sans Mono", 15), width=4).grid(row=1, column=2, sticky=W)
        self.entry5 = Entry(self.car_details, font=('DejaVu Sans Mono', 11), width=12)
        self.entry5.grid(row=1, column=3, sticky=W)
        self.entry5.insert(0, date_time[1][:-3])
    
        cars = [5, 7, 12]
        self.v1 = StringVar(self.car_details)
        self.v1.set('')
        cartype = Label(self.car_details, text='Car Seats', font=("DejaVu Sans Mono", 15), width=9).grid(row=2, column=0, sticky=W)
        type = OptionMenu(self.car_details, self.v1, *cars, command=self.car_model).grid(row=2, column=1, sticky=W)
    
        #print("printing models:", models)
        self.v2 = StringVar(self.car_details)
        self.v2.set("Select model")
        model = Label(self.car_details, text='Model', font=("DejaVu Sans Mono", 15), width=5).grid(row=2, column=2, sticky=W)
        self.modelname = OptionMenu(self.car_details, self.v2, [], command=self.car_number)
        self.modelname.grid(row=2, column=3, sticky=W)

        self.v3 = StringVar(self.car_details)
        self.v3.set("Select car number")
        carno = Label(self.car_details, text='Car No', font=("DejaVu Sans Mono", 15), width=6).grid(row=3, column=0, sticky=W)
        self.car_no = OptionMenu(self.car_details, self.v3, [])
        self.car_no.grid(row=3, column=1)

        self.book = Button(self.car_details, text='BOOK', font=("DejaVu Sans Mono", 15), anchor=CENTER, width=6, command=self.insert_cust)
        self.book.grid(row=5, column=1)

        self.root.mainloop()


if __name__ == "__main__":
    Rental()

