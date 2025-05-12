import win32com.client
import os

EXCEL_FILE_PATH = r"K:\Market Maps\Interest Rates Map (K).xlsm"
MACRO_NAME = "ExportMasterTableToCSV"  # Just the macro name, not ModuleName.MacroName

excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False  # Set to True for debugging

wb = excel.Workbooks.Open(EXCEL_FILE_PATH)
excel.Application.Run(f"'{os.path.basename(EXCEL_FILE_PATH)}'!{MACRO_NAME}")
wb.Close(SaveChanges=False)
excel.Quit()

print("✅ Macro executed and CSV exported.")
