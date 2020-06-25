import requests
from decimal import Decimal
import matplotlib.pyplot as plt

uri_transaparencia = 'http://www.transparencia.gov.br/api-de-dados/despesas/documentos-por-favorecido'
cnpj = ''
#Payments
phase = '3' 
years = [2015, 2016, 2017, 2018, 2019, 2020]
result_year_sum = dict((k, Decimal('0.0')) for k in years)

for year in years:
    page = 1
    while True:
        uri = '{}?{}&{}&{}&{}'.format(uri_transaparencia, 'codigoPessoa='+cnpj, 'fase='+phase, 'ano='+str(year), 'pagina='+str(page))
        #this a retry because the api response stranger things sometimes, :)
        while True:
            try:
                response = requests.get(uri)
                print(response.text)
                json = response.json()
            except:
                continue
            break
        if response.status_code != 200 or not json:
            print(f'GET {uri} and status code {response.status_code}')
            break
        for item in json:
            result_year_sum[year] = result_year_sum[year] + Decimal(item['valor'].replace('.', '').replace(',', '.').replace(' ', ''))
        page = page + 1

#Using matplotlib to plot bar chat 
plt.bar(range(len(result_year_sum)), list(result_year_sum.values()), align='center')
plt.xticks(range(len(result_year_sum)), list(result_year_sum.keys()))
plt.show()