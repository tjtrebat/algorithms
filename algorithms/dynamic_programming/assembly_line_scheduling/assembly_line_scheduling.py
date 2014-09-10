__author__ = 'Tom'

class AssemblyLineScheduler:
    def __init__(self, line1, line2, num_stations):
        self.num_stations = num_stations
        self.assembly_lines = (line1, line2,)
        self.fastest_time = 0
        self.fastest_line = -1

    def fastest_way(self):
        line1, line2 = self.assembly_lines
        line1.fastest_times[0] = line1.entry_time + line1.stations[0].assembly_time
        line2.fastest_times[0] = line2.entry_time + line2.stations[0].assembly_time
        for j in range(1, self.num_stations):
            f1_prev, f2_prev = line1.fastest_times[j - 1], line2.fastest_times[j - 1]
            t2 = line2.stations[j - 1].transfer_time
            a1 = line1.stations[j].assembly_time
            if f1_prev + a1 <= f2_prev + t2 + a1:
                line1.fastest_times[j] = f1_prev + a1
                line1.fastest_lines[j - 1] = 1
            else:
                line1.fastest_times[j] = f2_prev + t2 + a1
                line1.fastest_lines[j - 1] = 2
            t1 = line1.stations[j - 1].transfer_time
            a2 = line2.stations[j].assembly_time
            if f2_prev + a2 <= f1_prev + t1 + a2:
                line2.fastest_times[j] = f2_prev + a2
                line2.fastest_lines[j - 1] = 2
            else:
                line2.fastest_times[j] = f1_prev + t1 + a2
                line2.fastest_lines[j - 1] = 1
        f1, f2 = (line1.fastest_times[self.num_stations - 1] + line1.exit_time,
                  line2.fastest_times[self.num_stations - 1] + line2.exit_time,)
        if f1 <= f2:
            self.fastest_time = f1
            self.fastest_line = 1
        else:
            self.fastest_time = f2
            self.fastest_line = 2

    def recursive_fastest_way(self, n, line):
        if n == self.num_stations:
            t_line1 = self.recursive_fastest_way(n - 1, 0) + self.assembly_lines[0].exit_time
            t_line2 = self.recursive_fastest_way(n - 1, 1) + self.assembly_lines[1].exit_time
            if t_line1 <= t_line2:
                self.fastest_time = t_line1
                self.fastest_line = 1
            else:
                self.fastest_time = t_line2
                self.fastest_line = 2
            return self.fastest_time
        else:
            if not n:
                fastest_time = self.assembly_lines[line].stations[n].assembly_time + \
                                                             self.assembly_lines[line].entry_time
            else:
                other_line = (line + 1) % len(self.assembly_lines)
                assembly_time = self.assembly_lines[line].stations[n].assembly_time
                t_same_line = self.recursive_fastest_way(n - 1, line) + assembly_time
                t_diff_line = self.recursive_fastest_way(n - 1, other_line) + \
                                        self.assembly_lines[other_line].stations[n - 1].transfer_time + assembly_time
                if t_same_line <= t_diff_line:
                    if n:
                        self.assembly_lines[line].fastest_lines[n - 1] = line + 1
                    fastest_time = t_same_line
                else:
                    if n:
                        self.assembly_lines[line].fastest_lines[n - 1] = other_line + 1
                    fastest_time = t_diff_line
            self.assembly_lines[line].fastest_times[n] = fastest_time
        return self.assembly_lines[line].fastest_times[n]

    def print_stations(self):
        i = self.fastest_line
        print "line %d, station %d" % (i, self.num_stations,)
        for j in range(self.num_stations - 2, -1, -1):
            i = self.assembly_lines[i - 1].fastest_lines[j]
            print "line %d, station %d" % (i, j + 1,)

    def print_stations_in_order(self, j):
        if j == self.num_stations - 1:
            line = self.fastest_line
        else:
            line = self.assembly_lines[self.print_stations_in_order(j + 1) - 1].fastest_lines[j]
        return line

    @classmethod
    def read_assembly_lines(cls, infile):
        lines = infile.read().split("\n")
        a1 = AssemblyLine.read_assembly_line(lines[:3])
        a2 = AssemblyLine.read_assembly_line(lines[3:])
        return AssemblyLineScheduler(a1, a2, len(a1.stations))

    def __str__(self):
        s = ""
        s += "\t%s\n" % str(self.assembly_lines[0])
        s += "%s%s%s\n" % (str(self.assembly_lines[0].entry_time),
                               "\t" * (len(self.assembly_lines[0].stations) + 1),
                                self.assembly_lines[0].exit_time,)
        for station in self.assembly_lines[0].stations:
            if station.transfer_time is not None:
                s += "\t  " + str(station.transfer_time)
        s += "\n"
        for station in self.assembly_lines[1].stations:
            if station.transfer_time is not None:
                s += "\t  " + str(station.transfer_time)
        s += "\n"
        s += "%s%s%s\n" % (str(self.assembly_lines[1].entry_time),
                               "\t" * (len(self.assembly_lines[1].stations) + 1),
                               self.assembly_lines[1].exit_time,)
        s += "\t%s\n" % str(self.assembly_lines[1])
        return s

class AssemblyLine:
    def __init__(self, entry_time, exit_time, stations):
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.stations = stations
        self.fastest_times = [0] * len(stations)
        self.fastest_lines = [-1] * (len(stations) - 1)

    @classmethod
    def read_assembly_line(cls, txt):
        entry_time, exit_time = map(int, txt[0].split(" "))
        stations = []
        transfers = map(int, txt[2].split(" "))
        for i, at in enumerate(map(int, txt[1].split(" "))):
            if i < len(transfers):
                stations.append(Station(at, transfers[i]))
            else:
                stations.append(Station(at))
        return AssemblyLine(entry_time, exit_time, stations)

    def __str__(self):
        s = ""
        for station in self.stations:
            s += "%s\t" % station
        return s

class Station:
    def __init__(self, assembly_time, transfer_time=None):
        self.assembly_time = assembly_time
        self.transfer_time = transfer_time

    def __str__(self):
        return str(self.assembly_time)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Finds the fastest way through a factory')
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('--print-stations', action='store_true', help='print stations')
    args = parser.parse_args()
    als = AssemblyLineScheduler.read_assembly_lines(args.infile)
    als.fastest_way()
    # printing output...
    if args.print_stations:
        # print stations
        for j in range(als.num_stations):
            print "line %d, station %d" % (als.print_stations_in_order(j), j + 1,)
    else:
        # print results
        print als
        # print out fastest times
        f1, f2 = "", ""
        for i in range(als.num_stations):
            f1 += str(als.assembly_lines[0].fastest_times[i]).ljust(10)
            f2 += str(als.assembly_lines[1].fastest_times[i]).ljust(10)
        print "j".ljust(10) + "".join(map(lambda x: str(x).ljust(10), range(1, als.num_stations + 1)))
        print "f1[j]".ljust(10) + f1
        print "f2[j]".ljust(10) + f2
        print "f* = %d\n" % als.fastest_time
        # print out fastest lines
        l1, l2 = "", ""
        for i in range(als.num_stations - 1):
            l1 += str(als.assembly_lines[0].fastest_lines[i]).ljust(10)
            l2 += str(als.assembly_lines[1].fastest_lines[i]).ljust(10)
        print "j".ljust(10) + "".join(map(lambda x: str(x).ljust(10), range(2, als.num_stations + 1)))
        print "l1[j]".ljust(10) + l1
        print "l2[j]".ljust(10) + l2
        print "l* = %d\n" % als.fastest_line