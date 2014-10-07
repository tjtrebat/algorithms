__author__ = 'Tom'

import math
from Tkinter import *
from assembly_line_scheduling import *

class AssemblyLineCanvas:
    def __init__(self, root, als):
        self.root = root
        self.als = als
        self.setup_root()
        self.draw_factory()

    def setup_root(self):
        self.root.title("Assembly-line scheduling")
        self.root.resizable(0, 0)
        # make the width of the canvas dependent upon the assembly line length
        self.canvas = Canvas(self.root, width=250 + 150 * (self.als.num_stations - 1), height=500)
        self.canvas.pack(fill='both', expand='yes')
        self.canvas.configure(bg='white')

    def draw_factory(self):
        for i, assembly_line in enumerate(self.als.assembly_lines):
            # draw lines from entries to first stations
            self.canvas.create_line(50, 150 + 200 * i, 125, 75 + 350 * i)
            # draw arrow
            self.draw_arrow(125, 75 + 350 * i, math.pi / 4 if not i else -math.pi / 4)
            # draw lines from last station to exit
            # make exit station distance from assembly line symmetric with the enter station's distance.
            self.canvas.create_line(
                125 + 150 * (self.als.num_stations - 1),
                75 + 350 * i,
                200 + 150 * (self.als.num_stations - 1),
                150 + 200 * i)
            # draw arrow
            self.draw_arrow(950, 150 + 200 * i, -math.pi / 4 if not i else math.pi / 4)
            # draw entry points
            self.draw_circle(25, 125 + 200 * i, text=str(assembly_line.entry_time))
            for j, station in enumerate(assembly_line.stations):
                if station.transfer_time is not None:
                    # draw transfer lines
                    self.canvas.tag_lower(
                        self.canvas.create_line(125 + 150 * j, 75 + 350 * i, 275 + 150 * j, 75 + 350 * ((i + 1) % 2)))
                    # draw arrows on stations
                    self.draw_arrow(
                        275 + 150 * j,
                        75 + 350 * i,
                        math.atan(float(7) / 3) if not i else -math.atan(float(7) / 3))
                    # draw arrows on transfers
                    self.draw_arrow(
                        179 + 150 * j,
                        300 - 100 * i,
                        math.atan(float(7) / 3) if not i else -math.atan(float(7) / 3))
                    # create lines amongst stations
                    self.canvas.create_line(150 + 150 * j, 75 + 350 * i, 250 + 150 * j, 75 + 350 * i)
                    # create arrow to next station on line
                    self.draw_arrow(275 + 150 * j, 75 + 350 * i, 0)
                    # draw transfer node
                    self.draw_circle(154 + 150 * j, 175 + 100 * i, text=str(station.transfer_time))
                # draw station
                self.draw_circle(100 + 150 * j, 50 + 350 * i, text=str(station))
            # draw exit points
            self.draw_circle(175 + 150 * (self.als.num_stations - 1), 125 + 200 * i, text=str(assembly_line.exit_time))
        self.draw_fastest_way()
        # draw assembly-line bounding rectangles
        # make width of the rectangles proportional to number of stations on the line
        for i in range(2):
            self.canvas.tag_lower(self.canvas.create_rectangle(
                95,
                45 + 350 * i,
                155 + 150 * (self.als.num_stations - 1),
                105 + 350 * i, fill="gray"))

    def draw_circle(self, x, y, text):
        self.canvas.create_oval(x, y, x + 50, y + 50, fill="light grey")
        self.canvas.create_text(x + 25, y + 25, text=text)

    def draw_arrow(self, x, y, r):
        self.canvas.create_polygon(
            # base point
            x - 25 * math.cos(r),
            y + 25 * math.sin(r),
            # top-right point
            x - 25 * math.cos(r) + 10 * math.cos(3 * math.pi / 4 - r),
            y + 25 * math.sin(r) + 10 * math.sin(3 * math.pi / 4 - r),
            # top-left point
            x - 25 * math.cos(r) - 10 * math.cos(r - math.pi / 4),
            y + 25 * math.sin(r) + 10 * math.sin(r - math.pi / 4),
            fill="black"
        )

    def draw_fastest_way(self):
        self.als.fastest_way()
        i = self.als.fastest_line
        self.draw_highlighted_line(
            200 + 150 * (self.als.num_stations - 1),
            150 + 200 * i,
            125 + 150 * (self.als.num_stations - 1),
            75 + 350 * i,
            math.pi / 4 if not i else -math.pi / 4)
        for j in range(self.als.num_stations - 2, -1, -1):
            prev_line = self.als.assembly_lines[i].fastest_lines[j]
            if i != prev_line:
                self.draw_highlighted_line(
                    125 + 150 * (j + 1),
                    75 + 350 * i,
                    125 + 150 * j,
                    75 + 350 * prev_line,
                    math.atan(float(7) / 3) if not prev_line else -math.atan(float(7) / 3))
            else:
                self.draw_highlighted_line(
                    125 + 150 * (j + 1),
                    75 + 350 * i,
                    125 + 150 * j,
                    75 + 350 * prev_line,
                    0)
            if not j:
                self.draw_highlighted_line(
                    125,
                    75 + 350 * prev_line,
                    50,
                    150 + 200 * prev_line,
                    -math.pi / 4 if not prev_line else math.pi / 4)
            i = prev_line

    def draw_highlighted_line(self, x1, y1, x2, y2, r):
        # TODO: Calculate the slope, r, in this method
        self.canvas.tag_lower(
            self.canvas.create_polygon(
                x1 + 5 * math.sqrt(2) * math.cos(math.pi / 2 - r),
                y1 - 5 * math.sqrt(2) * math.sin(math.pi / 2 - r),
                x1 - 5 * math.sqrt(2) * math.cos(math.pi / 2 - r),
                y1 + 5 * math.sqrt(2) * math.sin(math.pi / 2 - r),
                x2 - 5 * math.sqrt(2) * math.cos(math.pi / 2 - r),
                y2 + 5 * math.sqrt(2) * math.sin(math.pi / 2 - r),
                x2 + 5 * math.sqrt(2) * math.cos(math.pi / 2 - r),
                y2 - 5 * math.sqrt(2) * math.sin(math.pi / 2 - r),
                fill="gray20")
        )

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Finds the fastest way through a factory')
    parser.add_argument('infile', type=argparse.FileType('r'))
    args = parser.parse_args()
    assembly_line_1, assembly_line_2 = read_assembly_lines_from_file(args.infile)
    if assembly_line_1 and assembly_line_2 is not None:
        als = AssemblyLineScheduler(assembly_line_1, assembly_line_2)
        root = Tk()
        AssemblyLineCanvas(root, als)
        root.mainloop()
