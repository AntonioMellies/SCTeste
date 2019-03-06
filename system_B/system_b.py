import datetime as dt
import pandas as pd

# models
from models.system_B.SystemBConsultaScoreCpfDTO import SystemBConsultaScoreCpfDTO

# exceptions
from exceptions.DataProcessingException import DataProcessingException
from exceptions.FormMissingParametersException import FormMissingParametersException

#
from flask import jsonify, request, Blueprint, Response
from flask_jwt_extended import jwt_required
from DB.DB_SystemB import DB_SystemB
from utils import Environment

environment = Environment.EnvironmentFunctions.get_environment()
system_b_blueprint = Blueprint("system_b_blueprint", __name__, url_prefix="/systemb")


@system_b_blueprint.route("/scorecreditocpf", methods=['POST'])
@jwt_required
def ScoreCredito():

    val_bens = 0
    qtd_renda = 0
    score_pontos = 0
    risco_addres = 0

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    cpf_form = request.json.get('cpf', None)

    if not cpf_form or len(str(cpf_form).replace(" ", "")) == 0:
        field = {'field': 'cpf'}
        raise FormMissingParametersException(payload=field, program='scorecreditocpf')


    try:
        dbConSystemB = DB_SystemB(environment)

        # CPF
        query = "SELECT * FROM TC1 WHERE cpf ='" + str(cpf_form).replace(" ", "") + "'"
        cpf_consulta = pd.read_sql_query(query, con=dbConSystemB.getConnection())

        if len(cpf_consulta) == 0:
            return jsonify({"msg": "CPF não encontrado"}), 400
        idade = id_addres = cpf_consulta.iloc[0]['age']

        # Endereço
        id_addres = cpf_consulta.iloc[0]['addres_id']

        query = "SELECT * FROM TA1 WHERE id ='" + str(id_addres) + "'"
        addres_consulta = pd.read_sql_query(query, con=dbConSystemB.getConnection())

        if len(addres_consulta) == 0:
            return jsonify({"msg": "Não há endereçoes relacioandos a esse CPF"}), 400
        else:
            risco_addres = addres_consulta.iloc[0]['risk']

        # Bens
        query = "SELECT * FROM TB1 WHERE cpf ='" + str(cpf_form).replace(" ", "") + "'"
        bens_consulta = pd.read_sql_query(query, con=dbConSystemB.getConnection())


        if len(bens_consulta) == 0:
            bens_consulta = pd.DataFrame(columns=['bens'],data=['Não existe bens relacionados a esse CPF'])
        else:
            val_bens = bens_consulta['value'].sum()

        # Fonde de Renda
        query = "SELECT * FROM TF1 WHERE cpf ='" + str(cpf_form).replace(" ", "") + "'"
        renda_consulta = pd.read_sql_query(query, con=dbConSystemB.getConnection())

        if len(renda_consulta) == 0:
            renda_consulta = pd.DataFrame(columns=['rendas'], data=['Não existe fontes de renda relacionados a esse CPF'])
        else:
            qtd_renda = len(renda_consulta)

        # Score - Idade
        if idade <= 18:
            score_pontos = 90
        elif idade <=25:
            score_pontos = 125
        elif idade <=40:
            score_pontos = 200
        else:
            score_pontos = 300

        # Score - Bens
        if val_bens <= 20000:
            score_pontos += 90
        elif val_bens <=60000:
            score_pontos += 125
        elif val_bens <=150000:
            score_pontos += 200
        elif val_bens <= 400000:
            score_pontos += 350
        else:
            score_pontos += 450

        # Score - Renda
        if qtd_renda == 0:
            score_pontos += 90
        elif qtd_renda == 1:
            score_pontos += 125
        else:
            score_pontos += 250

        # Score - Risco Endereço
        if risco_addres == 1:
            score_pontos -= 0
        elif risco_addres == 2:
            score_pontos -= 100
        elif risco_addres == 3:
            score_pontos -= 150
        elif risco_addres == 4:
            score_pontos -= 200
        else:
            score_pontos -= 300

        # Cria obj de retorno
        systemBConsultaScoreCpfDTO = SystemBConsultaScoreCpfDTO(cpf_consulta,addres_consulta,bens_consulta,renda_consulta,score_pontos)

    except Exception:
        raise DataProcessingException(status_code=401, program="consultadividacpf")

    return Response(systemBConsultaScoreCpfDTO.toJson(),
                    status=200,
                    mimetype='application/json')
