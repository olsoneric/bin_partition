import math

"""
Bin
A simple structure to speed up 2D spatial queries.

Background: http://en.wikipedia.org/wiki/Bin_(computational_geometry)

Evenly divide a space into a grid.
"""


class Bin:
    def __init__(self, columns, rows, fullWidth, fullHeight):
        self.numColumns = int(columns)
        self.numRows = int(rows)
        self.width = fullWidth
        self.height = fullHeight
        self.columnWidth = float(fullWidth) / self.numColumns
        self.rowHeight = float(fullHeight) / self.numRows
        self.columns = []
        self.rects = {}
        for j in range(self.numColumns):
            column = []
            for i in range(self.numRows):
                column.append([])
            self.columns.append(column)

    def get_string(self):
        result = ""
        for i in range(self.numRows):
            for j in range(self.numColumns):
                result += str(self.columns[j][i]) + " "
            result += "\n"
        return result

    def _get_col_row_range(self, rect):
        """Returns start_col, start_row, end_col, end_row."""

        # Note: The numbers for a python "range" are returned.
        #    which means one less than the end col and row is used.
        #startCol = int(float(rect.x) / self.columnWidth)
        #startRow = int(float(rect.y) / self.rowHeight)
        #endCol = min(self.numColumns,
        #                 int((rect.x+rect.width) / self.columnWidth) + 1)
        #endRow = min(self.numRows,
        #                 int((rect.y+rect.height) / self.rowHeight) + 1)
        ranges = (int(float(rect.x) / self.columnWidth),
                  int(float(rect.y) / self.rowHeight),
                  min(self.numColumns,
                      int((rect.x+rect.width) / self.columnWidth) + 1),
                  min(self.numRows,
                      int((rect.y+rect.height) / self.rowHeight) + 1)
                  )

        # Ensure they are non-negative
        return (max(0, ranges[0]),
                max(0, ranges[1]),
                max(0, ranges[2]),
                max(0, ranges[3]))

    def _get_col_row_range_from_point(self, point):
        """Returns start_col, start_row, end_col, end_row."""

        # Note: The numbers for a python "range" are returned.
        #    which means one less than the end col and row is used.
        #startCol = int(float(rect.x) / self.columnWidth)
        #startRow = int(float(rect.y) / self.rowHeight)
        #endCol = min(self.numColumns,
        #                 int((rect.x+rect.width) / self.columnWidth) + 1)
        #endRow = min(self.numRows,
        #                 int((rect.y+rect.height) / self.rowHeight) + 1)
        ranges = (int(float(point.x) / self.columnWidth),
                  int(float(point.y) / self.rowHeight),
                  min(self.numColumns,
                      int((point.x) / self.columnWidth) + 1),
                  min(self.numRows,
                      int((point.y) / self.rowHeight) + 1)
                  )

        # Ensure they are non-negative
        return (max(0, ranges[0]),
                max(0, ranges[1]),
                max(0, ranges[2]),
                max(0, ranges[3]))

    def insert(self, rect, obj):
        """Insert obj with region rect into the Bin structure."""

        if obj in self.rects.keys():
            raise Exception("remove before inserting again")
        #startCol = int(float(rect.x) / self.columnWidth)
        #startRow = int(float(rect.y) / self.rowHeight)
        startCol, startRow, endCol, endRow = self._get_col_row_range(rect)
        #print "Start:", startCol, startRow
        # Ex:  24 / 25.0 = 0.9xxx
        # Ex:  25 / 25.0 = 1.0
        # Ex:  26 / 25.0 = 1.xxx
        #endCol = int(math.ceil(float(rect.x+rect.width) / self.columnWidth))
        #endRow = int(math.ceil(float(rect.y+rect.height) / self.rowHeight))
        #endCol = min(self.numColumns,
        #                 int((rect.x+rect.width) / self.columnWidth) + 1)
        #endRow = min(self.numRows,
        #                 int((rect.y+rect.height) / self.rowHeight) + 1)
        #print "START,END:", startCol, startRow, "|", endCol, endRow
        for j in range(startCol,endCol):
            for i in range(startRow,endRow):
                # print j, i
                self.columns[j][i].append(obj)
        self.rects[obj] = rect

    def delete(self, obj):
        if obj in self.rects:
            del self.rects [obj]
        for j in range(self.numColumns):
            for i in range(self.numRows):
                if obj in self.columns[j][i]:
                    self.columns[j][i].remove(obj)

    def clear(self):
        self.columns = []
        self.rects = {}
        for j in range(self.numColumns):
            column = []
            for i in range(self.numRows):
                column.append([])
            self.columns.append(column)

    def move(self, obj, old_rect, new_rect):
        # TODO: unittest this!
        # TODO: make arg order in next two functions consistent
        self.deleteWithRect(obj, old_rect)
        del self.rects[obj]
        self.insert(new_rect, obj)

    def delete_with_rect(self, obj, rect):
        #startCol = int(rect.x / self.columnWidth)
        #startRow = int(rect.y / self.rowHeight)
        ##endCol = int((rect.x+rect.width) / self.columnWidth)
        ##endRow = int((rect.y+rect.height) / self.rowHeight)
        #endCol = int(math.ceil((rect.x+rect.width) / self.columnWidth))
        #endRow = int(math.ceil((rect.y+rect.height) / self.rowHeight))

        startCol, startRow, endCol, endRow = self._get_col_row_range(rect)
        for j in range(startCol, min(self.numColumns, endCol)):
            for i in range(startRow, min(self.numRows, endRow)):
        #for j in range(startCol,endCol):
        #    for i in range(startRow,endRow):
                if obj in self.columns[j][i]:
                    self.columns[j][i].remove(obj)

    # returns objects in the query rectangle
    def query(self, rect):
        returnObjectsRects = [] # list of tuples (obj,rect)
        #startCol = int(max(0,rect.x) / self.columnWidth)
        #startRow = int(max(0,rect.y) / self.rowHeight)
        ##endCol = int(math.ceil((rect.x+rect.width) / self.columnWidth))+1
        ##endRow = int(math.ceil((rect.y+rect.height) / self.rowHeight))+1
        #endCol = int((rect.x+rect.width) / self.columnWidth)
        #endRow = int((rect.y+rect.height) / self.rowHeight)

        startCol, startRow, endCol, endRow = self._get_col_row_range(rect)
        ##print "QUERY (scol,srow,ecol,erow): (2nd two numbers are range ends -- not inclusive)", startCol, startRow, endCol, endRow # -1 since we're using a python range
        #print "QUERY (scol,srow,ecol,erow): ", startCol, startRow, max(endCol-1, startCol), max(endRow-1,startRow) # -1 since we're using a python range
        #print startCol,endCol,startRow,endRow
        #for j in range(startCol,endCol):
        #    for i in range(startRow,endRow):
        for j in range(startCol,min(self.numColumns,endCol+1)):
            # the +1 in these loops is because range doesn't include last value
            for i in range(startRow,min(self.numRows,endRow+1)):
                for obj in self.columns[j][i]:
                    # print "rect test:", rect, self.rects[obj]
                    #if rect.colliderect(self.rects[obj]):
                    # next line works, but make more general
                    #if rect.intercepts(self.rects[obj]):
                    #print "COLLIDERECTS:", rect, self.rects[obj]
                    if self.collide_rects(rect,self.rects[obj]):
                        if (obj,self.rects[obj]) not in returnObjectsRects:
                            returnObjectsRects.append( (obj,self.rects[obj]) )

        return returnObjectsRects

    def query_point(self, point):
        return_objects_rects = []  # list of tuples (obj, rect)
        #startCol = int(max(0,rect.x) / self.columnWidth)
        #startRow = int(max(0,rect.y) / self.rowHeight)
        ##endCol = int(math.ceil((rect.x+rect.width) / self.columnWidth))+1
        ##endRow = int(math.ceil((rect.y+rect.height) / self.rowHeight))+1
        #endCol = int((rect.x+rect.width) / self.columnWidth)
        #endRow = int((rect.y+rect.height) / self.rowHeight)

        startCol, startRow, endCol, endRow = (
            self._get_col_row_range_from_point(point))
        ##print "QUERY (scol,srow,ecol,erow): (2nd two numbers are range ends -- not inclusive)", startCol, startRow, endCol, endRow # -1 since we're using a python range
        #print "QUERY (scol,srow,ecol,erow): ", startCol, startRow, max(endCol-1, startCol), max(endRow-1,startRow) # -1 since we're using a python range
        #print startCol,endCol,startRow,endRow
        #for j in range(startCol,endCol):
        #    for i in range(startRow,endRow):
        for j in range(startCol, min(self.numColumns, endCol+1)):
            # the +1 in these loops is because range doesn't include last value
            for i in range(startRow, min(self.numRows, endRow+1)):
                for obj in self.columns[j][i]:
                    # print "rect test:", rect, self.rects[obj]
                    #if rect.colliderect(self.rects[obj]):
                    # next line works, but make more general
                    #if rect.intercepts(self.rects[obj]):
                    #print "COLLIDERECTS:", rect, self.rects[obj]
                    if self.rects[obj].collidepoint(point):
                        if (obj, self.rects[obj]) not in return_objects_rects:
                            return_objects_rects.append((obj, self.rects[obj]))

        return return_objects_rects

    def get_all_objs(self):
        """Return all objects in grid."""

        objs = set()
        for column in self.columns:
            for row in column:
                objs.update(row)

        # Convert set to list and return
        return list(objs)

    def collide_rects_pygame(self, rect1, rect2):
        return rect1.colliderect(rect2)

    def collide_rects_e(self, rect1, rect2):
        return rect1.intercepts(rect2)

    collide_rects = collide_rects_e


def bin_use_pygame():
    Bin.collide_rects = Bin.collide_rects_pygame

