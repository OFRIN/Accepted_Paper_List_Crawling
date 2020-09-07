# Copyright (C) 2020 * Ltd. All rights reserved.
# author : Sanghyeon Jo <josanghyeokn@gmail.com>

import os
import openpyxl

class XLSX_Writer:
    def __init__(self, excel_path : str, class_names : list):
        if os.path.isfile(excel_path):
           raise ValueError 

        self.excel_path = excel_path
        
        self.book = openpyxl.Workbook()
        self.book.remove(self.book.get_sheet_by_name('Sheet'))
        self.sheet = self.book.create_sheet('Papers')

        self.start_ascii = 65
        self.row_index = 1

        self.update(class_names)

    def __call__(self, dataset : list):
        self.update(dataset)

    def update(self, dataset : list):
        for index, data in enumerate(dataset):
            column = chr(self.start_ascii + index)
            self.sheet['{}{}'.format(column, self.row_index)] = data
        self.row_index += 1

    def close(self):
        self.book.save(self.excel_path)

class XLSX_Reader:
    def __init__(self, excel_path : str, class_names : list):
        if not os.path.isfile(excel_path):
           raise ValueError 

        self.book = openpyxl.load_workbook(excel_path)
        self.sheet = book.get_sheet_by_name('Papers')

        self.get_fn = lambda name: sheet[name].value

        self.class_names = class_names

        self.start_ascii = 65
        self.row_index = 2