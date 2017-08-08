#!/usr/bin/python
# -*- coding: utf-8
#
# Copyright 2017 Mick Phillips (mick.phillips@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Display a window that allows the user to select a circular area."""
import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = Canvas(self, width=400, height=400)
        self.canvas.grid()

        self.btn_quit = tk.Button(self, text="Quit", command=self.quit)
        self.btn_quit.grid()


class Canvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.bind("<Button-1>", self.on_click)
        self.bind("<Button-3>", self.on_click)
        self.bind("<B1-Motion>", self.circle_resize)
        self.bind("<B3-Motion>", self.circle_drag)
        self.bind("<ButtonRelease>", self.on_release)
        self.circle = None
        self.p_click = None
        self.bbox_click = None

    def on_release(self, event):
        self.p_click = None
        self.bbox_click = None

    def on_click(self, event):
        if self.circle == None:
            self.circle = self .create_oval((event.x-1, event.y-1, event.x+1, event.y+1))

    def circle_resize(self, event):
        if self.circle is None:
            return
        if self.p_click is None:
            self.p_click = (event.x, event.y)
            self.bbox_click = self.bbox(self.circle)
            return
        bbox = self.bbox(self.circle)
        centre = ((bbox[2] + bbox[0])/2, (bbox[3] + bbox[1])/2)
        r0 = ((self.p_click[0] - centre[0])**2 + (self.p_click[1] - centre[1])**2)**0.5
        r1 = ((event.x - centre[0])**2 + (event.y - centre[1])**2)**0.5
        scale = r1 / r0
        self.scale(self.circle, centre[0], centre[1], scale, scale)
        self.p_click= (event.x, event.y)

    def circle_drag(self, event):
        if self.circle is None:
            return
        if self.p_click is None:
            self.p_click = (event.x, event.y)
            return
        self.move(self.circle,
                  event.x - self.p_click[0],
                  event.y - self.p_click[1])
        self.p_click = (event.x, event.y)
        self.update()


if __name__ == '__main__':
    app = App()
    app.master.title('Select a circle.')
    app.mainloop()