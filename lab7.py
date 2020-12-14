import tkinter as tk

from algorithms.primitives import Point
from algorithms.convex_hull import graham as graham_ch


class ObjectsHandler:
    drawed_objects = []
    ploted_points = []
    
    def __init__(self, canvas, answer_label):
        self.canvas = canvas
        self.answer_label = answer_label

    def plot_point_event(self, event):
        self.plot_point(event, color='black', radius=3)
        self.ploted_points.append(Point(event.x, event.y))

    def plot_point(self, point, radius=1, color='black'):
        x, y = int(point.x), int(point.y)
        x1, y1 = (x - radius), (y - radius)
        x2, y2 = (x + radius), (y + radius)
        point_id = self.canvas.create_oval(x1, y1, x2, y2, fill=color)
        self.drawed_objects.append(point_id)
        self.answer_label['text'] = ''
        return point_id

    def build_convex_hull_event(self, event):
        if len(self.ploted_points) <= 2:
            self.answer_label['text'] = "Failed to build convex hull with less than 3 points"
        convex_hull_points_pairs = graham_ch(self.ploted_points)
        for pair in convex_hull_points_pairs:
            self.plot_line(pair[0], pair[1])

    def plot_line(self, point_1, point_2, color='black'):
        line_id = self.canvas.create_line(
            point_1.x, point_1.y, point_2.x, point_2.y,
            fill=color)
        self.drawed_objects.append(line_id)
        return line_id

    def clean(self, event=None):
        for obj_id in self.drawed_objects:
            self.canvas.after(1, self.canvas.delete, obj_id)
        self.drawed_objects = []
        self.ploted_points = []
        self.answer_label['text'] = ''


# initialize main window
window = tk.Tk()
window.title("Convex hull")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

## build sidebar
sidebar = tk.Frame(window)
sidebar.grid(row=0, column=0, sticky="ns")

### prepare controls and info fields
controls = tk.Frame(sidebar,)# relief=tk.RAISED, borderwidth=1)
controls.pack(pady=5)
infos = tk.Frame(sidebar, )#relief=tk.RAISED, borderwidth=1)
infos.pack(pady=5)

#### Populate controls
btn_clean = tk.Button(controls, text="Clean Canvas")
btn_clean.pack()

btn_help = tk.Button(controls, text="Help")
btn_help.pack()

#### Populate infos
answer_label = tk.Label(infos, text="")
answer_label.pack()

## build canvas
canvas = tk.Canvas(window, bg='white')
canvas.grid(row=0, column=1, sticky="nsew")
handler = ObjectsHandler(canvas=canvas, answer_label=answer_label)

# define bindings
btn_clean.bind("<Button-1>", handler.clean)
canvas.bind('<ButtonPress-1>', handler.plot_point_event)
canvas.bind('<ButtonPress-2>', handler.build_convex_hull_event)


if __name__ == '__main__':
    window.mainloop()
