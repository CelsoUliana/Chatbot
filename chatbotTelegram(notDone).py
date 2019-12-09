###
#   Celso Antonio Uliana Junior - Nov 2019
###

#   Este trabalho consiste em um chatbot para uma hamburgueria.

#   Importação de dependencias.
import os
import csv
import frases
import random
import funcoes
import cardapio
import entidades
import datetime as dt
import param_grid as params

#   Integração Telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

def enviaMensagem(update, context, mensagem):
    update.message.reply_text(
        mensagem
    )

#   Funções bot telegram.
def start(update, context):

    saudacao = ''

    #   bom dia
    if hora > 6 and hora < 12:
        saudacao = random.choice(respostas['cumprimento']['manha'])

    #   boa tarde
    if hora > 12 and hora < 18:
        saudacao = random.choice(respostas['cumprimento']['tarde'])

    #   boa noite
    if hora > 18 or hora >= 0 and hora < 6:
        saudacao = random.choice(respostas['cumprimento']['noite'])

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text= saudacao + ' Para conversar, escreva /falar antes de qualquer mensagem.'
    )


def falar(update, context):
    #   Recebe o input e concatena
    separador = ' '
    frase = separador.join(context.args)

    #   Transforma e prediz.
    inst = vectorizer.transform([frase])
    intencao = classificador.predict(inst)

    print(intencao)

    if intencao == 'conta':
        
        valor = 0

        if pedido is not None:
            for chave in pedido:
                valor = valor + cardapio.mapeador[chave] * pedido[chave]

        if valor == 0:
            enviaMensagem(update, context, 'Você ainda não pediu nada.')

        else:

            frase_resultado = random.choice(respostas['conta']) + valor 

            enviaMensagem(update, context, frase_resultado)

            despedida = ''

            if hora > 6 and hora < 12:
                despedida = frase_resultado + random.choice(respostas['despedida']['manha'])

            if hora > 12 and hora < 18:
                despedida = frase_resultado + random.choice(respostas['despedida']['tarde'])

            if hora > 18 or hora >= 0 and hora < 6:
                despedida = frase_resultado + random.choice(respostas['despedida']['noite'])

            enviaMensagem(update, context, despedida)

            #   Limpeza de variaveis relacionadas ao uso, simulando o termino de uma conversa.
            pedido = {}

    if intencao == 'pedido':
        pedido_local = funcoes.reconhece_entidades(etiquetador, texto)
        if((pedido_local is not None) and ('num' in pedido_local) and ('pedidos' in pedido_local)):
            funcoes.mapeia_itens(pedido_local, mapeador, pedido)
            frase_resultado = random.choice(resposta['pedido'])
            enviaMensagem(update, context, frase_resultado)
        else:
            frase_resultado = random.choice(respostas['erro'])
            enviaMensagem(update, context, frase_resultado)


    if intencao == 'cardapio':
        enviaMensagem(update, context, random.choice(respostas['cardapio']))
        for sessao in card:
            enviaMensagem(update, context, str('------- ' + sessao + ' ----------'))
            for item in card[sessao]:
                enviaMensagem(update, context, str(' ' + item + ' R$:' + card[sessao][item]))

    if intencao == 'funcionario':
       frase_resultado = random.choice(respostas['funcionario'])
       enviaMensagem(update, context, frase_resultado)



def unknown(update, context):
    response_message = "Não foi reconhecido o /falar, formato é --> /falar <texto>"
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


#   x(texto), y(classe), flag para a conversa e hora do dia atual.
x = []
y = []
flag = 1
pedido = {}
hora = dt.datetime.today().hour

print(hora)

#   Leitura de parâmetros do modulo.
p = params.regressao()

#   Cardapio e entidades e frases de resposta.
card = cardapio.dic
respostas = frases.dic
mapeador = entidades.enum
etiquetador = entidades.dic

#   Leitura do dataset.
with open('dataset.csv', newline = '', encoding = 'utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        y.append(row['inten'])
        x.append(row['texto'])

#   Transformar os dados em BOW(bag of words).
vectorizer = TfidfVectorizer(sublinear_tf = True, max_df = 0.5, strip_accents = 'unicode')
x = vectorizer.fit_transform(x)

#   Instanciar o leave one outs.
loo = LeaveOneOut()
loo.get_n_splits(x)

print('Aguarde, o bot está sendo treinado...')

grid_search = GridSearchCV(LogisticRegression(), p, scoring = 'accuracy', cv = loo, iid = False)
grid_search.fit(x, y)

print('Acuracia do modelo =~ ', grid_search.best_score_)

classificador = LogisticRegression(random_state = grid_search.best_params_['random_state'], C = grid_search.best_params_['C'], multi_class = grid_search.best_params_['multi_class'],
solver = grid_search.best_params_['solver'], class_weight = grid_search.best_params_['class_weight'])

classificador.fit(x, y)


print('Pronto, agora é só usar!!')


def main():
    updater = Updater(token='895329401:AAHXBkqrcMCN0nyH9lm-ASBsS_gwb5Shqa0', use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        CommandHandler('start', start)
    )
    dispatcher.add_handler(
        CommandHandler('falar', falar, pass_args=True)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.command, unknown)
    )

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()
