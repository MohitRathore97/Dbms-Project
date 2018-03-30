from tkinter import *
import pymysql


def main():
    db = pymysql.connect("localhost", 'root', 'mars', 'test1')
    cursor = db.cursor()

    def insert_cust():
        print(entry1.get(), entry4.get(), entry5.get(), entry2.get(), entry3.get(), v3.get())
        cursor.execute("insert into customer(cust_name, check_in_date, check_in_time, contact, aadhar_no) \
                       values('{}', '{}', '{}', '{}', '{}');".format(entry1.get(), entry4.get(), entry5.get(),
                                                                     entry2.get(), entry3.get()))
        cursor.execute("insert into car_to_customer values('{}', '{}');".format(v3.get(), entry3.get()))
        cursor.execute("update car set available='no', where car_no='{}'".format(v3.get()))
        db.commit()
        db.close()
        root.destroy()

    def car_model(val):
        global modelname, model

        cursor.execute("select car_model from car where car_type={} and available='yes';".format(val))
        data = list(cursor.fetchall())
        models = [x[0] for x in data]
        # print("inside:", models)
        v2 = StringVar(car_details)
        v2.set("Select model")
        modelname.grid_forget()
        model = Label(car_details, text='Model', font=("DejaVu Sans Mono", 15), width=5).grid(row=2, column=2, sticky=W)
        modelname = OptionMenu(car_details, v2, *models, command=car_number)
        modelname.grid(row=2, column=3, sticky=W)

    def car_number(val):
        global carno, car_no
        # print('car choodsn', val)
        if val:
            cursor.execute("select car_no from car where car_model='{}';".format(val))
            data = list(cursor.fetchall())
            numbers = [x[0] for x in data]
            # print("inside:", numbers)
            car_no.grid_forget()
            v3 = StringVar(car_details)
            v3.set(numbers[0])
            carno = Label(car_details, text='Car No', font=("DejaVu Sans Mono", 15), width=6).grid(row=3, column=0,
                                                                                                   sticky=W)
            car_no = OptionMenu(car_details, v3, *numbers)
            car_no.grid(row=3, column=1)

    cursor.execute("select sysdate();")
    data = list(cursor.fetchall())
    date_time = str(data[0][0]).split()

    root = Tk()
    root.title('BookDesk')
    root.geometry('{}x{}'.format(450, 280))

    head_f = Frame(root)
    head_f.pack(side=TOP)

    driver_detail = Frame(root)
    driver_detail.pack(side=TOP)

    head = Label(head_f, text='BOOKING')
    head.config(width=50, font=("DejaVu Sans Mono", 18))
    head.pack()

    name = Label(driver_detail, text='NAME', font=("DejaVu Sans Mono", 15), width=8)
    name.grid(row=0, column=0, sticky=W)

    entry1 = Entry(driver_detail, font=('DejaVu Sans Mono', 11))
    entry1.grid(row=0, column=1)

    contact = Label(driver_detail, text='CONTACT No', font=("DejaVu Sans Mono", 15), width=14).grid(row=1, column=0,
                                                                                                    sticky=W)
    entry2 = Entry(driver_detail, font=('DejaVu Sans Mono', 11))
    entry2.grid(row=1, column=1)

    aadharid = Label(driver_detail, text='AADHAR ID', font=("DejaVu Sans Mono", 15), width=13).grid(row=2, column=0,
                                                                                                    sticky=W)
    entry3 = Entry(driver_detail, font=('DejaVu Sans Mono', 11))
    entry3.grid(row=2, column=1)

    driver = Label(driver_detail, text="DRIVER", font=('DejaVu Sans Mono', 15), width=10).grid(row=3, column=0,
                                                                                               sticky=W)

    var1 = IntVar()
    var1.set(1)
    c1 = Radiobutton(driver_detail, text='Yes', variable=var1, value=1)
    c1.grid(row=3, column=1, sticky=W)
    c2 = Radiobutton(driver_detail, text='No', variable=var1, value=0)
    c2.grid(row=3, column=2, sticky=W)

    car_details = Frame(root)
    car_details.pack(side=BOTTOM)

    checkin = Label(car_details, text='CHECK IN', font=("DejaVu Sans Mono", 15), width=8).grid(row=0, column=1)

    date = Label(car_details, text='Date', font=("DejaVu Sans Mono", 15), width=4).grid(row=1, column=0, sticky=W)
    entry4 = Entry(car_details, font=('DejaVu Sans Mono', 11), width=12)
    entry4.grid(row=1, column=1, sticky=W)
    entry4.insert(0, date_time[0])

    time = Label(car_details, text='Time', font=("DejaVu Sans Mono", 15), width=4).grid(row=1, column=2, sticky=W)
    entry5 = Entry(car_details, font=('DejaVu Sans Mono', 11), width=12)
    entry5.grid(row=1, column=3, sticky=W)
    entry5.insert(0, date_time[1][:-3])

    cars = [5, 7, 12]
    v1 = StringVar(car_details)
    v1.set('')
    cartype = Label(car_details, text='Car Seats', font=("DejaVu Sans Mono", 15), width=9).grid(row=2, column=0,
                                                                                                sticky=W)
    type = OptionMenu(car_details, v1, *cars, command=car_model).grid(row=2, column=1, sticky=W)

    # print("printing models:", models)
    v2 = StringVar(car_details)
    v2.set("Select model")
    model = Label(car_details, text='Model', font=("DejaVu Sans Mono", 15), width=5).grid(row=2, column=2, sticky=W)
    modelname = OptionMenu(car_details, v2, [], command=car_number)
    modelname.grid(row=2, column=3, sticky=W)

    v3 = StringVar(car_details)
    v3.set("Select car number")
    carno = Label(car_details, text='Car No', font=("DejaVu Sans Mono", 15), width=6).grid(row=3, column=0, sticky=W)
    car_no = OptionMenu(car_details, v3, [])
    car_no.grid(row=3, column=1)

    book = Button(car_details, text='BOOK', font=("DejaVu Sans Mono", 15), anchor=CENTER, width=6, command=insert_cust)
    book.grid(row=5, column=1)

    root.mainloop()


if __name__ == "__main__":
    main()

