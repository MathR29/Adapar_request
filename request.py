import requests

def adapar_requets(cultura,classe):

    url = "https://celepar07web.pr.gov.br/agrotoxicos/resultadoPesquisa.asp"

    payload = {
        "criterioClasse": classe,
        "criterioCulturaInfestada": cultura
    }

    response = requests.post(url = url,
                             data = payload)

    print(response.status_code)

    return print(response.text)


adapar_requets("Milho","Herbicida")
