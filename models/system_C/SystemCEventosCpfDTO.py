import json
import pandas as pd
from models.Model_DTO import Model_DTO




class SystemCEventosCpfDTO(Model_DTO):

    def __init__(self, cpf_consulta,ultConsultaCPF_consulta,mov_consulta,ultCompraCC_consulta):
        self.cpf_consulta: pd.DataFrame = cpf_consulta
        self.ultConsultaCPF_consulta: pd.DataFrame = ultConsultaCPF_consulta
        self.mov_consulta: pd.DataFrame = mov_consulta
        self.ultCompraCC_consulta: pd.DataFrame = ultCompraCC_consulta

    def toJson(self):
        ret_json = {
           'cpf': self.cpf_consulta.to_dict(orient='records'),
           'ultima_cosulta': self.ultConsultaCPF_consulta.to_dict(orient='records'),
           'movimentacoes': self.mov_consulta.to_dict(orient='records'),
           'ultima_compra_cc': self.ultCompraCC_consulta.to_dict(orient='records')
        }

        return json.dumps(ret_json)
