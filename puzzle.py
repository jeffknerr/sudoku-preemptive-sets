"""
Sudoku Puzzle Class

Includes methods to solve the puzzle:
    - find forced numbers
    - mark up the puzzle
    - find preemptive sets
    - solve using preemptive sets

J. Knerr
Jan 2020
"""

import numpy as np
import cell
import markup
import preemptiveset


class Puzzle():
    """sudoku puzzle class"""

    def __init__(self):
        """create empty sudoku puzzle"""
        self.puzzle = np.zeros((9, 9), dtype=cell.Cell)
        self.markups = []    # all markups in the puzzle
        self.pss = []        # preemptive sets

    def setnums(self, nums):
        """given np.array of nums, create 9x9 puzzle of cells"""
        for row in range(9):
            for col in range(9):
                self.puzzle[row, col] = cell.Cell(row, col, nums[row, col])

    def __str__(self):
        """pretty-print the puzzle"""
        ncols = 19
        pstr = "-"*ncols + "\n"
        for row in range(9):
            strrow = "|"
            for col in range(9):
                divider = ":"
                if col in (2, 5):
                    divider = "|"
                number = self.puzzle[row, col].getnum()
                if number == 0:
                    char = " " + divider
                else:
                    char = str(number) + divider
                strrow += char
            pstr += strrow + "\n"
            if row in (2, 5):
                pstr += "-"*ncols + "\n"
        pstr += "-"*ncols + "\n"
        return pstr

    def filtermarkups(self):
        """use the preemptive sets to filter numbers out of the markups"""
        # e.g., if you have 126 in a preemptive box set, then you
        # can remove 1s 2s and 6s from the *other* markups in that box.
        # after this step, see if you have any singletons
        for preset in self.pss:
            # get the markups in this pss
            psmarkups = preset.getmarkups()
            # get all markups in this row, col, or box
            row = psmarkups[0].getrow()
            col = psmarkups[0].getcol()
            ptype = preset.gettype()
            if ptype == "row":
                # get all row markups
                marks = self._getrowmarkups(row, col)
            elif ptype == "col":
                # get all col markups
                marks = self._getcolmarkups(row, col)
            else:
                # get all box markups
                marks = self._getboxmarkups(row, col)
            # now remove the pss markups, since we don't want
            # to filter the numbers from themselves
            self._rmmarks(psmarkups, marks)
            # numbers in this preemptive set
            nums = preset.getnums()
            # now filter the numbers from the non-pss markups
            for num in nums:
                for mark in marks:
                    mark.rmnum(num)

    def _rmmarks(self, psmarkups, marks):
        """remove the pss markups from the row/col/box markups"""
        for m in psmarkups:
            if m in marks:
                marks.remove(m)

    def findpss(self):
        """find preemptive sets"""
        for i in range(len(self.markups)):
            row = (i//9)
            col = (i - (row*9))
            n = len(self.markups[i])
            if n > 0:
                if n == 1:
                    print("singleton!!", self.markups[i], row, col)
                    num = self.markups[i].getnums()[0]
                    # set number in puzzle cell
                    self.puzzle[row, col].setnum(num)
                    # remove number from this markup
                    self.markups[i].rmnum(num)
                    # fix/check other markups in this box, row, col
                    marks = self._getrowmarkups(row, col)
                    marks += self._getcolmarkups(row, col)
                    marks += self._getboxmarkups(row, col)
                    for m in marks:
                        m.rmnum(num)
                else:
                    # print("check row for PS")
                    self._checkforpresets(self._getrowmarkups, i, n, row, col, "row")
                    self._checkforpresets(self._getcolmarkups, i, n, row, col, "col")
                    self._checkforpresets(self._getboxmarkups, i, n, row, col, "box")

    def _checkforpresets(self, markupsfunction, i, n, row, col, pstype):
        """helper to get preemptive sets for this row/col/box"""
        count = 0
        markset = set(self.markups[i].getnums())
        marks = markupsfunction(row, col)
        pset = preemptiveset.PreemptiveSet(pstype)
        for m in marks:
            if m != self.markups[i]:
                if len(m) <= n:
                    if set(m.getnums()).issubset(markset):
                        pset.addmarkup(m)
                        count += 1
        if count == n-1:
            # add self
            pset.addmarkup(self.markups[i])
            # and save (if not already in)
            if pset not in self.pss:
                self.pss.append(pset)
                self.pss.sort(key=lambda x: x.size)
        # ignore pss if size == number of non-empty markups in this row/col/box???

    def _getboxmarkups(self, row, col):
        """return all non-zero markup arrays for this box, but not myself"""
        boxrow = (row)//3
        boxcol = (col)//3
        boxnum = boxrow * 3 + (boxcol + 1)
        markups = []
        start = (((boxnum - 1) // 3) * 27) + (((boxnum - 1) % 3) * 3)
        indices = list(range(start, start+3)) \
            + list(range(start+9, start+9+3)) \
            + list(range(start+18, start+18+3))
    #   print(boxnum, row, col, start, indices)
        for i in indices:
            if len(self.markups[i]) > 0:
                markups.append(self.markups[i])
        return markups

    def _getrowmarkups(self, row, col):
        """return all non-zero markup arrays for this row, but not myself"""
        markups = []
        for i in range(row*9, row*9 + 9):
            if len(self.markups[i]) > 0:
                if i % ((row+1)*9) != col:
                    markups.append(self.markups[i])
        return markups

    def _getcolmarkups(self, row, col):
        """return all non-zero markup arrays for this column, but not myself"""
        markups = []
        column = col % 9
        indices = range(column, 81, 9)
        for i in indices:
            if len(self.markups[i]) > 0:
                if (i//9) != row:
                    markups.append(self.markups[i])
        return markups

    def mark(self):
        """create the markups for this puzzle"""
        # for each cell: rm #s in row, col, box
        for row in range(9):
            for col in range(9):
                newmarkup = markup.Markup()
                newmarkup.setcell(self.puzzle[row, col])
                if self.puzzle[row, col].getnum() == 0:
                    rowcells = self.puzzle[row]
                    colcells = self.puzzle[:, col]
                    rownums = []
                    for rcell in rowcells:
                        rownums.append(rcell.getnum())
                    colnums = []
                    for ccell in colcells:
                        colnums.append(ccell.getnum())
                    boxrow = (row)//3
                    boxcol = (col)//3
                    boxnum = boxrow * 3 + (boxcol)
                    boxnums = self._getboxnums(boxnum)
                    for i in range(1, 10):
                        if i not in rownums:
                            if i not in colnums:
                                if i not in boxnums:
                                    newmarkup.addnum(i)
                self.markups.append(newmarkup)

    def showpreemptivesets(self):
        """pretty-print the preemptive sets"""
        print("current preemptive sets:")
        for pss in self.pss:
            print(pss)

    def showmarkup(self):
        """pretty-print the markup"""
        ndash = 100
        for row in range(9):
            if row % 3 == 0:
                print("-" * ndash)
            rowstr = ""
            for col in range(9):
                nums = self.markups[(9*row)+col].getnums()
                arraystr = str(nums)
                arraystr = arraystr.replace(", ", "")
                rowstr += "%10s" % arraystr
                if (col+1) % 3 == 0:
                    rowstr += " ||"
            print(rowstr)
        print("-" * ndash)

    def findforced(self):
        """find and fill in all 'forced' numbers (the easy ones)"""
        numchanged = 0
        for num in range(1, 10):  # actual num in puzzle, so 1-9
            print("finding forced numbers...looking for %ds" % (num))
            # check each box
            for box in range(9):
                boxnums = self._getboxnums(box)
                if num not in boxnums:
                    # find all possible positions num could be
                    # possible = cells with 0's in them, in this box
                    possible = self._emptypositions(box)
                    if len(possible) == 0:
                        error = "uh oh..%d not in box (%d)" % (num, box+1)
                        error += ", but no empty cells???"
                        print(error)
                    # now check rows and cols,
                    # delete from possible if num found
                    pcopy = possible[:]
                    for row, col in pcopy:
                        rowcells = self.puzzle[row]
                        colcells = self.puzzle[:, col]
                        rownums = []
                        for rcell in rowcells:
                            rownums.append(rcell.getnum())
                        colnums = []
                        for ccell in colcells:
                            colnums.append(ccell.getnum())
                        if num in rownums:
                            possible.remove((row, col))
                        elif num in colnums:
                            possible.remove((row, col))
                    # if only 1 possible left, put num in that cell
                    if len(possible) == 1:
                        numchanged += 1
                        print("FOUND: %d in %s" % (num, possible[0]))
                        self.puzzle[possible[0][0], possible[0][1]].setnum(num)
        return numchanged

    def solved(self):
        """return True if puzzle is solved"""
        for boxnum in range(9):
            empties = self._emptypositions(boxnum)
            if len(empties) > 0:
                return False
        # if no empty positions left...
        return True

    def _emptypositions(self, boxnum):
        """return list of empty positions in this box"""
        posns = []
        if boxnum < 3:
            rows = [0, 1, 2]
        elif boxnum < 6:
            rows = [3, 4, 5]
        else:
            rows = [6, 7, 8]
        if boxnum in [0, 3, 6]:
            cols = [0, 1, 2]
        elif boxnum in [1, 4, 7]:
            cols = [3, 4, 5]
        else:
            cols = [6, 7, 8]
        for row in rows:
            for col in cols:
                if self.puzzle[row, col].getnum() == 0:
                    posns.append((row, col))
        return posns

    def _getboxnums(self, boxnum):
        """get all numbers in the box, return as array"""
        if boxnum < 3:
            rstart = 0
            rend = 3
        elif boxnum < 6:
            rstart = 3
            rend = 6
        else:
            rstart = 6
            rend = 9
        if boxnum in [0, 3, 6]:
            cstart = 0
            cend = 3
        elif boxnum in [1, 4, 7]:
            cstart = 3
            cend = 6
        else:
            cstart = 6
            cend = 9
        cells = self.puzzle[rstart:rend, cstart:cend]
        nums = []
        for row in cells:
            for rowcell in row:
                nums.append(rowcell.getnum())
        return nums

############################################


def main():
    """simple tests of Puzzle class"""

    # easy: all can be forced
    easy = np.array([[9, 0, 7, 5, 6, 0, 0, 4, 3],
                     [0, 1, 4, 0, 8, 0, 0, 6, 5],
                     [0, 0, 5, 0, 0, 0, 7, 2, 0],
                     [0, 0, 8, 0, 9, 0, 0, 0, 1],
                     [0, 0, 0, 0, 7, 0, 0, 0, 0],
                     [6, 0, 0, 0, 5, 0, 4, 0, 0],
                     [0, 3, 9, 0, 0, 0, 8, 0, 0],
                     [4, 7, 0, 0, 1, 0, 3, 9, 0],
                     [8, 5, 0, 0, 3, 9, 6, 0, 4]])
    puzz1 = Puzzle()
    puzz1.setnums(easy)
    print(puzz1)
    done = False
    while not done:
        numchanged = puzz1.findforced()
        if numchanged == 0:
            done = True
    print(puzz1)
    print("solved?", puzz1.solved())

    shortz = np.array([[0, 3, 9, 5, 0, 0, 0, 0, 0],
                       [0, 0, 0, 8, 0, 0, 0, 7, 0],
                       [0, 0, 0, 0, 1, 0, 9, 0, 4],
                       [1, 0, 0, 4, 0, 0, 0, 0, 3],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 7, 0, 0, 0, 8, 6, 0],
                       [0, 0, 6, 7, 0, 8, 2, 0, 0],
                       [0, 1, 0, 0, 9, 0, 0, 0, 5],
                       [0, 0, 0, 0, 0, 1, 0, 0, 8]])
    puzz2 = Puzzle()
    puzz2.setnums(shortz)
    print(puzz2)
    done = False
    while not done:
        numchanged = puzz2.findforced()
        if numchanged == 0:
            done = True
    print(puzz2)
    print("solved?", puzz2.solved())
    print("creating puzzle markup...")
    puzz2.mark()
    puzz2.showmarkup()
    print("finding preemptive sets...")
    puzz2.findpss()
    puzz2.showpreemptivesets()
    print("filtering markups...")
    puzz2.filtermarkups()
    puzz2.showmarkup()
    while not puzz2.solved():
        print(puzz2)
        puzz2.findpss()
        puzz2.showpreemptivesets()
        puzz2.filtermarkups()
        puzz2.showmarkup()
    print(puzz2)

# two that don't solve yet...
    diabolical = np.array([[0, 9, 0, 7, 0, 0, 8, 6, 0],
                           [0, 3, 1, 0, 0, 5, 0, 2, 0],
                           [8, 0, 6, 0, 0, 0, 0, 0, 0],
                           [0, 0, 7, 0, 5, 0, 0, 0, 6],
                           [0, 0, 0, 3, 0, 7, 0, 0, 0],
                           [5, 0, 0, 0, 1, 0, 7, 0, 0],
                           [0, 0, 0, 0, 0, 0, 1, 0, 9],
                           [0, 2, 0, 6, 0, 0, 3, 5, 0],
                           [0, 5, 4, 0, 0, 8, 0, 7, 0]])
    puzz3 = Puzzle()
    puzz3.setnums(diabolical)
    print(puzz3)
    """
    done = False
    while not done:
        numchanged = puzz3.findforced()
        if numchanged == 0:
            done = True
    print(puzz3)
    print("solved?", puzz3.solved())
    print("creating puzzle markup...")
    puzz3.mark()
    puzz3.showmarkup()
    while not puzz3.solved():
        print(puzz3)
        puzz3.findpss()
        puzz3.showpreemptivesets()
        puzz3.filtermarkups()
        puzz3.showmarkup()
    print(puzz3)
    """

    beach = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 7, 0, 0, 3, 8, 0, 0],
                      [2, 0, 0, 0, 0, 0, 0, 3, 0],
                      [0, 9, 0, 6, 0, 4, 0, 1, 0],
                      [0, 0, 6, 0, 1, 0, 5, 0, 0],
                      [0, 3, 0, 9, 0, 7, 0, 6, 0],
                      [0, 4, 0, 0, 8, 0, 0, 0, 2],
                      [0, 0, 9, 5, 0, 0, 1, 0, 0],
                      [3, 0, 0, 0, 0, 0, 0, 0, 9]])
    puzz4 = Puzzle()
    puzz4.setnums(beach)
    print(puzz4)
    """
    done = False
    while not done:
        numchanged = puzz4.findforced()
        if numchanged == 0:
            done = True
    print(puzz4)
    print("solved?", puzz4.solved())
    print("creating puzzle markup...")
    puzz4.mark()
    puzz4.showmarkup()
    while not puzz4.solved():
        print(puzz4)
        puzz4.findpss()
        puzz4.showpreemptivesets()
        puzz4.filtermarkups()
        puzz4.showmarkup()
    print(puzz4)
    """

if __name__ == "__main__":
    main()
