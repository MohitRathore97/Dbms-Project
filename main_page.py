from tkinter import *
import car_rental
import payment


root = Tk()
root.title('Car_rental')
root.geometry('{}x{}'.format(450, 280))

book = Button(root, text='BOOK', command=car_rental.Rental)
bill = Button(root, text='Generate Bill', anchor=CENTER, command=payment.Payment)
book.place(relx=0.5, rely=0.5, anchor=CENTER)
bill.place(relx=0.5, rely=0.3, anchor=N)

root.mainloop()