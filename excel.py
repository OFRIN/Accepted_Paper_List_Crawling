# Copyright (C) 2020 * Ltd. All rights reserved.
# author : Sanghyeon Jo <josanghyeokn@gmail.com>

import os
import openpyxl

class XLSX_Writer:
    def __init__(self, excel_path : str, class_names : list):
        if os.path.isfile(excel_path):
           raise ValueError 
        
        self.book = openpyxl.Workbook()
        self.book.remove(self.book.get_sheet_by_name('Sheet'))
        self.sheet = self.book.create_sheet('Papers')

        self.start_ascii = 65
        self.row_index = 1

        self.update(class_names)

    def __call__(self, dataset):
        self.update(dataset)

    def update(self, dataset):
        for index, data in enumerate(dataset):
            column = chr(self.start_ascii + index)
            self.sheet['{}{}'.format(column, self.row_index)] = data
        self.row_index += 1

    def close(self, dataset):
        self.book.save(self.excel_path)