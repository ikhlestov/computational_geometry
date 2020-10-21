import tkinter as tk

from algorithms.primitives import line_segment_from_coordinates
from algorithms import lines_segment_intersection_point


class LinesDB:
    def __init__(self):
        self.lines = {}
        self.idx_to_line_id = {}
        self.line_id_to_idx = {}
        self.finished_lines = 0

    def add(self, line_id, x_start, y_start, x_end, y_end):
        self.lines[line_id] = {'start': [x_start, y_start], 'end': [x_end, y_end]}
        line_idx = len(self.lines) - 1
        self.idx_to_line_id[line_idx] = line_id
        self.line_id_to_idx[line_id] = line_idx

    def remove(self, line_id):
        line_idx = self.line_id_to_idx.pop(line_id)
        self.idx_to_line_id.pop(line_idx)
        self.lines.pop(line_id)

    def line_by_idx(self, line_idx):
        line_id = self.idx_to_line_id[line_idx]
        line_data = self.lines[line_id]
        return line_segment_from_coordinates(*line_data['start'], *line_data['end'])

    def __len__(self):
        return len(self.lines)

def plot_point(x, y, radius=1):
    python_green = "#476042"
    x, y = int(x), int(y)
    x1, y1 = (x - radius), (y - radius)
    x2, y2 = (x + radius), (y + radius)
    return canvas.create_oval(x1, y1, x2, y2, fill=python_green)


def reset_line():
    canvas.start_coordinates = None
    canvas.prev_line_id = None


def draw_line(event):
    if canvas.lines_db.finished_lines == 2:
        return

    line_idx = canvas.lines_db.finished_lines
    
    if str(event.type) == 'ButtonPress':
        canvas.start_coordinates = event.x, event.y
        canvas.lines_widgets[line_idx]['startx'].insert(0, event.x)
        canvas.lines_widgets[line_idx]['starty'].insert(0, event.y)

    x_start, y_start = canvas.start_coordinates
    x_end, y_end = event.x, event.y
    canvas.lines_widgets[line_idx]['endx'].delete(0, tk.END)
    canvas.lines_widgets[line_idx]['endx'].insert(0, x_end)
    canvas.lines_widgets[line_idx]['endy'].delete(0, tk.END)
    canvas.lines_widgets[line_idx]['endy'].insert(0, y_end)
    if canvas.prev_line_id:
        canvas.after(1, canvas.delete, canvas.prev_line_id)
        canvas.lines_db.remove(canvas.prev_line_id)
    line_id = canvas.create_line(x_start, y_start, x_end, y_end, fill='black')
    canvas.lines_db.add(line_id, x_start, y_start, x_end, y_end)
    canvas.prev_line_id = line_id

    if len(canvas.lines_db) == 2:
        try:
            if canvas.intersection_point:
                canvas.after(1, canvas.delete, canvas.intersection_point)
            
            intersection = lines_segment_intersection_point(
                canvas.lines_db.line_by_idx(0),
                canvas.lines_db.line_by_idx(1),
            )
            if intersection:
                intersection_data['text'] = '%.1f; %.1f' % intersection
                canvas.intersection_point = plot_point(*intersection, radius=5)
            else:
                intersection_data['text'] = 'None'
                canvas.intersection_point = None
        except ValueError:
            pass

    if str(event.type) == 'ButtonRelease':
        reset_line()
        canvas.lines_db.finished_lines += 1

def clean(event):
    line_ids = canvas.lines_db.lines.keys()
    for line_id in line_ids:
        canvas.after(1, canvas.delete, line_id)
    canvas.lines_db = LinesDB()
    for entry_field in canvas.lines_widgets:
        for coord_name in entry_field:
            entry_field[coord_name].delete(0, tk.END)
    intersection_data['text'] = 'None'


window = tk.Tk()

window.title("Lines Segments Intersection")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

canvas = tk.Canvas(window, bg='white')

# Control frames population
controls_frame = tk.Frame(window)
btn_clean = tk.Button(controls_frame, text="Clean Canvas")
btn_clean.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
lines_frame = tk.Frame(controls_frame)
lines_frame.grid(row=1, column=0, sticky="ew", padx=5)

lines_widgets = []
row_idx = 0
for idx in range(2):
    row_idx += 1
    line_header = tk.Label(lines_frame, text="Line %d" % (idx + 1))
    line_header.grid(row=row_idx, column=0, sticky="e", padx=5)

    line_coords_widgets = {}
    for level in ['start', 'end']:
        row_idx += 1
        level_header = tk.Label(lines_frame, text=level)
        level_header.grid(row=row_idx, column=0, sticky="e", padx=2)
        for col_idx, coord_name in enumerate(['x', 'y']):
            coord_header = tk.Label(lines_frame, text=coord_name + ':')
            coord_header.grid(row=row_idx, column=1 + col_idx, sticky="e", padx=2)
            line_entry = tk.Entry(lines_frame)
            line_entry.grid(row=row_idx, column=2 + col_idx * 2, sticky="e", padx=2)
            line_coords_widgets[level + coord_name] = line_entry
    lines_widgets.append(line_coords_widgets)
intersection_header = tk.Label(lines_frame, text="Intersection:")
intersection_header.grid(row=row_idx+1, column=1, sticky="w", padx=5)
intersection_data = tk.Label(lines_frame, text="None")
intersection_data.grid(row=row_idx+1, column=2, sticky="w", padx=5)

controls_frame.grid(row=0, column=0, sticky="ns")
canvas.grid(row=0, column=1, sticky="nsew")

canvas.lines_db = LinesDB()
canvas.lines_widgets = lines_widgets
canvas.intersection_point = None
reset_line()

# Events handlers
canvas.bind('<ButtonPress-1>', draw_line)
canvas.bind('<ButtonRelease-1>', draw_line)
canvas.bind('<B1-Motion>', draw_line)
btn_clean.bind("<Button-1>", clean)


if __name__ == '__main__':
    window.mainloop()
