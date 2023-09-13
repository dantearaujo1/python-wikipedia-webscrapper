# Projeto para vaga de estágio

O projeto consiste em um script python para pegar dados sobre as capitais
brasileiras e jogá-los em um DataFrame. Para isso foram utilizadas algumas
bibliotecas de terceiros como pandas, wikipedia, requests, bs4.

# Como usar

Na raiz do projeto, crie um ambiente virtual usando venv
e em seguida instale os pacotes necessários

```
python -m venv  .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ao final rode o programa

```
python wiki_city_scrapping.py
```

Será printado no console o DataFrame e também será criado um arquivo csv para
olhar no excel ou derivados.
