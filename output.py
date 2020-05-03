import openpyxl

def excel(name,f_number, diff_percent,split,len_bs,res,sheet):
    wb = openpyxl.load_workbook("Input/"+name+'.xlsx', read_only=False)
    ws=wb[sheet]
    row_count = ws.max_row + 1
    for i in range(split):
        r = row_count + i
        ws.cell(r, 1).value = str(f_number)
        ws.cell(r, 2).value = diff_percent
        ws.cell(r, 3).value = i
        for j in range(len_bs):
            try:
                ws.cell(r, 4 + j*3).value = res[j][i][1][1]
                ws.cell(r, 5 + j*3).value = res[j][i][0][0]
                ws.cell(r, 6 + j * 3).value = str(res[j][i][2])
            except:
                ws.cell(r, 4 + j * 3).value = 0
                ws.cell(r, 5 + j * 3).value = 0
                ws.cell(r, 6 + j * 3).value = "ERROR"
    r = ws.max_row + 1
    for line,item in zip(range(3),['MIN','MAX','AVERAGE']):
        l=r+line
        ws['D'+ str(l)] = '=' +item+'(D'+str(r-5)+':D'+str(r-1)+')'
        ws['E' + str(l)] = '=' +item+'(E'+str(r-5)+':E' + str(r - 1) + ')'
        ws['G' + str(l)] = '=' +item+'(G'+str(r-5)+':G' + str(r - 1) + ')'
        ws['H' + str(l)] = '=' +item+'(H'+str(r-5)+':H' + str(r - 1) + ')'
        ws['J' + str(l)] = '=' + item + '(J' + str(r - 5) + ':J' + str(r - 1) + ')'
        ws['K' + str(l)] = '=' +item+'(K'+str(r-5)+':K' + str(r - 1) + ')'
    wb.save("Input/"+name+".xlsx")