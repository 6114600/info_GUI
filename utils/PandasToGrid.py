import wx
import wx.grid as grid

import pandas as pd


class GridTable(grid.PyGridTableBase):

    def __init__(self, datas):

        grid.GridTableBase.__init__(self)

        self.datas = datas

        self.isModified = False

        self.odd = grid.GridCellAttr()

        self.odd.SetReadOnly(True)

        self.odd.SetBackgroundColour('yellow')

        self.even = grid.GridCellAttr()

        self.even.SetReadOnly(True)

    def SetValue(self, row, col, value):

        print(str(row) + ";" + str(col) + ";" + value)

        def innerSetValue(row, col, value):

            try:

                self.datas[row][col] = value

            except IndexError:

                # add a new row

                self.datas.append([''] * self.GetNumberCols())

                innerSetValue(row, col, value)

                # tell the grid we've added a row

                msg = grid.GridTableMessage(self,  # The table

                                            grid.GRIDTABLE_NOTIFY_ROWS_APPENDED,  # what we did to it

                                            1  # how many

                                            )

                self.GetView().ProcessTableMessage(msg)

        innerSetValue(row, col, value)

    def GetAttr(self, row, col, kind):

        attr = [self.even, self.odd][row % 2]

        attr.IncRef()

        return attr

    def GetNumberRows(self):

        return len(self.datas)

    def GetNumberCols(self):

        return len(self.colLabels)

    def GetColLabelValue(self, col):

        return self.colLabels[col]

    def GetRowLabelValue(self, row):

        return str(row)

    def GetValue(self, row, col):

        return self.datas[row][col]

    def IsModified(self):

        return self.isModified

    def InsertRows(self, pos=1, newData=None):

        if newData is None:
            newData = [u'', u'', u'', u'', u'']

        self.datas.insert(pos, newData)

        self.isModified = True

        gridView = self.GetView()

        gridView.BeginBatch()

        insertMsg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED, pos, 1)

        gridView.ProcessTableMessage(insertMsg)

        gridView.EndBatch()

        getValueMsg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)

        gridView.ProcessTableMessage(getValueMsg)

        # if self.onGridValueChanged:

        #     self.onGridValueChanged()

        return True

    def AppendRows(self, newData=None):

        if newData is None:
            newData = [u'', u'', u'', u'', u'']

        self.datas.append(newData)

        self.isModified = True

        gridView = self.GetView()

        gridView.BeginBatch()

        appendMsg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)

        gridView.ProcessTableMessage(appendMsg)

        gridView.EndBatch()

        getValueMsg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)

        gridView.ProcessTableMessage(getValueMsg)

        # if self.onGridValueChanged:

        #     self.onGridValueChanged()

        return True

    def DeleteRows(self, pos=0, numRows=1):

        if self.datas is None or len(self.datas) == 0:
            return False

        for rowNum in range(0, numRows):
            self.datas.remove(self.datas[pos + rowNum])

        gridView = self.GetView()

        gridView.BeginBatch()

        deleteMsg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, pos, numRows)

        gridView.ProcessTableMessage(deleteMsg)

        gridView.EndBatch()

        getValueMsg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)

        gridView.ProcessTableMessage(getValueMsg)

        # if self.onGridValueChanged:

        #     self.onGridValueChanged()

        return True


# 将pandas 数据显示于grid控件中

def PandasToGrid(grid, df):
    # 数据表设置

    gridDatas = df.values

    Tdata = GridTable(gridDatas)

    # 设置标题
    labels = list(map(lambda x: str(x), df.columns))
    for i in range(len(labels)):
        # print(labels[i])
        if labels[i] == 'Squence':
            labels[i] = '流水号'
        elif labels[i] == 'date_time':
            labels[i] = '记录时间'
        elif labels[i] == 'water_h':
            labels[i] = '热水表读数'
        elif labels[i] == 'water_c':
            labels[i] = '冷水表读数'
        elif labels[i] == 'electri':
            labels[i] = '电表读数'
    Tdata.colLabels = labels

    grid.SetTable(Tdata, True)

    grid.Refresh()
