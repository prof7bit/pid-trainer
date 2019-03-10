#!/usr/bin/env python3

import tkinter as tk
import math

DELAY = 10
WIDTH = 640
HEIGHT = 480

class DelayLine:
    def __init__(self, delay):
        self.delay_steps = delay
        self.buffer = [0] * delay
        self.index = 0

    def delay(self, value):
        self.buffer[self.index] = value
        self.index += 1
        if self.index >= self.delay_steps:
            self.index = 0
        return self.buffer[self.index]

    def init(self, value):
        for i in range(self.delay_steps):
            self.buffer[i] = value


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

    def reset(self):
        self.previous = 0
        self.intergral = 0

    def calculate(self, error):
        p = error * self.kp
        i = self.intergral + error * self.ki
        self.intergral = i
        d = (error - self.previous) * self.kd
        self.previous = error
        return p + i + d


class App:
    def __init__(self):
        self.delay_line = DelayLine(DELAY)
        self.pid = PID()

        self.root = tk.Tk()
        self.slider_p = tk.Scale(self.root, from_=100, to=0, command=self.update)
        self.slider_i = tk.Scale(self.root, from_=100, to=0, command=self.update)
        self.slider_d = tk.Scale(self.root, from_=100, to=0, command=self.update)
        self.plot = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, background="#000000")

        self.plot.grid(row=0, column=0)
        self.slider_p.grid(row=0, column=1)
        self.slider_i.grid(row=0, column=2)
        self.slider_d.grid(row=0, column=3)

        self.update(None)
        self.root.mainloop()


    def update(self, event):
        self.pid.set_params(
            self.slider_p.get() * 0.001,
            self.slider_i.get() * 0.00001,
            self.slider_d.get() * 0.01
        )
        self.plot.delete(tk.ALL)
        prevx = 0
        prevy = HEIGHT
        variable = 0
        self.delay_line.init(0)
        self.pid.reset()
        setpoint = HEIGHT / 2
        amp = HEIGHT / 2
        for x in range(0, WIDTH):
            error = self.delay_line.delay(setpoint - variable)
            variable += self.pid.calculate(error)
            y = HEIGHT - variable
            self.plot.create_line(prevx, prevy, x, y, fill="#3333ff")
            prevx = x
            prevy = y

        pass


if __name__ == '__main__':
    app = App()

