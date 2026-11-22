
# from __future__ import annotations
# from collections import defaultdict
# from typing import Dict, List
# import openpyxl

# class Statistics:
#     @staticmethod
#     def aggregate_by_project_and_form(rows: List[Dict]) -> List[Dict]:
#         agg = defaultdict(lambda: defaultdict(int))
#         for r in rows:
#             key = (r['project'], r['form_name'])
#             agg[key][r['status']] += 1
#         result = []
#         for (project, form), counts in agg.items():
#             res = {
#                 'Projekt': project,
#                 'Tickettyp': form,
#                 'Open': counts.get('Open', 0),
#                 'In Progress': counts.get('In Progress', 0),
#                 'Resolved': counts.get('Resolved', 0),
#                 'Closed': counts.get('Closed', 0),
#                 'Rejected': counts.get('Rejected', 0),
#                 'Feedback': counts.get('Feedback', 0),
#             }
#             result.append(res)
#         return result

#     @staticmethod
#     def write_statistik_01(wb_path: str, data_rows: List[Dict]):
#         book = openpyxl.load_workbook(wb_path)
#         sheet = book['Statistik_01']
#         headers = ['Projekt', 'Tickettyp', 'Open', 'In Progress', 'Resolved', 'Closed', 'Rejected', 'Feedback']
#         for col, h in enumerate(headers, start=1):
#             sheet.cell(row=1, column=col).value = h
#         for r_idx, row in enumerate(data_rows, start=2):
#             sheet.cell(row=r_idx, column=1).value = row['Projekt']
#             sheet.cell(row=r_idx, column=2).value = row['Tickettyp']
#             sheet.cell(row=r_idx, column=3).value = row['Open']
#             sheet.cell(row=r_idx, column=4).value = row['In Progress']
#             sheet.cell(row=r_idx, column=5).value = row['Resolved']
#             sheet.cell(row=r_idx, column=6).value = row['Closed']
#             sheet.cell(row=r_idx, column=7).value = row['Rejected']
#             sheet.cell(row=r_idx, column=8).value = row['Feedback']
#         book.save(wb_path)

#     @staticmethod
#     def write_statistik_02_bars(wb_path: str):
#         book = openpyxl.load_workbook(wb_path)
#         src = book['Statistik_01']; dst = book['Statistik_02']
#         dst.column_dimensions['A'].width = 20
#         dst.column_dimensions['B'].width = 10
#         dst.column_dimensions['C'].width = 10
#         dst.column_dimensions['D'].width = 5
#         from openpyxl.utils import get_column_letter
#         for col in range(5, 703):  # E (5) to ZZ (702)
#             dst.column_dimensions[get_column_letter(col)].width = 1
#         dst['A1'].value = 'Projekt'; dst['B1'].value = 'Item'; dst['C1'].value = 'Quantity'; dst['E1'].value = 'Load'
#         from openpyxl.styles import PatternFill
#         fills = {
#             0: PatternFill(start_color='FFAAAA', end_color='FFAAAA', fill_type='solid'),
#             1: PatternFill(start_color='10FF88', end_color='10FF88', fill_type='solid'),
#             2: PatternFill(start_color='10FF88', end_color='10FF88', fill_type='solid'),
#             3: PatternFill(start_color='00D36A', end_color='00D36A', fill_type='solid'),
#             4: PatternFill(start_color='51A8FF', end_color='51A8FF', fill_type='solid'),
#             5: PatternFill(start_color='51A8FF', end_color='51A8FF', fill_type='solid'),
#         }
#         from collections import defaultdict
#         projects = defaultdict(lambda: [0,0,0,0,0,0])
#         for r in range(2, src.max_row+1):
#             proj = src.cell(r,1).value
#             if not proj: continue
#             vals = [src.cell(r, c).value or 0 for c in range(3,9)]
#             projects[proj] = [a+b for a,b in zip(projects[proj], vals)]
#         row = 2; labels = ['Open','In Progress','Resolved','Closed','Rejected','Feedback']
#         for proj, counts in projects.items():
#             for i, label in enumerate(labels):
#                 dst.cell(row=row, column=1).value = proj
#                 dst.cell(row=row, column=2).value = label
#                 dst.cell(row=row, column=3).value = counts[i]
#                 width = (counts[i] + 9)//10
#                 for col in range(5, 5+max(1, width)):
#                     dst.cell(row=row, column=col).fill = fills.get(i)
#                 row += 1
#             row += 1
#         book.save(wb_path)
