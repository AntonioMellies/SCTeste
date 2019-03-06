import pandas as pd

# models
from models.system_C.SystemCEventosCpfDTO import SystemCEventosCpfDTO

# exceptions
from exceptions.DataProcessingException import DataProcessingException
from exceptions.FormMissingParametersException import FormMissingParametersException

from flask import jsonify, request, Blueprint, Response
from DB.DB_SystemC import DB_SystemC
from utils import Environment

environment = Environment.EnvironmentFunctions.get_environment()
system_c_blueprint = Blueprint("system_c_blueprint", __name__, url_prefix="/systemc")



@system_c_blueprint.route("/eventoscpf", methods=['POST'])
def EventosCPF():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    cpf_form = request.json.get('cpf', None)

    if not cpf_form or len(str(cpf_form).replace(" ", "")) == 0:
        field = {'field': 'cpf'}
        raise FormMissingParametersException(payload=field, program='eventosCPF')


    try:
        dbConSystemC = DB_SystemC(environment)

        # CPF
        query = "SELECT * FROM TC1 WHERE cpf ='" + str(cpf_form).replace(" ", "") + "'"
        cpf_consulta = pd.read_sql_query(query, con=dbConSystemC.getConnection())

        if len(cpf_consulta) == 0:
            return jsonify({"msg": "CPF não encontrado"}), 400

        # Ultima Consulta CPF
        query = "SELECT * FROM TL1 WHERE cpf ='" + str(cpf_form).replace(" ", "") + "'"
        ultConsultaCPF_consulta = pd.read_sql_query(query, con=dbConSystemC.getConnection())
        if len(ultConsultaCPF_consulta) == 0:
            ultConsultaCPF_consulta = pd.DataFrame(columns=['ultima_cosulta'],
                                                   data=['CPF não possui consultas'])

        # Movimentações financeiras
        query = """SELECT 
                    M1.id  as id,
                    M1.cpf  as cpf,
                    M1.data as data,
                    M1.mov_type as tipo_movimento,
                    TM.type as desc_movimento
                FROM TM1 M1 
                INNER JOIN TTM TM ON (TM.id = M1.mov_type)
                WHERE 
                    M1.cpf ='""" + str(cpf_form).replace(" ", "") + "'"
        mov_consulta = pd.read_sql_query(query, con=dbConSystemC.getConnection())
        if len(mov_consulta) == 0:
            dividas_consulta = pd.DataFrame(columns=['movimentacoes'],
                                            data=['CPF não possui movimentações financeiras'])
        else:
            # Limita ultimas 6 movimentações
            mov_consulta.head(6)

        # Ultima compra no cartão de credito
        query = """SELECT 	* FROM TCC
                    WHERE 
                        cpf = """ + str(cpf_form).replace(" ", "") + """
                    ORDER BY id DESC 
                    LIMIT 1 """
        ultCompraCC_consulta = pd.read_sql_query(query, con=dbConSystemC.getConnection())
        if len(ultCompraCC_consulta) == 0:
            ultCompraCC_consulta = pd.DataFrame(columns=['ultima_compra_cc'],
                                            data=['CPF não compras no cartão de credito'])

        # Cria obj de retorno
        systemCEventosCpfDTO = SystemCEventosCpfDTO(cpf_consulta,ultConsultaCPF_consulta,mov_consulta,ultCompraCC_consulta)

    except Exception:
        raise DataProcessingException(status_code=401, program="consultadividacpf")

    return Response(systemCEventosCpfDTO.toJson(),
                    status=200,
                    mimetype='application/json')