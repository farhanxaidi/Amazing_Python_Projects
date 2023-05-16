import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pygame

pygame.mixer.init(42050, -16, 2, 2048)
alarm_sound = pygame.mixer.Sound("MyAlarm.wav")

start_printed = False
stop_printed = True
done = False
finished = False
stop_clicked = False

class AlarmApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)


        self.title("Alarm Clock")

        self.resizable(width = False, height = False)

        self.hr = tk.IntVar(self)
        self.min = tk.IntVar(self)
        self.ampm = tk.StringVar(self)

        self.hr.set('12')
        self.min.set("00")
        self.ampm.set("AM")

        hours = []
        minutes = []
        ampmlist = ["AM","PM"]

        for x in range(1,13):
            hours.append(x)

        for y in range(0,60):
            minutes.append("%02d" % (y,))

        self.popmenuhours = tk.OptionMenu(self,self.hr, *hours)
        self.popmenuminutes = tk.OptionMenu(self,self.min, *minutes)
        self.popmenuAMPM = tk.OptionMenu(self, self.ampm, *ampmlist)

        self.popmenuhours.pack(side = "left")
        self.thing = tk.Label(text = ":").pack(side = "left")
        self.popmenuminutes.pack(side = "left")
        self.popmenuAMPM.pack(side = "left")

        self.alarmbutton = tk.Button(self, text="Set Alarm", command=self.start_clock)

        self.cancelbutton = tk.Button(self, text="Cancel Alarm", command=self.stop_clock, state = "disabled")
        self.stopalarmbutton = tk.Button(self, text = "Stop Alarm", command=self.stop_audio, state = "disabled")

        self.alarmbutton.pack()
        self.cancelbutton.pack()
        self.stopalarmbutton.pack()

    def start_clock(self):

        global done, start_printed, stop_printed, stop_clicked

        if done == False:

            self.cancelbutton.config(state = "active")

            self.alarmbutton.config(state = "disabled")

            if start_printed == False:

                print("Alarm set for {}:{}{}".format(self.hr.get(), "%02d" % (self.min.get()),self.ampm.get()))

                start_printed = True

                stop_printed = False

            if self.ampm.get() == "AM":
                if self.hr.get() in range(1,12):
                    hour_value = self.hr.get()
                else:
                    hour_value = self.hr.get() - 12
            if self.ampm.get() == "PM":
                if self.hr.get() in range(1,12):
                    hour_value = self.hr.get() +12
                else:
                    hour_value = self.hr.get()

            self.Alarm("%02d" % (hour_value,), "%02d" % (self.min.get()))

        if stop_clicked == True:
            done = False
            start_printed = False
            stop_clicked = False

    def stop_clock(self):
        global done, stop_clicked

        print("Alarm set for {}:{}{} has been cancelled".format(self.hr.get(), "%02d" % (self.min.get()),self.ampm.get()))

        stop_clicked = True

        done = True

        self.cancelbutton.config(state = "disabled")
        self.alarmbutton.config(state = "active")

    def stop_audio(self):

        pygame.mixer.Sound.stop(alarm_sound)

        self.stopalarmbutton.config(state = "disabled")
        self.alarmbutton.config(state = "active")



    def Alarm(self,myhour,myminute):
        global done, start_printed, finished

        if done == False:

            myhour,myminute = str(myhour),str(myminute)

            a = str(datetime.now())
            b = a.split(" ")[1].split(":")
            hour = b[0]
            minute = b[1]

            if hour == myhour and minute == myminute:

                pygame.mixer.Sound.play(alarm_sound, loops = -1)
                print("Alarm is ringing!")

                done = True

                finished = True

                self.cancelbutton.config(state = "disabled")
                self.stopalarmbutton.config(state = "active")

            else:

                self.after(1000, self.start_clock)
            done = False

        if finished == True:
            start_printed = False
            finished = False

app = AlarmApp()
app.mainloop()
