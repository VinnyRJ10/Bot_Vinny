# botvinny_barbeiro_v5.py - Bot Profissional Barbearia Bigode com horários naturais

import random
import re

# Lista de palavras iniciais / cumprimentos
palavras_iniciais = [
    "oi", "olá", "bom dia", "boa tarde", "boa noite", "e aí",
    "fala", "opa", "hey", "blz", "tudo bem", "como vai", "como tá"
]

# Palavras de agendamento
palavras_agendamento = [
    "marcar", "agendar", "horário", "consulta", "vaga", "atendimento"
]

# Lista de barbeiros
barbeiros = ["adriano", "gordo"]

# Turnos de cada barbeiro (hora início, hora fim em 24h)
turnos = {
    "adriano": (7, 19),   # 7h às 19h
    "gordo": (13, 25)     # 13h às 1h da manhã (25 equivale a 1h)
}

# Serviços e preços
servicos_precos = {
    "fixit barba": 30,
    "fixit cabelo": 30,
    "fixit barba e cabelo": 50,
    "neuvoux barba": 40,
    "neuvoux cabelo": 60
}

# Palavras de serviços
palavras_servicos = [
    "fixit", "neuvoux", "barba", "cabelo", "outros procedimentos"
]

# Respostas de cumprimentos
respostas_cumprimento = [
    "Oi! Tudo bem com você? Quer marcar um horário com nossos barbeiros?",
    "Olá! Que bom te ver! Posso te ajudar a agendar com Adriano ou Gordo?",
    "Ei! Tudo certo? Me conta, você quer marcar com qual barbeiro?"
]

# Respostas padrão
respostas_default = [
    "Desculpa, não entendi. Pode repetir?",
    "Interessante! Pode explicar melhor?",
    "Hmm... não entendi direito, me conta mais!"
]

# Agenda simulada: {barbeiro: {dia: [horários ocupados]}}
agenda = {
    "adriano": {},
    "gordo": {}
}

# Função para converter horário natural para formato 24h "HH:MM"
def parse_horario(horario_texto):
    # Remove "às" ou espaços
    h = horario_texto.lower().replace("às", "").strip()
    # Padrão hh ou hh:mm
    match = re.match(r"(\d{1,2})([:h]?(\d{1,2})?)?", h)
    if match:
        hora = int(match.group(1))
        minuto = match.group(3)
        minuto = int(minuto) if minuto else 0
        return f"{hora:02d}:{minuto:02d}"
    return None

# Função para validar horário dentro do turno
def horario_valido(barbeiro, horario):
    hora_int = int(horario.split(":")[0])
    if barbeiro == "gordo" and hora_int < turnos[barbeiro][0]:
        hora_int += 24
    inicio, fim = turnos[barbeiro]
    return inicio <= hora_int < fim

# Função para agendar horário
def agendar_horario(barbeiro, dia, horario_texto):
    horario = parse_horario(horario_texto)
    if not horario:
        return "Não consegui entender o horário. Use formato 14h ou 14:30."
    if not horario_valido(barbeiro, horario):
        return f"Desculpa, {barbeiro.title()} não trabalha nesse horário. Confira o turno dele."
    if dia not in agenda[barbeiro]:
        agenda[barbeiro][dia] = []
    if horario in agenda[barbeiro][dia]:
        return f"Desculpa, {barbeiro.title()} já tem um horário às {horario} neste dia."
    agenda[barbeiro][dia].append(horario)
    return f"Confirmado! {barbeiro.title()} às {horario} no dia {dia}. Até lá!"

# Função principal para responder mensagens
def responder(mensagem):
    msg = mensagem.lower().strip()
    
    # Cumprimentos
    for palavra in palavras_iniciais:
        if msg.startswith(palavra):
            return random.choice(respostas_cumprimento)
    
    # Interesse em serviços
    for palavra in palavras_servicos:
        if palavra in msg:
            for servico in servicos_precos:
                if servico in msg:
                    return f"O serviço {servico.title()} custa R${servicos_precos[servico]}."
            if "outros procedimentos" in msg:
                return "Para outros procedimentos, consulte diretamente o barbeiro."
            return "Quer saber os preços dos nossos serviços Fixit ou Neuvoux, ou outros procedimentos?"
    
    # Agendamento
    for palavra in palavras_agendamento:
        if palavra in msg:
            for barbeiro in barbeiros:
                if barbeiro in msg:
                    return f"Perfeito! Vamos agendar com {barbeiro.title()}. Me diga o dia e horário desejado (ex: 20/02 às 14h)."
            return "Com qual barbeiro você quer marcar, Adriano ou Gordo?"
    
    # Confirmação de horário no formato natural: "adriano 20/02 14h"
    partes = msg.split()
    if len(partes) == 3:
        b, d, h = partes
        if b in barbeiros:
            return agendar_horario(b, d, h)
    
    # Se não reconhecer
    return random.choice(respostas_default)

# Teste rápido
if __name__ == "__main__":
    print("Bot Vinny da Barbearia Bigode iniciado! Escreva 'sair' para encerrar.")
    while True:
        entrada = input("Você: ")
        if entrada.lower() == "sair":
            print("Bot: Até mais! Volte sempre à Barbearia Bigode!")
            break
        resposta = responder(entrada)
        print("Bot:", resposta)
