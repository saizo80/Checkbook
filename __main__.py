import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import checkbookFunctions, os
from datetime import date

todayBuffer = date.today()
today = todayBuffer.strftime('%b-%y')
transactionDate = todayBuffer.strftime('%m-%d-%y')

class tkinterApp(tk.Tk): 
      
    # __init__ function for class tkinterApp  
    def __init__(self, *args, **kwargs):  
          
        # __init__ function for class Tk 
        tk.Tk.__init__(self, *args, **kwargs) 
          
        # creating a container 
        self.container = tk.Frame(self)   
        self.container.pack(side = "top", fill = "both", expand = True)  
        
        self.container.grid_rowconfigure(0, weight = 1) 
        self.container.grid_columnconfigure(0, weight = 1) 
        
        # initializing frames to an empty array 
        self.frames = {}   
   
        # iterating through a tuple consisting 
        # of the different page layouts 
        for F in (MainPage, TransactionsPage, BudgetsPage, addTransaction, editTransactions, editBudgets): 
   
            frame = F(self.container, self) 
   
            # initializing frame of that object from 
            # MainPage, TransactionsPage, BudgetsPage respectively with  
            # for loop 
            self.frames[F] = frame  
   
            frame.grid(row = 0, column = 0, sticky ="nsew") 
   
        self.show_frame(MainPage) 
    
    # to display the current frame passed as a parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    def updateAll(self):
        for f in self.frames:
            try:
                self.frames.get(f).update()
            except:
                pass
    def showFrameAndDestroy(self, toFrame, fromFrame):
        self.frames[fromFrame].destroy()
        frame = fromFrame(self.container, self)
        self.frames[fromFrame] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(toFrame)


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.label = tk.Label(self, text ="Main Page", font = LARGEFONT) 
        self.label.configure(anchor="center")
        self.label.pack(fill=tk.X, pady=10)
        
        button1 = ttk.Button(self, text="Transactions", command = lambda : controller.show_frame(TransactionsPage))
        button1.pack(fill=tk.X, pady=10)
        
        button2 = ttk.Button(self, text="Budget Goals", command = lambda : controller.show_frame(BudgetsPage))
        button2.pack(fill=tk.X, pady=10)
        
        killButton = ttk.Button(self, text="Quit", command = tty.kill)
        killButton.pack(fill=tk.X, pady=10)
        
    def button3Click(self):
        tty.jam(self.label)
        
class TransactionsPage(tk.Frame):  
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        
        label = tk.Label(self, text ="Transactions", font = LARGEFONT) 
        label.configure(anchor="center")
        label.pack(fill=tk.X, pady=10)
        
        self.txt = tk.Text(self, borderwidth=1, relief="sunken")
        self.txt.config(font=SMALLFONT, undo=True, wrap='word', width=40, height=20)
        self.txt.pack(padx=2, pady=2)
        self.txt.insert(1.0, tty.getTransactions())

        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.pack(side=tk.RIGHT)
        self.txt['yscrollcommand'] = scrollb.set
   
        button2 = ttk.Button(self, text ="Add Transaction", command = lambda : controller.show_frame(addTransaction)) 
        button2.pack(fill=tk.X)
        
        button3 = ttk.Button(self, text="Edit Transactions", command = lambda : controller.show_frame(editTransactions))
        button3.pack(fill=tk.X)
        
        returnButton = ttk.Button(self, text ="Return", command = lambda : controller.show_frame(MainPage)) 
        returnButton.pack(fill=tk.X)
        
    def temp(self, controller):
        print(tty.transReport())

    def updateAll(self, controller):
        controller.updateAll()
        
    def update(self):
        self.txt.delete("1.0", "end")
        self.txt.insert(1.0, tty.getTransactions())

class addTransaction(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Add Transaction:", font = LARGEFONT)
        #label.grid(row=1, column=2)
        label.pack()

        # - - - - - - - - - - - - - - - 
        # Specify Budget Type:
        self.budgetType = tk.StringVar()
        self.budgetType.set("0")
        budgetFrame = tk.LabelFrame(self, text="Budget Type", relief=tk.RIDGE, pady=6)
        #budgetFrame.grid(row=3, column=1, padx=6, sticky=tk.N + tk.S + tk.E + tk.W)
        budgetFrame.pack(pady=5)
        
        budgetrow = 1
        budgetcolumn = 1
        for i in tty.budgets:
            budget = ttk.Radiobutton(budgetFrame,text=tty.budgets.get(i).name,
                                     variable=self.budgetType,
                                     value=tty.budgets.get(i).name)
            budget.grid(row=budgetrow,column = budgetcolumn, sticky=tk.W + tk.N)
            #budget.pack()
            if budgetcolumn is 2:
                budgetcolumn = 1
                budgetrow += 1
            else:
                budgetcolumn +=1
        
        # - - - - - - - - - - - - - - -
        # Specify Amount:
        self.amount = tk.StringVar()
        self.amount = ""
        
        amountFrame = ttk.LabelFrame(self, text="Amount\n+ = Credit\n-  = Debit", relief=tk.RIDGE, padding=6)
        #amountFrame.grid(row=2, column=2, padx=6, sticky=tk.N + tk.S + tk.E + tk.W)
        amountFrame.pack(pady=5)
        
        self.amountEntry = ttk.Entry(amountFrame)
        #self.amountEntry.grid(row=1,column=1, sticky=tk.W+tk.N)
        self.amountEntry.pack()
        
        # - - - - - - - - - - - - -
        # Description:
        self.description = tk.StringVar()
        self.description = ""
        
        descriptionFrame = ttk.LabelFrame(self, text="Description", relief=tk.RIDGE, padding=6)
        #descriptionFrame.grid(row=3, column=2, padx=6, sticky=tk.N + tk.S + tk.E + tk.W)
        descriptionFrame.pack(pady=5)
        
        self.description = tk.Text(descriptionFrame, height=10, width=20)
        self.description.configure(font=SMALLFONT)
        #self.description.grid(row=1,column=1, sticky=tk.W+tk.N)
        self.description.pack()
        
         # - - - - - - - - - - - - - 
        # Specify Date:
        self.date = tk.StringVar()
        self.date = ""
        
        self.dateFrame = ttk.LabelFrame(self, text="Date:", relief=tk.RIDGE, padding=6)
        self.dateFrame.pack(pady=5)
        
        self.dateButton = ttk.Button(self.dateFrame, text="Not Today", command=self.showDate)
        self.dateButton.pack()
        self.dateEntry = ttk.Entry(self.dateFrame)
        

        # - - - - - - - - - - - - - 
        # Update and exit buttons
        enterButton = ttk.Button(self, text="Enter", width=25, command = lambda : self.passInfo(controller))
        #enterButton.grid(row=4,column=1)
        enterButton.pack()
        
        #quitButton = ttk.Button(self, text ="Cancel", width=25, command = lambda : controller.show_frame(TransactionsPage))
        quitButton = ttk.Button(self, text ="Cancel", width=25, command = lambda : self.reset(controller))
        #quitButton.grid(row=6, column=1)
        quitButton.pack()

    def passInfo(self, controller):
        if self.dateEntry.get() is "":
            tty.addTransaction(float(self.amountEntry.get()), self.budgetType.get(),
                              transactionDate,(self.description.get("1.0", "end")))
        else:
            tty.addTransaction(float(self.amountEntry.get()), self.budgetType.get(),
                              self.dateEntry.get(),(self.description.get("1.0", "end")))
        controller.updateAll()
        controller.show_frame(TransactionsPage)
    
    def showDate(self):
        self.dateFrame.configure(text="Enter Date: mm-dd-yy")
        self.dateButton.configure(text="Today", command=self.removeDate)
        self.dateEntry.pack()
    def removeDate(self):
        self.dateFrame.configure(text="Date:")
        self.dateButton.configure(text="Not Today", command=self.showDate)
        self.dateEntry.destroy()
        self.dateEntry = ttk.Entry(self.dateFrame)
    def reset(self, controller):
        controller.showFrameAndDestroy(TransactionsPage, addTransaction)
        

class editTransactions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Edit Transaction:", font=LARGEFONT)
        label.pack(pady=10,padx=10)
        
        self.combobox_value = tk.StringVar()
        self.combo = ttk.Combobox(self, height=10, width=50, textvariable=self.combobox_value)
        self.combo.pack()
        try:
            self.combo['values'] = tty.getTransactionsCombo()
        except:
            pass
        
        # - - - - - - - - - - - - - - - - -
        # Budget Type
        self.budgetType = tk.StringVar()
        self.budgetType.set("0")
        self.budgetFrame = tk.Frame(self, relief=tk.RIDGE)
        self.budgetFrame.pack(pady=5)
        
        self.budgetButton = ttk.Button(self.budgetFrame, text="Change Budget", command = self.showBudget)
        self.budgetButton.pack()
        
        # - - - - - - - - - - - - - - - - -
        # Amount
        self.amount = tk.StringVar()
        self.amount = ""
        
        self.amountFrame = tk.Frame(self, relief=tk.RIDGE)
        self.amountFrame.pack(pady=5)
        self.amountEntry = ttk.Entry(self.amountFrame)
        
        self.amountButton = ttk.Button(self.amountFrame, text="Change Amount", command = self.showAmount)
        self.amountButton.pack()

        # - - - - - - - - - - - - - - - - -
        # Date
        self.date = tk.StringVar()
        self.date = ""
        
        self.dateFrame = tk.Frame(self, relief=tk.RIDGE)
        self.dateFrame.pack(pady=5)
        
        self.dateButton = ttk.Button(self.dateFrame, text="Change Date", command=self.showDate)
        self.dateButton.pack()
        self.dateEntry = ttk.Entry(self.dateFrame)
        
        # - - - - - - - - - - - - - - - - -
        # Description:
        
        self.description = tk.StringVar()
        self.description = ""
        
        self.descriptionFrame = tk.Frame(self, relief=tk.RIDGE)
        self.descriptionFrame.pack(pady=5)
        
        self.description = tk.Text(self.descriptionFrame, height=10, width=20)
        self.description.configure(font=SMALLFONT)
        
        self.descriptionButton = ttk.Button(self.descriptionFrame, text="Change Description", command =self.showDescription)
        self.descriptionButton.pack()
        
        # - - - - - - - - - - - - - - - - - - 
        # Delete
        
        deleteFrame = tk.Frame(self, relief=tk.RIDGE)
        deleteFrame.pack(pady=5)
        
        deleteButton = ttk.Button(deleteFrame, text="Delete", command = lambda : self.deleteMethod(controller))
        deleteButton.pack()
        
        enterButton = ttk.Button(self, text="Enter", width=25, command = lambda : self.submitChanges(controller))
        enterButton.pack(pady=10)
        
        quitButton = ttk.Button(self, text="Cancel", width=25, command= lambda : self.reset(controller))
        quitButton.pack()
    
    def showBudget(self):
        self.budgetButton.destroy()
        budgetrow, budgetcolumn = 1, 1
        for i in tty.budgets:
            budget = ttk.Radiobutton(self.budgetFrame,text=tty.budgets.get(i).name,
                                     variable=self.budgetType,
                                     value=tty.budgets.get(i).name)
            budget.grid(row=budgetrow,column = budgetcolumn, sticky=tk.W + tk.N)
            #budget.pack()
            if budgetcolumn is 2:
                budgetcolumn = 1
                budgetrow += 1
            else:
                budgetcolumn +=1
        self.budgetType.set("{}".format(tty.comboboxReturn(self.combobox_value.get()).budget))
    
    def showAmount(self):
        self.amountButton.destroy()
        self.amountEntry.insert(0, "{:.2f}".format(tty.comboboxReturn(self.combobox_value.get()).amount))
        self.amountEntry.pack()
    
    def showDate(self):
        self.dateButton.destroy()
        self.dateEntry.insert(0, tty.comboboxReturn(self.combobox_value.get()).date)
        self.dateEntry.pack()
    
    def showDescription(self):
        self.descriptionButton.destroy()
        self.description.insert("1.0", tty.comboboxReturn(self.combobox_value.get()).descrip)
        self.description.pack()
        
    def reset(self, controller):
        controller.showFrameAndDestroy(TransactionsPage, editTransactions)
    
    def deleteMethod(self, controller):
        if messagebox.askyesno("Warning", "Delete {}?".format(self.combobox_value.get())):
            tty.removeTransaction(self.combobox_value.get())
            controller.updateAll()
            controller.showFrameAndDestroy(TransactionsPage, editTransactions)
        
    
    def update(self):
        try:
            self.combo['values'] = tty.getTransactionsCombo()
        except:
            pass
    
    def submitChanges(self, controller):
        date = self.dateEntry.get()
        amount = self.amountEntry.get()
        descrip = self.description.get("1.0", "end")
        budget = self.budgetType.get()
        data = self.combobox_value.get()
        tty.editTransaction(date, budget, amount, descrip, data)
        controller.updateAll()
        controller.showFrameAndDestroy(TransactionsPage, editTransactions)
        

        
         
class BudgetsPage(tk.Frame):  
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        
        label = tk.Label(self, text ="Budgets", font = LARGEFONT) 
        label.configure(anchor="center")
        label.pack(fill=tk.X, pady=10)
        
        self.txt = tk.Text(self, borderwidth=1, relief="sunken")
        self.txt.config(font=SMALLFONT, undo=True, wrap='word', width=40, height=20)
        self.txt.pack()
        self.txt.insert(1.0, tty.getBudgets())
        
        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.pack(side=tk.RIGHT)
        self.txt['yscrollcommand'] = scrollb.set
        
        button3 = ttk.Button(self, text="Edit Budgets", command = lambda : controller.show_frame(editBudgets))
        button3.pack(fill=tk.X)
        
        returnButton = ttk.Button(self, text ="Return", command = lambda : controller.show_frame(MainPage)) 
        returnButton.pack(fill=tk.X, pady=10)
    def update(self):
        self.txt.delete("1.0", "end")
        self.txt.insert(1.0, tty.getBudgets())
        
class editBudgets(tk.Frame):  
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        
        self.combobox_value = tk.StringVar()
        self.combo = ttk.Combobox(self, height=10, width=50, textvariable=self.combobox_value)
        self.combo.pack()
        try:
            self.combo['values'] = tty.budgetsCombo()
        except:
            pass
        
   
def center(win):
    win.update_idletasks()

    width = win.winfo_width()
    height = win.winfo_height()
    
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y)) 

if __name__ == "__main__":
    LARGEFONT = ("Arial", 35)
    SMALLFONT = ("Arial", 13)
    tty = checkbookFunctions.Functions()
    
    app = tkinterApp() 
    
    app.geometry("400x600")
    #app.maxsize(500, 500)
    
    app.title("CheckBook")
    
    center(app)
    
    os.system("clear")
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    app.mainloop()        