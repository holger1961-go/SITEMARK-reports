
import win32com.client as win32

def make_macro() -> None:

    excel = win32.Dispatch("Excel.Application")
    excel.Visible = True


# TODO 261122 variabelize path und Abfrage leere Seite
    wb = excel.Workbooks.Open(r"C:\Users\HG396236\Documents\250130_x_________SITEMARK REPORT\sitemark_report.xlsx")

    ws = wb.Worksheets("Open Points")
    chart_obj = ws.ChartObjects(1)
    chart = chart_obj.Chart
    chart.Rotation = 40
    chart.Axes(1).TickLabels.Orientation = 90
    chart.Axes(3).TickLabels.Orientation = 90


    ws = wb.Worksheets("Checklists")
    chart_obj = ws.ChartObjects(1)
    chart = chart_obj.Chart
    chart.Rotation = 40
    chart.Axes(1).TickLabels.Orientation = 90
    chart.Axes(3).TickLabels.Orientation = 90    