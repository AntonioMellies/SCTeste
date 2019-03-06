import json
import pandas as pd
from models.Model_DTO import Model_DTO




class SystemAConsultaDividaCpfDTO(Model_DTO):

    def __init__(self, cpf_consulta, addres_consulta, dividas_consulta):
        self.cpf_consulta: pd.DataFrame = cpf_consulta
        self.addres_consulta: pd.DataFrame = addres_consulta
        self.dividas_consulta: pd.DataFrame = dividas_consulta

    def toJson(self):
        ret_json = {
            'cpf': self.cpf_consulta.to_dict(orient='records'),
            'endereco': self.addres_consulta.to_dict(orient='records'),
            'divida': self.dividas_consulta.to_dict(orient='records')
        }

        return json.dumps(ret_json)
