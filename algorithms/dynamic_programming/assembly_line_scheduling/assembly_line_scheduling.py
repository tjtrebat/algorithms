"""
Solves the assembly-line scheduling problem for determining the fastest way through a factory.
"""

__author__ = 'Tom'

class AssemblyLineScheduler:
    def __init__(self, line1, line2):
        """ Constructs an AssemblyLineScheduler.

        Attributes:
            line1 -- the first line
            line2 -- the second line
            num_stations -- the number of stations on a line
        """
        self.assembly_lines = (line1, line2,)
        self.num_stations = len(line1.stations)

    def fastest_way(self):
        """ Find the fastest way through a factory using dynamic programming techniques.
        """
        # calculate the fastest time to the first station on each line
        for line in self.assembly_lines:
            line.fastest_times[0] = line.stations[0].assembly_time + line.entry_time
        for j in range(1, self.num_stations):
            for i, line in enumerate(self.assembly_lines):
                station = line.stations[j]
                other_line = self.assembly_lines[(i + 1) % 2]
                # get fastest time from previous station on the same line
                line_time = line.fastest_times[j - 1] + station.assembly_time
                # get fastest time from previous station on the other line plus the transfer time
                other_line_time = (other_line.fastest_times[j - 1] + other_line.stations[j - 1].transfer_time
                                   + station.assembly_time)
                # assign the smaller of the two times to the station's fastest time
                if line_time <= other_line_time:
                    line.fastest_times[j] = line_time
                    line.fastest_lines[j - 1] = i
                else:
                    line.fastest_times[j] = other_line_time
                    line.fastest_lines[j - 1] = (i + 1) % 2
        # set self.fastest_time to the fastest time upon exiting the line
        self.fastest_time = float("inf")
        for i, line in enumerate(self.assembly_lines):
            finishing_time = line.fastest_times[self.num_stations - 1] + line.exit_time
            if finishing_time < self.fastest_time:
                self.fastest_time = finishing_time
                self.fastest_line = i

    def fastest_way_recursive(self):
        """ A wrapper function for a recursive method used to solve the assembly-line scheduling problem.
        """
        # calculate the fastest time to the first station on each line
        for line in self.assembly_lines:
            line.fastest_times[0] = line.stations[0].assembly_time + line.entry_time
        # set self.fastest_time to the fastest time upon exiting the line
        self.fastest_time = float("inf")
        for i, line in enumerate(self.assembly_lines):
            finishing_time = self._fastest_way_recursive(self.num_stations - 1, line, i) + line.exit_time
            if finishing_time < self.fastest_time:
                self.fastest_time = finishing_time
                self.fastest_line = i

    def _fastest_way_recursive(self, n, line, i):
        """ A recursive method called in fastest_way_recursive.
        """
        if n > 0:
            station = line.stations[n]
            other_line = self.assembly_lines[(i + 1) % 2]
            line_time = self._fastest_way_recursive(n - 1, line, i) + station.assembly_time
            other_line_time = (self._fastest_way_recursive(n - 1, other_line, (i + 1) % 2)
                           + other_line.stations[n - 1].transfer_time + station.assembly_time)
            if line_time <= other_line_time:
                line.fastest_times[n] = line_time
                line.fastest_lines[n - 1] = i
            else:
                line.fastest_times[n] = other_line_time
                line.fastest_lines[n - 1] = (i + 1) % 2
        return line.fastest_times[n]

    def print_stations(self):
        """ Prints the fastest way through the factory.
        """
        i = self.fastest_line
        print "line %d, station %d" % (i + 1, self.num_stations,)
        for j in range(self.num_stations - 2, -1, -1):
            i = self.assembly_lines[i - 1].fastest_lines[j]
            print "line %d, station %d" % (i + 1, j + 1,)

    def print_stations_in_order(self):
        """ Prints the fastest way through the factory in order.
        """
        for i in range(self.num_stations):
            line = self.fastest_line
            for j in range(self.num_stations - 2, i - 1, -1):
                line = self.assembly_lines[line].fastest_lines[j]
            print "line %d, station %d" % (line + 1, i + 1,)

    def __str__(self):
        """ A string representation of the assembly-line scheduling problem.
        """
        # print out fastest times
        station_numbers = lambda start: "j".ljust(9) + "".join(
            map(lambda x: str(x).ljust(10), range(start, als.num_stations + 1)))
        s = station_numbers(1) + "\n"
        for i, line in enumerate(als.assembly_lines):
            fastest_times = "f%d[j]".ljust(10) % (i + 1)
            for j in range(als.num_stations):
                fastest_times += str(line.fastest_times[j]).ljust(10)
            s += fastest_times + "\n"
        s += "f* = %d\n" % als.fastest_time + "\n"
        # print out fastest lines
        s += station_numbers(2) + "\n"
        for i, line in enumerate(als.assembly_lines):
            fastest_lines = "l%d[j]".ljust(10) % (i + 1)
            for j in range(als.num_stations - 1):
                fastest_lines += str(line.fastest_lines[j] + 1).ljust(10)
            s += fastest_lines + "\n"
        s += "l* = %d\n" % (als.fastest_line + 1)
        return s

class AssemblyLine:
    """ Represents an assembly line in a factory.
    """
    def __init__(self, entry_time, exit_time, stations):
        """Contructs an AssemblyLine.

        Attributes:

            entry_time -- an entry time
            exit_time -- an exit time
            stations -- a list of stations
        """
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.stations = stations
        self.fastest_times = [0] * len(stations)
        self.fastest_lines = [-1] * (len(stations) - 1)

    def __str__(self):
        """ A string representation of the AssemblyLine.
        """
        s = ""
        for station in self.stations:
            s += "%s\t" % station
        return s

class Station:
    """ An object used to denote a station on an AssemblyLine.
    """
    def __init__(self, assembly_time, transfer_time=None):
        """ Construct a Station.

        Attributes:
            assembly_time -- the assembly time
            transfer_time -- the transfer time to the next station on separate line
        """
        self.assembly_time = assembly_time
        self.transfer_time = transfer_time

    def __str__(self):
        """ The string representation of this station.
        """
        return str(self.assembly_time)

def read_assembly_lines_from_file(infile):
    """ Reads a file containing assembly line data. Format of the file is specified as follows. Assuming an assembly
    line with k stations, containing k - 1 transfers to stations on a separate line. Each line of data designates an
    individual assembly line. The first number represents the entry time to the line, and is followed by successive
    pairs of assembly and transfer times for each station in order of their arrival, i.e.:

        <entry_time> <assembly_time_1> <transfer_time_1> ... <assembly_time_k> <transfer_time_k> <exit_time>
    """
    txt = infile.read()
    if txt:
        lines = txt.split("\n")
        if len(lines) > 1:
            assembly_line_1 = read_assembly_line_from_txt(lines[0])
            assembly_line_2 = read_assembly_line_from_txt(lines[1])
            if len(assembly_line_1.stations) == len(assembly_line_2.stations):
                return assembly_line_1, assembly_line_2

def read_assembly_line_from_txt(txt_line):
    """ Reads a line of text representing an individual assembly line.
    """
    arr_line = map(int, txt_line.split())
    if len(arr_line) > 1:
        entry_time, exit_time, stations = -1, -1, []
        i = 0
        while i < len(arr_line):
            if not i:
                entry_time = arr_line[i]
            elif len(arr_line) <= i + 1:
                exit_time = arr_line[i]
            elif len(arr_line) > i:
                if len(arr_line) <= i + 2:
                    stations.append(Station(arr_line[i]))
                else:
                    stations.append(Station(arr_line[i], arr_line[i + 1]))
                    i += 1
            i += 1
        return AssemblyLine(entry_time, exit_time, stations)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Finds the fastest way through a factory')
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('--recursive', action='store_true', help='use a recursive method to solve')
    args = parser.parse_args()
    assembly_lines = read_assembly_lines_from_file(args.infile)
    if assembly_lines is not None:
        als = AssemblyLineScheduler(*assembly_lines)
        if args.recursive:
            als.fastest_way_recursive()
        else:
            als.fastest_way()
        als.print_stations_in_order()
