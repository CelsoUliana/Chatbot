###
#   Celso Antonio Uliana Junior - Nov 2019
###

#   Reconhece entidades, e mapeia elas num dicionario
def reconhece_entidades(dic, texto):
    dic_resultado = {}
    palavras = texto.split()
    for palavra in palavras:
        temp = busca_dict(dic, palavra)
        if temp is not None:
            if temp[0] not in dic_resultado:
                dic_resultado[temp[0]] = []

            dic_resultado[temp[0]].append(temp[1])

    return dic_resultado
            
#   Busca se uma palavra está em um dicionario(que contem listas)
def busca_dict(dic, palavra):
    for chave, valor in dic.items():
        if palavra in valor:
            if chave == 'bebidas' or chave == 'pratos':
                return 'pedidos', palavra
            return chave, palavra
    return None

#   Dado entidades, mapeia elas em entidades reais (xburger -> x-burger), onde são reconhecidas no cardapio
def mapeia_itens(pedido_local, mapeador, pedido):
    lista_numerica = pedido_local['num']
    lista_pedidos = pedido_local['pedidos']
    if len(lista_numerica) != len(lista_pedidos):
        return
    for i in range(len(lista_pedidos)):
        chave = mapeador[lista_pedidos[i]]
        if chave not in pedido:
            pedido[chave] = mapeador[lista_numerica[i]]
        else:
            pedido[chave] = mapeador[lista_numerica[i]] + pedido[chave]
