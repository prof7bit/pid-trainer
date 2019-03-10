#!/usr/bin/env python3

import tkinter as tk
import math

DELAY = 10

class DelayLine:
    def __init__(self, delay):
        self.delay = delay
        self.buffer = [0] * delay
        self.index = 0

    def delay(self, value):
        self.buffer[self.index] = value
        self.index += 1
        if self.index >= self.delay:
            self.index = 0
        return self.buffer[self.index]


class PID:
    def __init__(self):
        self.kp = 0
        self.ki = 0
        self.kd = 0
        self.intergral = 0
        self.previous = 0

    def set_params(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def calculate(self, error):
        pass


class App:
    def __init__(self):
        self.cw = 640
        self.ch = 480

        self.delay_line = DelayLine(DELAY)

        self.root = tk.Tk()
        self.slider_p = tk.Scale(self.root, from_=100, to=0, command=self.update)
        self.slider_i = tk.Scale(self.root, from_=100, to=0, command=self.update)
        self.slider_d = tk.Scale(self.root, from_=100, to=0, command=self.update)
        self.plot = tk.Canvas(self.root, width=self.cw, height=self.ch)

        self.plot.grid(row=0, column=0)
        self.slider_p.grid(row=0, column=1)
        self.slider_i.grid(row=0, column=2)
        self.slider_d.grid(row=0, column=3)

        y = int(self.ch / 2)
        self.plot.create_line(0, y, self.cw, y, fill="#476042")

        self.root.mainloop()

    def update(self, event):
        kp = self.slider_p.get()
        ki = self.slider_i.get()
        kd = self.slider_d.get()

        self.plot.delete(tk.ALL)
        prevx = 0
        prevy = 0
        zero = self.ch / 2
        amp = self.ch / 2
        for x in range(0, self.cw):
            y = zero + kp * math.sin(x / (1 + ki))
            self.plot.create_line(prevx, prevy, x, y)
            prevx = x
            prevy = y

        pass


if __name__ == '__main__':
    app = App()

