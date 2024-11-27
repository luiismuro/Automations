import requests
from bs4 import BeautifulSoup
import time
import csv


# Link do site da cotação do dolar
link = "https://www.google.com/search?q=cota%C3%A7%C3%A3o+dolar"

# requisicao para acessar o link
requisicao = requests.get(link)

# imprimindo o valor da requisicao (se foi aprovado ou nao) e imprimindo o texto do conteudo do site em html (link)
print(requisicao)
# print(requisicao.text)

site = BeautifulSoup(requisicao.text, "html.parser")
# print(site.prettify())

print(site.title)

pesquisa = site.find_all("input")
print(pesquisa[2])
