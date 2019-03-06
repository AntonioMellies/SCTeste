import json
import pandas as pd
from models.Model_DTO import Model_DTO




class SystemBConsultaScoreCpfDTO(Model_DTO):

    def __init__(self, cpf_consulta,addres_consulta,bens_consulta,renda_consulta,score_pontos):
        self.cpf_consulta: pd.DataFrame = cpf_consulta
        self.addres_consulta: pd.DataFrame = addres_consulta
        self.bens_consulta: pd.DataFrame = bens_consulta
        self.renda_consulta: pd.DataFrame = renda_consulta
        self.score_pontos: int = score_pontos

    def toJson(self):
        ret_json = {
           'cpf': self.cpf_consulta.to_dict(orient='records'),
           'endereco': self.addres_consulta.to_dict(orient='records'),
           'bens': self.bens_consulta.to_dict(orient='records'),
           'rendas': self.renda_consulta.to_dict(orient='records') ,
           'score': self.score_pontos
        }

        return json.dumps(ret_json)
