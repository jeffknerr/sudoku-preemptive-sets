"""
sudoku cell class

Jan 2022
J. Knerr
"""


class Cell():
    """one cell in a sudoku puzzle"""

    def __init__(self, row=0, col=0, num=0):
        """constuctor for cell class: default is 0,0,0"""

        self.row = row
        self.col = col
        self.num = num

    def __repr__(self):
        """every class should have a repr"""
        # thanks to Dan Bader for this!
        return "%s(%d, %d, %d)" % (self.__class__.__name__,
                                   self.row, self.col, self.num)

    def getrow(self):
        """getter for row"""
        return self.row

    def getcol(self):
        """getter for col"""
        return self.col

    def getnum(self):
        """getter for num"""
        return self.num

    def setnum(self, num):
        """setter for num"""
        self.num = num

    def __eq__(self, other):
        """allow test of cell1 == cell2"""
        if isinstance(other, Cell):
            return (self.row == other.row) and \
                   (self.col == other.col) and \
                   (self.num == other.num)
        return False


def main():
    """minimal tests for the cell class"""
    cell1 = Cell()
    print("cell1:", cell1)
    row = 2
    col = 3
    num = 5
    cell2 = Cell(row, col, num)
    print("cell2:", cell2)
    assert cell2.getrow() == row
    assert cell2.getcol() == col
    assert cell2.getnum() == num
    cell3 = Cell(row, col, num)
    print("cell3:", cell3)
    print("cell1 equals cell2:", cell1 == cell2)
    print("cell3 equals cell2:", cell3 == cell2)
    print("cell3 equals 5:", cell3 == 5)
    cell3.setnum(8)
    print("cell2:", cell2)
    print("cell3:", cell3)
    print("cell1 equals cell2:", cell1 == cell2)
    print("cell3 equals cell2:", cell3 == cell2)


if __name__ == "__main__":
    main()
