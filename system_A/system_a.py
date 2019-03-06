import pandas as pd

# models
from models.system_A.SystemAConsultaDividaCpfDTO import SystemAConsultaDividaCpfDTO

# exceptions
from exceptions.DataProcessingException import DataProcessingException
from exceptions.FormMissingParametersException import FormMissingParametersException

#
from flask import jsonify, request, Blueprint, Response
from flask_jwt_extended import jwt_required
from DB.DB_SystemA import DB_SystemA
from utils import Environment

environment = Environment.EnvironmentFunctions.get_environment()
system_a_blueprint = Blueprint("system_a_blueprint", __name__, url_prefix="/systema")


@system_a_blueprint.route("/consultadividacpf", methods=['POST'])
@jwt_required
def ConsultaDividaCPF():

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    cpf_form = request.json.get('cpf', None)

    if not cpf_form or len(str(cpf_form).replace(" ", "")) == 0:
        field = {'field': 'cpf'}
        raise FormMissingParametersException(payload=field, program='consultadividacpf')


    try:
        dbConSystemA = DB_SystemA(environment)

        # CPF
        query = "SELECT * FROM TC1 WHERE cpf ='" + str(cpf_form).replace(" ", "") + "'"
        cpf_consulta = pd.read_sql_query(query, con=dbConSystemA.getConnection())

        if len(cpf_consulta) == 0:
            return jsonify({"msg": "CPF não encontrado"}), 400

        # Endereço
        id_addres = cpf_consulta.iloc[0]['addres_id']

        query = "SELECT * FROM TA1 WHERE id ='" + str(id_addres) + "'"
        addres_consulta = pd.read_sql_query(query, con=dbConSystemA.getConnection())

        if len(addres_consulta) == 0:
            return jsonify({"msg": "Não há endereçoes relacioandos a esse CPF"}), 400

        # Dividas
        query = "SELECT * FROM TD1 WHERE cpf ='" + str(cpf_form).replace(" ", "") + "'"
        dividas_consulta = pd.read_sql_query(query, con=dbConSystemA.getConnection())

        if len(dividas_consulta) == 0:
            dividas_consulta = pd.DataFrame(columns=['dividas'],data=['não há dividas'])

        # Cria obj de retorno
        systemAConsultaDividaCpfDTO = SystemAConsultaDividaCpfDTO(cpf_consulta,addres_consulta,dividas_consulta)

    except Exception:
        raise DataProcessingException(status_code=401, program="consultadividacpf")

    return Response(systemAConsultaDividaCpfDTO.toJson(),
                    status=200,
                    mimetype='application/json')
