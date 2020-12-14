import tkinter as tk

from algorithms.primitives import line_segment_from_coordinates, Point
from algorithms import PointsPolygonChecker

# TODO: create Polygon class

class ObjectsHandler:
    drawed_objects = []
    polygon_points = []
    z_point = None
    points_polygon_checker = None

    def __init__(self, canvas, answer_label):
        self.canvas = canvas
        self.answer_label = answer_label

    def clean(self, event=None):
        for obj_id in self.drawed_objects:
            self.canvas.after(1, self.canvas.delete, obj_id)
        self.drawed_objects = []
        self.polygon_points = []
        self.z_point = None
        self.points_polygon_checker = None

    def add_point_to_polygon(self, event):
        if self.points_polygon_checker:
            return
        point = Point(event.x, event.y)
        self.plot_point(point, radius=2)
        if len(self.polygon_points):
            self.answer_label['text'] = ''
            prev_point = self.polygon_points[-1]
            self.plot_line(point, prev_point)
        self.polygon_points.append(point)

    def plot_z_point(self, event):
        if self.z_point:
            self.plot_point(self.z_point, color='white', radius=3)
        point = Point(event.x, event.y)
        self.z_point = point
        self.plot_point(point, color="green", radius=3)

    def finish_polygon_plot(self, event):
        if len(self.polygon_points) >= 3:
            self.plot_line(self.polygon_points[0], self.polygon_points[-1])
            self.points_polygon_checker = PointsPolygonChecker(self.polygon_points)
        else:
            self.answer_label['text'] = "Failed to finish two points polygon"
            self.clean()

    def check_z_point_location(self):
        if self.points_polygon_checker(self.z_point):
            self.answer_label['text'] = "Point belongs to the polygon"
        else:
            self.answer_label['text'] = "Point outside of the polygon"

    def right_button_handler(self, event):
        self.finish_polygon_plot(event)
        self.plot_z_point(event)
        self.check_z_point_location()

    def plot_line(self, point_1, point_2, color='black'):
        line_id = self.canvas.create_line(
            point_1.x, point_1.y, point_2.x, point_2.y,
            fill=color)
        self.drawed_objects.append(line_id)
        return line_id

    def plot_point(self, point, radius=1, color='black'):
        x, y = int(point.x), int(point.y)
        x1, y1 = (x - radius), (y - radius)
        x2, y2 = (x + radius), (y + radius)
        point_id = self.canvas.create_oval(x1, y1, x2, y2, fill=color)
        self.drawed_objects.append(point_id)
        return point_id


# initialize main window
window = tk.Tk()
window.title("Point belongs to a polygon check")
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
canvas.bind('<ButtonPress-1>', handler.add_point_to_polygon)
canvas.bind('<ButtonPress-2>', handler.right_button_handler)


if __name__ == '__main__':
    window.mainloop()
