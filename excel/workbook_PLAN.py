
# from __future__ import annotations
# from openpyxl import Workbook
# from openpyxl.styles import Alignment
# from openpyxl.chart import AreaChart3D, Reference
# from openpyxl.chart._3d import View3D
# from openpyxl.utils import get_column_letter
# from openpyxl.drawing.spreadsheet_drawing import TwoCellAnchor
# from ..utils.logging_setup import logger
# from typing import List, Tuple

# class WorkbookManager:
#     def __init__(self, path):
#         self.path = path
#         self.wb = Workbook()
#         ws0 = self.wb.worksheets[0]; ws0.title = 'Timeview - Open Points'
#         self.wb.create_sheet('Timeview - Open Checklists')
#         self.wb.create_sheet('Statistik_02')
#         self.wb.create_sheet('Statistik_01')
#         self.wb.create_sheet('Data_basis')

#     def set_headers(self, ws_name: str, headers: List[Tuple[str, int]]):
#         ws = self.wb[ws_name]
#         for col, (title, width) in enumerate(headers, start=1):
#             c = ws.cell(row=1, column=col, value=title)
#             c.alignment = Alignment(horizontal='left', textRotation=90)
#             ws.column_dimensions[c.column_letter].width = width
#         return ws

#     def add_area_chart(self, ws_name: str, title: str, x_title: str, y_title: str, header_row: int = 1):
#         """Insert an area chart using `header_row` as the row containing column titles.
#         Data rows begin at `header_row + 1`.
#         """
#         ws = self.wb[ws_name]
#         # need at least one header row and one data row with at least two columns of data
#         if ws.max_row < header_row + 1 or ws.max_column < 3:
#             logger.info('Überspringe Diagramm für %s (zu wenig Daten).', ws_name)
#             return
            
#         chart = AreaChart3D()
#         chart.title = title
#         chart.style = 13
#         chart.grouping = "standard" # Erzwingt die Standard-Darstellung
        
#         chart.legend = None

#         # Positionierung
#         anchor = TwoCellAnchor()
#         anchor._from.col = 0 
#         anchor._from.row = ws.max_row + 1 
#         anchor.to.col = 15 
#         anchor.to.row = ws.max_row + 30 
#         chart.anchor = anchor

#         # Daten-Referenzen
#         cats = Reference(ws, min_col=1, min_row=header_row + 1, max_row=ws.max_row)
#         data = Reference(ws, min_col=2, min_row=header_row, max_col=ws.max_column, max_row=ws.max_row)
        
#         if chart.x_axis:
#             chart.x_axis.title = x_title
#             chart.x_axis.delete = False
#             chart.x_axis.tickLblPos = "nextTo"
#         else:
#             logger.info("Fehler beim x_axis")

#         if chart.y_axis:
#                 chart.y_axis.title = y_title
#                 chart.y_axis.delete = False
#                 chart.y_axis.tickLblPos = "nextTo"
#         else:
#             logger.info("Fehler beim y_axis")

#         chart.z_axis.delete = False

#         # Daten hinzufügen
#         chart.add_data(data, titles_from_data=True)
#         chart.set_categories(cats)

#         ws.add_chart(chart)

#     def save(self):
#         self.wb.save(self.path)
#         logger.info("Excel gespeichert: %s", self.path)
