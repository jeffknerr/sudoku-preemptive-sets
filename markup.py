"""
sudoku markup class

Jan 2022
J. Knerr
"""

import cell


class Markup():
    """one cell's markup in a sudoku puzzle"""

    def __init__(self, size=0, mycell=None, nums=None):
        """constuctor for cell markup class: default is 0,None,None"""

        self.size = size
        self.mycell = mycell
        if nums is None:
            self.nums = []
        else:
            if isinstance(nums, list):
                # nums that could be in this cell
                self.nums = nums
            else:
                self.nums = []

    def __repr__(self):
        """every class should have a repr"""
        # thanks to Dan Bader for this!
        return "%s()" % (self.__class__.__name__)

    def __str__(self):
        """pretty-print the cell markup"""
        mstr = ""
        if self.mycell is not None:
            mstr = "(%d,%d): " % (self.mycell.getrow(), self.mycell.getcol())
        for num in self.nums:
            mstr += str(num)
        return mstr

    def getsize(self):
        """getter for size of markup"""
        return self.size

    def __len__(self):
        return self.size

    def getrow(self):
        """getter for cell row"""
        return self.mycell.getrow()

    def getcol(self):
        """getter for cell col"""
        return self.mycell.getcol()

    def getcellnum(self):
        """getter for cell number"""
        # should be a zero if self.nums is not empty
        return self.mycell.getnum()

    def getnums(self):
        """getter for markup numbers"""
        return self.nums

    def setsize(self, size):
        """setter for size"""
        self.size = size

    def setcell(self, mycell):
        """setter for mycell"""
        self.mycell = mycell

    def setnums(self, nums):
        """setter for nums"""
        self.nums = nums

    def addnum(self, num):
        """add a number to the markup"""
        if isinstance(num, int):
            if num not in self.nums:
                if 1 <= num <= 9:
                    self.size += 1
                    self.nums.append(num)
                    self.nums.sort()
        else:
            print("Can only add integers to the markup...")

    def rmnum(self, num):
        """remove a number from the markup"""
        if isinstance(num, int):
            if num in self.nums:
                self.size -= 1
                self.nums.remove(num)
        else:
            print("Can only remove integers from the markup...")

    def single(self):
        """return True if markup is singleton"""
        return len(self.nums) == 1

    def __eq__(self, other):
        """allow test of mark1 == mark2"""
        if isinstance(other, Markup):
            if self.size == other.size:
                # if size is same, cell same, and all nums are same
                if self.mycell == other.mycell:
                    for num in self.nums:
                        if num not in other.nums:
                            return False
                    return True
                return False
            return False
        return False


def main():
    """minimal tests for the cell markup class"""
    row = 2
    col = 3
    num = 0
    cell1 = cell.Cell(row, col, num)
    print("cell1:", cell1)
    mark1 = Markup()
    mark1.addnum(4)
    mark1.addnum(2)
    mark1.addnum(6)
    mark1.addnum(2)
    mark1.addnum(10)
    mark1.rmnum(10)
    mark1.setcell(cell1)
    mark1.addnum('hello')
    print(mark1)
    mark1.addnum(3)
    print(mark1)
    mark1.rmnum(4)
    print(mark1)
    print("markup 1 is singleton:", mark1.single())
    mark2 = Markup(0, cell1, None)
    mark2.addnum(8)
    print(mark2)
    print("markup 2 is singleton:", mark2.single())
    print("markup1 == markup2:", mark2 == mark1)
    mark3 = Markup()
    mark3.addnum(3)
    mark3.addnum(2)
    mark3.addnum(6)
    mark3.setcell(cell1)
    print(mark3)
    print("markup1 == markup3:", mark3 == mark1)


if __name__ == "__main__":
    main()
