# Checkbook Program
Written by Matthew Thornton, @matt8094

## About:
As a broke college student on a very tight budget, I came to the dilema that I needed a way of accurately keeping up with my budgets and finances. I could have used a regular checkbook, but, as any programmer knows, it's way more fun to write a program to do it for you. So this program was born. It started out as just a command line program that would read and write from local files on the computer. Then I came across the problem that I have multiple devices, and it would not do to have access to this program restricted to just one device. Luckily I have a server for these kind of issues. So the network part of the program was born. It will connect to a server upon startup and grab the files from there, then read from them. If there are any changes made to the files, it will upload them to the server when the program is **gracefully** ended. 

After all that was said and done, it popped into my mind that this is something that I will be using for quite some time, so it needs to be very user friendly for added incentive for me to stick with it. That's when I started working on the version with a dedicated GUI. This took some time as this was the first time I had ever worked with GUIs in Python, but it wasn't soon after, the GUI was finally done! If you work with Python GUIs professionally, please be kind when you see the *most likely* botched code.

## Installation
The GUI version works on Windows, Mac, and Linux. So if you are using one of those, I recommend using that version, just for the sake of simplicity. The networking comes integrated, therefore I will include instructions to use that, and I will also provide instructions to disable it if you wish to **not** use it.

Download the code file of whichever version you want, and place it wherever you want in your filesystem. I recommend **not** placing it anywhere that administrator priviledges are required. In the folder of the code, you will need to make 3 different files. I will cover the transactions file and the budgets file here, and the networking file will be covered later.

### Transactions File:
This is where the transactions will be stored, obviously. To start, you need to make a file called **transactions.txt**. On this first line of this file you will put your current balance as a floating point number. 

On the second line, you will put the abbreviated version of the current month and the last two digits of the current year separated by a dash.

```
1234.56
Aug-19
```

### Budgets File:
This is where the budgets will be stored. Starting off it is easier to write them all in the file with the correct syntax rather than using the program itself to make them, as that can become quite tedious. On each line you will simply put the name of the budget and the upper limit of the budget separated by a comma **without a space**.

```
Rent,774.00
Bills,100.00
Groceries,300.00
```

You can make as many different budgets as you want.

## Networking

This one is a bit tricky. I will not go over how to set up a server, but I will show you how to use this program if you have one that ready to use, or you feeling like making one. 

### Network.cfg:
This is where you will store the IP address, port, username, password, and appropriate file paths for connecting to your server. On the very first line of the network.cfg file you will have all that it required for connecting to the server. It will be the IP, port, username, and password all separated by commas with **no spaces**. The port number can be a custom port, whatever you use for connecting via ssh. If you do not use a custom port, use 22 in the file as that is the default port for ssh.

The second line will be the file path to the transactions.txt file and the third line will be the file path to the budgets.txt file.

```
10.0.0.0,22,username,password
/home/server/path/to/transactions.txt
/home/server/path/to/budgets.txt
```

If you instead **do not want to use the networking** these following steps must be followed exactly.

#### Non-GUI Version:
In the __main__.py file, you must comment out, or delete, lines 159-162. Therefore, it will look like this:

```python
"""
if self.budget_change or self.changed:
                    self.control.putFiles()
"""
```

And in the budgetController.py file, you must comment out line 81. 

```python
# self.getFiles()
```

After that, the networking will not longer be used in the program.

#### GUI Version:
In the __main__.py file, comment out, or delete, lines 105-108. 

```python
"""
if BUDGET_CHANGED or CHANGED:
            bControl.putFiles()
"""
```

And in the budgetController.py file, comment out or delete line 86.

```python
# self.getFiles()
```

And after that, the networking will not longer be used.
