#Requisitos iniciais necessarios

#pip install graphviz

#instalar também no sistema https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/12.2.1/windows_10_cmake_Release_graphviz-install-12.2.1-win64.exe

from graphviz import Digraph

class AFD:
    def __init__(self, sigma, Q, delta, q0, F):
        self.sigma = sigma  # Alfabeto
        self.Q = Q          # Conjunto de estados
        self.delta = delta  # Função de transição
        self.q0 = q0        # Estado inicial
        self.F = F          # Conjunto de estados finais

    def __str__(self):
        return f"AFD(Sigma={self.sigma}, Q={self.Q}, delta={self.delta}, q0={self.q0}, F={self.F})"

    def visualizar(self, nome_arquivo="afd"):
        """
        Gera uma representação visual do AFD usando graphviz.
        """
        dot = Digraph(comment="AFD")

        # Adiciona estados
        for estado in self.Q:
            if estado in self.F:
                dot.node(estado, shape="doublecircle")  # Estado final
            else:
                dot.node(estado)

            if estado == self.q0:
                # Adiciona uma seta invisível para indicar o estado inicial
                dot.node("inicio", shape="point")
                dot.edge("inicio", estado)

        # Adiciona transições
        for (origem, simbolo), destino in self.delta.items():
            dot.edge(origem, destino, label=simbolo)

        # Renderiza e salva a imagem
        dot.render(nome_arquivo, format="png", cleanup=True)
        print(f"Representação visual salva como '{nome_arquivo}.png'")

# Função para criar um AFD
def criar_afd(sigma, Q, q0, F, delta):
    return AFD(sigma, Q, delta, q0, F)

# Função para validar uma palavra
def validar_palavra(afd, palavra):
    """
    Valida uma palavra no AFD e retorna o resultado e as etapas de validação.
    """
    estado_atual = afd.q0
    etapas = [f"Estado inicial: {estado_atual}"]
    
    for simbolo in palavra:
        if simbolo not in afd.sigma:
            etapas.append(f"Erro: Símbolo '{simbolo}' não pertence ao alfabeto.")
            return False, etapas
        
        proximo_estado = afd.delta.get((estado_atual, simbolo), '')
        if not proximo_estado:  # Se for vazio ou None
            etapas.append(f"Erro: Não há transição definida para δ({estado_atual}, {simbolo}).")
            return False, etapas
        
        etapas.append(f"Transição: δ({estado_atual}, {simbolo}) = {proximo_estado}")
        estado_atual = proximo_estado
    
    if estado_atual in afd.F:
        etapas.append(f"A palavra '{palavra}' é aceita pelo AFD.")
        return True, etapas
    else:
        etapas.append(f"A palavra '{palavra}' não é aceita pelo AFD.")
        return False, etapas

def completar_afd(afd):
    """
    Completa o AFD adicionando um estado de "morte" para transições indefinidas.
    Retorna uma cópia completa do AFD original.
    """
    # Criar um novo estado de "nulo" (usando um nome que não conflite com estados existentes)
    estado_morte = 'q_nulo'
    while estado_morte in afd.Q:
        estado_morte += '_'
    
    Q_completo = afd.Q.union({estado_morte})
    delta_completo = {}
    
    # Preencher todas as transições
    for estado in Q_completo:
        for simbolo in afd.sigma:
            if estado in afd.Q:
                # Para estados originais, usa a transição definida ou vai para estado_morte
                prox_estado = afd.delta.get((estado, simbolo), '')
                delta_completo[(estado, simbolo)] = prox_estado if prox_estado else estado_morte
            else:
                # Para o estado_morte, todas as transições voltam para ele mesmo
                delta_completo[(estado, simbolo)] = estado_morte
    
    return AFD(afd.sigma, Q_completo, delta_completo, afd.q0, afd.F)

# Função para minimizar o AFD
def minimizar_afd(afd):
    # Primeiro completamos o AFD
    afd_completo = completar_afd(afd)
    
    # Agora usamos o afd_completo para a minimização
    def remover_inalcancaveis(afd):
        alcancaveis = set()
        pilha = [afd.q0]
        
        while pilha:
            estado = pilha.pop()
            if estado not in alcancaveis:
                alcancaveis.add(estado)
                for simbolo in afd.sigma:
                    proximo_estado = afd.delta.get((estado, simbolo))
                    if proximo_estado and proximo_estado not in alcancaveis:
                        pilha.append(proximo_estado)
        
        afd.Q = alcancaveis
        afd.delta = {k: v for k, v in afd.delta.items() if k[0] in alcancaveis}
        afd.F = afd.F.intersection(alcancaveis)

    remover_inalcancaveis(afd_completo)

    # Passo 2: Construir a tabela de pares de estados
    pares = set()
    estados_ordenados = sorted(afd_completo.Q)  # Ordena para consistência
    for i, q1 in enumerate(estados_ordenados):
        for q2 in estados_ordenados[i+1:]:
            pares.add((q1, q2))

    # Passo 3: Identificar pares de estados trivialmente não equivalentes
    marcados = set()
    for q1, q2 in pares:
        if (q1 in afd_completo.F and q2 not in afd_completo.F) or (q2 in afd_completo.F and q1 not in afd_completo.F):
            marcados.add((q1, q2))

    # Passo 4: Analisar os pares restantes
    def sao_equivalentes(q1, q2, marcados):
        for simbolo in afd_completo.sigma:
            prox1 = afd_completo.delta[(q1, simbolo)]  # Garantido que existe
            prox2 = afd_completo.delta[(q2, simbolo)]  # Garantido que existe
            if (prox1, prox2) in marcados or (prox2, prox1) in marcados:
                return False
        return True

    while True:
        novos_marcados = set()
        for q1, q2 in pares - marcados:
            if not sao_equivalentes(q1, q2, marcados):
                novos_marcados.add((q1, q2))
        if not novos_marcados:
            break
        marcados.update(novos_marcados)

    # Passo 5: Unificar estados equivalentes
    equivalentes = {q: q for q in afd_completo.Q}

    for q1, q2 in pares - marcados:
        if equivalentes[q1] != equivalentes[q2]:
            representante = min(equivalentes[q1], equivalentes[q2])
            for q in afd_completo.Q:
                if equivalentes[q] in (equivalentes[q1], equivalentes[q2]):
                    equivalentes[q] = representante

    # Passo 6: Criar o AFD minimizado
    novos_estados = set(equivalentes.values())
    novos_finais = {equivalentes[q] for q in afd_completo.F if q in equivalentes}
    
    nova_delta = {}
    for (q, simbolo), prox in afd_completo.delta.items():
        novo_q = equivalentes[q]
        novo_prox = equivalentes[prox]
        nova_delta[(novo_q, simbolo)] = novo_prox

    afd_minimizado = AFD(afd_completo.sigma, novos_estados, nova_delta, 
                        equivalentes[afd_completo.q0], novos_finais)
    
    return afd_minimizado

def obter_tabela_transicoes(afd):
    """
    Retorna uma representação em string da tabela de transições do AFD
    """
    # Ordena os estados e símbolos para consistência
    estados_ordenados = sorted(afd.Q)
    simbolos_ordenados = sorted(afd.sigma)
    
    # Cabeçalho da tabela
    tabela = "Tabela de Transições:\n"
    tabela += "Estado\t" + "\t".join(simbolos_ordenados) + "\n"
    
    # Linhas da tabela
    for estado in estados_ordenados:
        linha = estado + "\t"
        for simbolo in simbolos_ordenados:
            transicao = afd.delta.get((estado, simbolo), "∅")  # ∅ representa transição vazia
            linha += str(transicao) + "\t"
        tabela += linha + "\n"
    
    return tabela