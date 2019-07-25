import sys, os, psutil, time, threading
from explorePDF import explorePDF
from tkinter import *
from tkinter import scrolledtext
from tkinter.simpledialog import askstring
from tkinter.filedialog import askdirectory
from win32api import GetSystemMetrics


class textMiner():
    def __init__(self):
        text = 'hello, this text will be used to test label text positioning, for this reason, i want it too long to show if there is a mistake in te sizesible feature os label i want to test'
        for i in range(5):
            text = text + text
        self.width = int(GetSystemMetrics(0) * 0.7)
        self.height = int(GetSystemMetrics(1) * 0.7)
        self.root = Tk()
        self.root.resizable(0, 0)
        self.root.title('textMiner V 0.0 pre-alpha - state: developing pdfMiner post-processing')
        self.root.geometry(f'{self.width}x{self.height}')
        self.placeWidgets()

    def placeWidgets(self):
        self.frame1 = Frame(self.root, bg='black', height=self.height, width=int(self.width / 4))
        self.frame1.pack_propagate(False)
        self.FpdfMiner = LabelFrame(self.frame1, text=r'pdfMiner', bg='black', relief=RIDGE,
                                    height=int(self.height / 3), width=int(self.width / 4), fg='white',
                                    font=("comic sans ms", 13, "bold"))
        self.FpdfMiner.pack_propagate(False)
        self.BpdfMiner = Button(self.FpdfMiner, command=self.auxFunc,
                                bg='Black', fg='white', font=("comic sans ms", 10), text='explorePDF')
        self.frame2 = Frame(self.root, bg='black', height=self.height, width=int(3 * self.width / 4))
        self.frame2.pack_propagate(False)
        self.state = scrolledtext.ScrolledText(self.frame2, undo=True, relief=RIDGE, bg='black', fg='white',
                                               height=self.height, width=int(3 * self.width / 4))
        self.state['font'] = ("comic sans ms", 12)
        self.state.pack(expand=True, fill='both')
        #         self.state.insert(END, text)
        #         self.state.config(state=DISABLED)
        # Packing all
        self.FpdfMiner.pack(side=TOP)
        self.BpdfMiner.pack(side=TOP)
        self.frame1.pack(side=LEFT)
        self.frame2.pack(side=LEFT)
        self.state.pack(side=LEFT)

    def pdfMiner(self):
        workPath = askdirectory(initialdir="/", title="Select directory where database is located")
        try:
            os.makedirs(os.path.join(workPath, r'reports'))
        except:
            if len(re.findall(r'y.*', self.proceed, re.IGNORECASE))>0:
                try:
                    os.remove(os.path.join(workPath, r'reports\consolidate.csv'))
                    os.remove(os.path.join(workPath, r'reports\rejected.txt'))
                except:
                    pass
            else:
                self.setState('process rejected')
                return
        # first we upgrade code
        database = explorePDF(workPath, self.state)  # creating explorePDF object
        database.upgrade()
        # and here we run pdfExplorer
        database = explorePDF(workPath, self.state)  # creating explorePDF object
        database.main()
        self.setState('********************************************')
        self.setState('database analized')
        self.setState('********************************************')

    def auxFunc(self):
        self.proceed = askstring(r'Confirm transaction', r'Reports will be erase, do you want proceed? (y/n):')
        process = threading.Thread(name='pdfMiner', target=self.pdfMiner, daemon=True)
        process.start()

    def setState(self, text):
        self.state.config(state=NORMAL)
        self.state.insert(END, '\n'+text)
        self.state.config(state=DISABLED)

    def _mainloop_(self):
        self.root.mainloop()