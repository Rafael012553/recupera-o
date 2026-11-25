"""Algoritmos de ordenação e busca (UC30 - Lógica de Programação).

Implementados à mão, sem usar sorted() ou list.sort(), para demonstrar a lógica.
"""


def ordenar_por_nome(lista):
    """Ordena uma lista de dicionários pelo campo 'nome' (Insertion Sort).

    Retorna uma NOVA lista, sem alterar a original.
    """
    resultado = list(lista)
    for i in range(1, len(resultado)):
        atual = resultado[i]
        j = i - 1
        # Desloca para a direita os itens maiores que o atual
        while j >= 0 and resultado[j]["nome"].lower() > atual["nome"].lower():
            resultado[j + 1] = resultado[j]
            j -= 1
        resultado[j + 1] = atual
    return resultado


def busca_por_nome(lista, termo):
    """Busca sequencial: devolve os itens cujo 'nome' contém o termo."""
    termo = termo.strip().lower()
    encontrados = []
    for item in lista:
        if termo in item["nome"].lower():
            encontrados.append(item)
    return encontrados
