import tkinter as tk
import subprocess as sp
import time
from PIL import Image, ImageTk
import pytesseract

input_dir   = './'
input_file  = 'test.png'
infi        = input_dir+input_file
output_dir  = './'
output_file = 'test_output.png'
outfi       = output_dir+output_file

class Controls(tk.Frame):
        theOtherWindow  = None        
        master          = None
        
        size                = 100
        threshold           = 50
        brightness          = 0
        contrast            = 0
        NUM_OF_ITERATIONS   = 10
        last_command        = []
        
        border      = '3x3'
        bordercolor = 'White'
        
        def __init__(self, master=None):
            super().__init__(master)
            
            self.master = master
            
            # ======== SCALES ========
            lab_sre = tk.Label(master, name='lab_sre', text='Resize').grid(row=3, column=0, sticky=tk.W)

            sre = tk.Scale(master, name='sre', orient=tk.HORIZONTAL, length=300, resolution=25, from_=100, to=1000, tickinterval=900, command=self.updateSize).grid(row=3, column=1)
            h = master.nametowidget('sre')
            h.set(100)


            lab_sth = tk.Label(master, name='lab_sth', text='Threshold').grid(row=4, column=0, sticky=tk.W)

            sth = tk.Scale(master, name='sth', orient=tk.HORIZONTAL, length=300, resolution=1, from_=0, to=100, tickinterval=100, command=self.updateThreshold).grid(row=4, column=1)
            h = master.nametowidget('sth')
            h.set(85)


            lab_sbr = tk.Label(master, name='lab_sbr', text='Brightness').grid(row=5, column=0, sticky=tk.W)

            sbr = tk.Scale(master, name='sbr', orient=tk.HORIZONTAL, length=300, resolution=1, from_=-100, to=100, tickinterval=100, command=self.updateBrightness).grid(row=5, column=1)
            h = master.nametowidget('sbr')
            h.set(-42)


            lab_sco = tk.Label(master, name='lab_sco', text='Contrast').grid(row=6, column=0, sticky=tk.W)

            sco = tk.Scale(master, name='sco', orient=tk.HORIZONTAL, length=300, resolution=1, from_=-100, to=100, tickinterval=100, command=self.updateContrast).grid(row=6, column=1)
            h = master.nametowidget('sco')
            h.set(100)


            lab_sbo = tk.Label(master, name='lab_sbo', text='Border size').grid(row=7, column=0, sticky=tk.W)

            sbo = tk.Scale(master, name='sbo', orient=tk.HORIZONTAL, length=300, resolution=1, from_=0, to=10, tickinterval=10, command=self.updateBorder).grid(row=7, column=1)
            h = master.nametowidget('sbo')
            h.set(3)

            # ====== /SCALES ======
            
            check_timings_btn = tk.Button(master, text='Check timings with following\n amount of iterations', name='check_timings_btn', command=self.check_timings).grid(row=8, column=0)

            num_of_iterations = tk.Text(master, name='num_of_iterations_text', width=4, height=1).grid(row=8, column=1, sticky=tk.W)
            h = master.nametowidget('num_of_iterations_text')
            h.insert(tk.END, str(self.NUM_OF_ITERATIONS))
            
            # time to execute pytesseract image_to_string, i.e. read the image
            lab_exec_pytess = tk.Label(master, name='lab_exec_pytess', text='Exec. time pytesseract [s]').grid(row=9, column=0, sticky=tk.W)
            exectime_pytess = tk.Label(master, text='', name='exectime_pytess', font='Helvetica 16').grid(row=9, column=1)

            # time to invoke the 'convert' function and execute it
            lab_exec_conv = tk.Label(master, name='lab_exec_conv', text='Exec. time convert [s]').grid(row=10, column=0, sticky=tk.W)
            exectime_convert = tk.Label(master, text='', name='exectime_convert', font='Helvetica 16').grid(row=10, column=1)
            
        def setTheOtherWindow(self, tow):
            self.theOtherWindow = tow
                
        def updateThreshold(self, value):
            self.threshold = value
            self.updateImage()
            
        def updateSize(self, value):
            self.size = value
            self.updateImage()
            
        def updateContrast(self, value):
            self.contrast = value
            self.updateImage()

        def updateBrightness(self, value):
            self.brightness = value
            self.updateImage()

        def updateBorder(self, value):
            self.border = str(value)+'x'+str(value)
            self.updateImage()
            
        def updateImage(self):
            global infi
            global outfi
        
            s0 = time.time()
            self.last_command = ['convert', infi, '-resize', str(self.size)+'%', '-brightness-contrast', str(self.brightness)+'x'+str(self.contrast), '-threshold', str(self.threshold)+'%', '-border',self.border,'-bordercolor', self.bordercolor, outfi]
            sp.call(self.last_command)
            
            s1 = time.time()
            
            read = pytesseract.image_to_string(Image.open(outfi))
            s2 = time.time()
            
            
            h = self.theOtherWindow.nametowidget('tesseract')
            h.config(text=read)
            
            h = self.master.nametowidget('exectime_convert')
            h.config(text=str(s1-s0))
            
            h = self.master.nametowidget('exectime_pytess')
            h.config(text=str(s2-s1))
            
            # redraw update image
            # destroy old
            h = self.theOtherWindow.nametowidget('img_label')
            h.destroy()
            
            #create new
            self.img2 = tk.PhotoImage(file=outfi)
            l = tk.Label(self.theOtherWindow, image=self.img2, name='img_label').grid(row=2)
        
        def check_timings(self):
            global outfi

            h = self.master.nametowidget('num_of_iterations_text')
            self.NUM_OF_ITERATIONS = int(h.get('current linestart', tk.END))

            avg_convert = 0
            avg_tesseract = 0
            for i in range(self.NUM_OF_ITERATIONS):
                s = time.time()
                sp.call(self.last_command)
                
                s1 = time.time()
                
                read = pytesseract.image_to_string(Image.open(outfi))
                s2 = time.time()
                
                avg_convert += s1-s
                avg_tesseract += s2-s1

            avg_convert     /= self.NUM_OF_ITERATIONS
            avg_tesseract   /= self.NUM_OF_ITERATIONS

            h = self.master.nametowidget('exectime_convert')
            h.config(text=str(avg_convert))

            h = self.master.nametowidget('exectime_pytess')
            h.config(text=str(avg_tesseract))
        
class Display(tk.Frame):
        img = ''
        img2 = ''
        master = None
        
        def __init__(self, master=None):
            super().__init__(master)
            
            self.master = master
            
            # pytesseract output
            tesseract = tk.Label(master, text='', name='tesseract', font='Helvetica 16').grid(row=0)
            
            global infi
            global outfi
            
            self.img = tk.PhotoImage(file=infi)
            l = tk.Label(master, image=self.img).grid(row=1)

            self.img2 = tk.PhotoImage(file=outfi)
            l2 = tk.Label(master, image=self.img2, name='img_label').grid(row=2)
    
def main():    
    root = tk.Tk()
    root.title('Controls - Pytesseract interactive filtering')
    controls = Controls(root)
    
    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    root.geometry('+150+150') #str(int(ws/2))+'x'+str(int(hs))+'+0+0')

    second_win = tk.Toplevel(root)
    second_win.title('Display - Pytesseract interactive filtering')
    second_win.geometry('+650+150')#str(int(ws/2))+'x'+str(int(hs))+'+'+str(int(ws/2))+'+0')
    d = Display(second_win)
    
    controls.setTheOtherWindow(second_win)
    
    # just to create an output file immediately
    global infi
    global outfi
    sp.call(['convert', infi, outfi])
    
    root.mainloop()
    
if __name__ == '__main__':
    main()
