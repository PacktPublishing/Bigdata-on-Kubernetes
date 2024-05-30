class CaseTemplate:

    def build_template(self, workbook, unique_id):
        wb = workbook
        ws = wb.active
        ws.title = str(unique_id)
        ws['A1'] = 'CASEID'
        ws['B1'] = 'CLIENT'
        ws['C1'] = 'CASENAME'
        ws['D1'] = 'CHALLENGE'
        ws['E1'] = 'SOLUTION'
        ws['F1'] = 'BUDGET'
        ws['G1'] = 'KPI'

        return wb
    
    def fill_template_parameters(self, workbook, parameter_dict) -> None:
        wb = workbook
        ws = wb.active
        ws['A2'] = parameter_dict['caseid']
        ws['B2'] = parameter_dict['client']
        ws['C2'] = parameter_dict['casename']
        ws['D2'] = parameter_dict['challenge']
        ws['E2'] = parameter_dict['solution']
        ws['F2'] = parameter_dict['budget']
        ws['G2'] = parameter_dict['kpi']

        return wb
    
    def save_template(self, workbook, filename) -> None:
        wb = workbook
        wb.save(filename)
