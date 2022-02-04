"""
PreemptiveSet Set Class

Jan 2022
J. Knerr
"""

import cell
import markup


class PreemptiveSet():
    """preemptive set class for solving sudoku puzzles"""

    def __init__(self, pstype):
        """create a new, empty, preemptive set"""
        # pstype = box, row, or col

        self.size = 0
        self.markups = []
        self.pstype = pstype
        if pstype not in ["box", "row", "col"]:
            raise ValueError("ps type should be box, row, or col")

    def __repr__(self):
        """every class should have a repr"""
        # thanks to Dan Bader for this!
        return "%s()" % (self.__class__.__name__)

    def __str__(self):
        """to pretty-print the preemptive sets"""
        pstr = "size: %d  type: %s\n" % (self.size, self.pstype)
        for mark in self.markups:
            pstr += str(mark) + " "
        return pstr

    def addmarkup(self, markuptoadd):
        """add a markup to the ps"""
        self.markups.append(markuptoadd)
        self.size += 1

    def gettype(self):
        """getter for pstype"""
        return self.pstype

    def getsize(self):
        """getter for size"""
        return self.size

    def getmarkups(self):
        """getter for markups"""
        return self.markups

    def getnums(self):
        """get all numbers in the preemptive set"""
        nums = []
        for mark in self.markups:
            nums += mark.getnums()
        return list(set(nums))

    def __eq__(self, other):
        """allow test of ps1 == ps2"""
        if isinstance(other, PreemptiveSet):
            if self.size == other.size and self.pstype == other.pstype:
                # if size is same, and all cells are same
                # assume markups are the same????
                for mark in self.markups:
                    if mark not in other.markups:
                        return False
                return True
        return False


def main():
    """minimal tests for the preemptive set class"""
    ps1 = PreemptiveSet("box")
    print("ps1:", ps1)
    cell1 = cell.Cell(2, 3, 0)
    mark1 = markup.Markup(0, cell1, None)
    mark1.addnum(3)
    mark1.addnum(6)
    mark1.addnum(7)
    ps1.addmarkup(mark1)
    cell2 = cell.Cell(2, 4, 0)
    mark2 = markup.Markup(0, cell2, None)
    mark2.addnum(6)
    mark2.addnum(7)
    ps1.addmarkup(mark2)
    cell3 = cell.Cell(2, 8, 0)
    mark3 = markup.Markup(0, cell3, None)
    mark3.addnum(3)
    mark3.addnum(7)
    ps1.addmarkup(mark3)
    print("ps1:", ps1)
    # test if same preemptive set
    ps2 = PreemptiveSet("row")
    ps2.addmarkup(mark2)
    ps2.addmarkup(mark3)
    ps2.addmarkup(mark1)
    print("ps2:", ps2)
    print("ps1 same as ps2:", ps1 == ps2)
    ps3 = PreemptiveSet("box")
    mark1.addnum(5)
    ps3.addmarkup(mark2)
    ps3.addmarkup(mark3)
    ps3.addmarkup(mark1)
    print("ps3:", ps3)
    print("ps1:", ps1)
    print("ps1 same as ps3:", ps1 == ps3)


if __name__ == "__main__":
    main()
