import requests
import json

# definir a URL da API do Azure DevOps
url = "https://dev.azure.com/{SafewebInfra}/{93}/_apis/wit/workitems/?api-version=6.0"

# definir o ID do colaborador e do projeto e o ID do item de trabalho
colaborador_id = "xxxxx"
projeto_id = "xxxxx"
item_trabalho_id = "xxxxx"

# definir o ID do campo personalizado que você deseja atualizar
campo_personalizado_id = "xxxxx"

# definir os dados da atualização
atualizacao = [{
    "op": "add",
    "path": "/fields/" + campo_personalizado_id,
    "value": "Novo valor do campo personalizado"
}]

# definir o cabeçalho de autenticação com o token de acesso pessoal
cabecalho = {"Authorization": "Basic <seu_token_de_acesso_pessoal_aqui>"}

# criar a solicitação HTTP POST
solicitacao = requests.patch(
    url.format(organization="SuaOrganizacao", project=projeto_id, id=item_trabalho_id),
    headers=cabecalho,
    json=atualizacao
)

# verificar o código de status da resposta
if solicitacao.status_code == 200:
    print("Valor do campo personalizado atualizado com sucesso!")
else:
    print("Ocorreu um erro ao atualizar o valor do campo personalizado:", solicitacao.text)
