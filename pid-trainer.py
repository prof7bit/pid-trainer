#!/usr/bin/env python3

import tkinter as tk
import math

FILTER = 50
WIDTH = 1200
HEIGHT = 400


class Gauss:
    """implements a Gauss filter (low pass) to model all the
    delay and physical inertia inside of the control loop"""
    def __init__(self, size):
        self.buffer = [0] * size
        self.size = size

    def update(self, value):
        for i in range(self.size):
            avg = (self.buffer[i] + value) / 2
            self.buffer[i] = value
            value = avg
        return value

    def reset(self, value):
        for i in range(self.size):
            self.buffer[i] = value


class PID:
    """implements a standard PID controller"""
    def __init__(self):
        self.kp = 0
        self.ki = 0
        self.kd = 0
        self.p = 0
        self.i = 0
        self.d = 0
        self.previous_error = 0

    def set_params(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def reset(self):
        self.previous_error = 0
        self.i = 0

    def calculate(self, error):
        self.p = error * self.kp
        self.i += error * self.ki
        self.d = (error - self.previous_error) * self.kd
        self.previous_error = error
        return self.p + self.i + self.d


class App:
    def __init__(self):
        self.filter = Gauss(FILTER)
        self.pid = PID()

        self.root = tk.Tk()
        self.root.title("PID trainer")
        self.slider_p = tk.Scale(self.root, from_=100, to=0, length=HEIGHT, command=self.update)
        self.slider_i = tk.Scale(self.root, from_=100, to=0, length=HEIGHT, command=self.update)
        self.slider_d = tk.Scale(self.root, from_=100, to=0, length=HEIGHT, command=self.update)
        self.plot = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, background="#000000")

        # initialize sliders with some reasonable values
        self.slider_p.set(31)
        self.slider_i.set(14)
        self.slider_d.set(36)

        self.plot.grid(row=0, column=0)
        self.slider_p.grid(row=0, column=1)
        self.slider_i.grid(row=0, column=2)
        self.slider_d.grid(row=0, column=3)

        self.update(None)
        self.root.mainloop()


    def update(self, event):
        """This method is called every time one of the sliders is moved"""
        self.pid.set_params(
            # arbitrary scaling factors to make it work nicely ;-)
            self.slider_p.get() * 0.001,
            self.slider_i.get() * 0.00001,
            self.slider_d.get() * 0.01
        )

        # reset everything to a defined state
        # to begin a completely new new plot
        self.filter.reset(0)
        self.pid.reset()
        prevx = 0
        prevy = HEIGHT
        self.plot.delete(tk.ALL)

        # process variable starts at zero and the
        # setpoint is in the middle of the y axsis,
        # this is the impulse whose response we will plot.
        variable = 0
        setpoint = HEIGHT / 2

        # now run the simulation, iterate over time
        for x in range(0, WIDTH):
            # run the control loop and delay and the correction
            # of the PID controller with a heavy low pass filter
            # to simulate some inertia, delay and filtering
            error = setpoint - variable
            correction = self.pid.calculate(error)
            delayed_effect = self.filter.update(correction)
            variable += delayed_effect

            # plot the process variable
            y = HEIGHT - variable
            self.plot.create_line(prevx, prevy, x, y, fill="#3333ff")
            prevx = x
            prevy = y

        pass


if __name__ == '__main__':
    app = App()

