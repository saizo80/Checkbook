# Checkbook Program
Written by Matthew Thornton

## About:
As a broke college student on a very tight budget, I came to the dilema that I needed a way of accurately keeping up with my budgets and finances. I could have used a regular checkbook, but, as any programmer knows, it's way more fun to write a program to do it for you. So this program was born. It started out as just a command line program that would read and write from local files on the computer. Then I came across the problem that I have multiple devices, and it would not do to have access to this program restricted to just one device. Luckily I have a server for these kind of issues. So the network part of the program was born. It will connect to a server upon startup and grab the files from there, then read from them. If there are any changes made to the files, it will upload them to the server when the program is **gracefully** ended. 

After all that was said and done, it popped into my mind that this is something that I will be using for quite some time, so it needs to be very user friendly for added incentive for me to stick with it. That's when I started working on the version with a dedicated GUI. This took some time as this was the first time I had ever worked with GUIs in Python, but it wasn't soon after, the GUI was finally done! If you work with Python GUIs professionally, please be kind when you see the, *most likely*, botched code.

## Table of Contents:
- [Installation](#installation)
  - [Requirements](#requirements)
  - [Transactions File](#transactions)
  - [Budgets File](#budgets)
- [Networking](#networking)
  - [Network.cfg](#networkFile)
  - [Non-GUI Version](#non-gui)
  - [GUI Version](#gui)
- [Usage](#usage)
  - [Pyinstaller](#pyinstaller)

## Installation
The GUI version works on Windows, Mac, and Linux. So if you are using one of those, I recommend using that version, just for the sake of simplicity. The networking comes integrated, therefore I will include instructions to use that, and I will also provide instructions to disable it if you wish to **not** use it.

Download the code file of whichever version you want, and place it wherever you want in your filesystem. I recommend **not** placing it anywhere that administrator priviledges are required. In the folder of the code, you will need to make 3 different files. I will cover the transactions file and the budgets file here, and the networking file will be covered later.

### Requirements:
Python version 3 is required to run this and there are two module requirements:

- tkinter (for the GUI version)
- paramiko (for the ssh and sftp networking)
- The network, transactions, and budgets files need to be written in Notepad++ if on Windows (because of the way regular notepad handles carriage returns)

### Transactions File:<a name="transactions"></a>
This is where the transactions will be stored, obviously. To start, you need to make a file called **transactions.txt**. On this first line of this file you will put your current balance as a floating point number. 

On the second line, you will put the abbreviated version of the current month and the last two digits of the current year separated by a dash.

```
1234.56
Aug-19
```

### Budgets File:<a name="budgets"></a>
This is where the budgets will be stored. Starting off it is easier to write them all in the file with the correct syntax rather than using the program itself to make them, as that can become quite tedious. On each line you will simply put the name of the budget and the upper limit of the budget separated by a comma **without a space**.

```
Rent,774.00
Bills,100.00
Groceries,300.00
```

You can make as many different budgets as you want.

## Networking

This one is a bit tricky. I will not go over how to set up a server, but I will show you how to use this program if you have one that ready to use, or you feeling like making one. 

### Network.cfg:<a name="networkFile"></a>
This is where you will store the IP address, port, username, password, and appropriate file paths for connecting to your server. On the very first line of the network.cfg file you will have all that it required for connecting to the server. It will be the IP, port, username, and password all separated by commas with **no spaces**. The port number can be a custom port, whatever you use for connecting via ssh. If you do not use a custom port, use 22 in the file as that is the default port for ssh.

The second line will be the file path to the transactions.txt file, the third line will be the file path to the budgets.txt file, and the fourth line will be the file path to the folder you want to use to store the old transactions files when the month changes.

```
10.0.0.0,22,username,password
/home/server/path/to/transactions.txt
/home/server/path/to/budgets.txt
/home/server/path/to/old_transactions/
```

If you instead **do not want to use the networking** these following steps must be followed exactly.

#### Non-GUI Version:<a name="non-gui"></a>
In the __main__.py file, you must comment out, or delete, lines 159-162. Therefore, it will look like this:

```python
"""
if self.budget_change or self.changed:
                    self.control.putFiles()
"""
```

And in the budgetController.py file, you must comment out, or delete, lines 88 and 226. 

```python
# self.getFiles()
```

```python
# self.uploadOld()
```

After that, the networking will not longer be used in the program.

#### GUI Version:<a name="gui"></a>
In the __main__.py file, comment out, or delete, lines 105-108. 

```python
"""
if BUDGET_CHANGED or CHANGED:
            bControl.putFiles()
"""
```

And in the budgetController.py file, comment out or delete lines 93 and 235.

```python
# self.getFiles()
```

```python
# self.uploadOld()
```

And after that, the networking will not longer be used.

## Usage:
The usage of this program is fairly straightforward in and of itself. There are proper labels and everything should be self explanatory. One thing that you need to know is that **if you make changes, you must use the quit option/button in the main menu**. If you have made changes and you exit out of the program without letting it **gracefully** shutdown, it will not save any of the changes that you have made. This is very important, especially if you are making many changes at a time.

### Pyinstaller:
An interesting thing that you can do if you are on Windows or Mac is compile the program into an appropriate executable file, .exe on Windows and .command on Mac. If you do not have pyinstaller installed, it is a very easy thing to do. Just `pip install pyinstaller` will do the trick.

You can also use a custom icon when you do this, just to change it from the default python icon **(just note that the file must be a .ico file)**. I have since included the .ico file that I personally use in the topmost folder of the repository.

For the Non-GUI version, the syntax will be:
```
pyinstaller /path/to/__main__.py --icon=/path/to/.ico
```
And for the GUI version I recommend using the following:
```
pyinstaller /path/to/__main__.py --noconsole --icon=/path/to/.ico
```
The `--noconsole` will ensure that the command prompt will not open when the GUI version is launched.

With either of these commands, it will create a few folders wherever your __main__.py file is located. Move the transactions.txt, budgets.txt, and network.cfg into the dist/__main__/ folder (where the __main__.exe file is). Then you can make a shortcut to the .exe or .command file and put that wherever you want. Then just launching that app will open up the application for you.