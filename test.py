import requests

url = 'https://celepar07web.pr.gov.br/agrotoxicos/listar.asp?Cod=2014&descIngrediente=&CodIngredienteAtivo=null&CodFormulacao=null&IdRegistrante=null&CodFormaAcao=null&CodAlvo=null&CodGrupoQuimico=null&CodClassToxicologica=null&CodSituacao=null&CodClassificacao=null&CodEspecie=78&CodAgrotoxico=null&NumeroRegistro=null&expurgo=null&aplica=null&tratam=null&ClassificacaoQuiBio=null&criterioAgrotoxico=&criterioIngredienteAtivo=&criterioRegistrante=&criterioClassificacaoToxicologica=&criterioPraga=&criterioSituacao=&criterioClasse=&criterioCulturaInfestada=Arroz&criterioExpurgo=&criterioAplicacaoAerea=&criterioTratamentoSementes='

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.adapar.pr.gov.br/agrotoxicos/pesquisar.asp",
}

response = requests.get(url, headers=headers).text
print(response)
with open("pagina.html", "w", encoding="utf-8") as f:
    f.write(response.text)
