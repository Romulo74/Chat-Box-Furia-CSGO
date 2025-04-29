import requests
import random
from random import choice
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
)

# --- Dados dos jogadores ---
JOGADORES = {
    "KSCERATO": "Função: Rifler | Destaque: Clutch Master",
    "Yuurih": "Função: Entry Fragger | Destaque: First bloods",
    "Chelo": "Função: Support | Destaque: Estratégia sólida"
}

# --- Perguntas do quiz ---
quiz_perguntas = [
  
    {
        "pergunta": "Qual é o nome do mapa mais antigo do CS:GO?",
        "opcoes": ["Dust2", "Mirage", "Inferno", "Nuke"],
        "resposta": "Dust2"
    },
    {
        "pergunta": "O que significa 'eco round' no CS:GO?",
        "opcoes": [
            "Rodada com economia de dinheiro",
            "Rodada com armas pesadas",
            "Rodada sem bomb",
            "Rodada de empate"
        ],
        "resposta": "Rodada com economia de dinheiro"
    },
    {
        "pergunta": "Quantos jogadores compõem um time no competitivo de CS:GO?",
        "opcoes": ["4", "5", "6", "7"],
        "resposta": "5"
    },
    {
        "pergunta": "Qual é a função de um 'AWPer' em uma equipe?",
        "opcoes": [
            "Usar granadas",
            "Usar armas automáticas",
            "Sniper principal",
            "Iniciar rush"
        ],
        "resposta": "Sniper principal"
    },
    {
        "pergunta": "Qual time brasileiro venceu o Major de CS:GO em 2016?",
        "opcoes": ["FURIA", "MIBR", "SK Gaming", "Imperial"],
        "resposta": "SK Gaming"
    },
    {
        "pergunta": "Em qual mapa é mais comum usar táticas no bombsite B primeiro?",
        "opcoes": ["Nuke", "Dust2", "Overpass", "Mirage"],
        "resposta": "Mirage"
    },
    {
        "pergunta": "O que acontece quando você é 'flashado' no CS:GO?",
        "opcoes": [
            "Seu som some",
            "Você morre instantaneamente",
            "Sua tela fica branca temporariamente",
            "Você ganha velocidade"
        ],
        "resposta": "Sua tela fica branca temporariamente"
    }
]

# --- Buscar jogos da FURIA ---
def buscar_proximos_jogos():
    url = "https://hltv-api.vercel.app/api/matches"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        jogos_furia = [
            jogo for jogo in dados
            if 'FURIA' in jogo['team1']['name'] or 'FURIA' in jogo['team2']['name']
        ]
        return jogos_furia
    return []

# --- Comandos do bot ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🔥 Bem-vindo ao FURIA Fan Chat! 🔥\n\n"
        "Comandos disponíveis:\n"
        "/proximojogo - Ver o próximo jogo\n"
        "/torcida - Simular torcida\n"
        "/jogadores - Ver jogadores\n"
        "/quiz - Responder perguntas\n"
        "/placar - Ver sua pontuação"
    )
    await update.message.reply_text(msg)

async def proximojogo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jogos = buscar_proximos_jogos()
    if jogos:
        jogo = jogos[0]
        msg = (
            f"📆 Próximo jogo:\n"
            f"🏆 Evento: {jogo['event']['name']}\n"
            f"🆚 {jogo['team1']['name']} vs {jogo['team2']['name']}\n"
            f"🕓 Data/Hora: {jogo['date']}\n"
        )
    else:
        msg = "❌ Nenhum jogo da FURIA encontrado no momento."
    await update.message.reply_text(msg)

async def torcida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    frases = [
        "💥 VAMO FURIAAAA!",
        "🔥 É clutch ou é eco!",
        "🎯 Confia no KSCERATO!",
        "🐍 A tropa da FURIA tá on fire!"
    ]
    await update.message.reply_text(choice(frases))

async def jogadores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📋 Jogadores da FURIA:\n"
    for nome, desc in JOGADORES.items():
        msg += f"\n⭐ {nome} - {desc}"
    await update.message.reply_text(msg)

# --- Comando /quiz ---
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pergunta = random.choice(quiz_perguntas)
    context.user_data["resposta_certa"] = pergunta["resposta"]

    keyboard = [
        [InlineKeyboardButton(text=opcao, callback_data=opcao)]
        for opcao in pergunta["opcoes"]
    ]

    await update.message.reply_text(
        text=pergunta["pergunta"],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- Resposta do quiz ---
async def resposta_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    resposta_usuario = query.data
    resposta_certa = context.user_data.get("resposta_certa")

    if resposta_usuario == resposta_certa:
        context.user_data["pontos"] = context.user_data.get("pontos", 0) + 1
        await query.edit_message_text(
            f"✅ Resposta correta! 🔥\n\nSeu placar: {context.user_data['pontos']} ponto(s)."
        )
    else:
        await query.edit_message_text(
            f"❌ Resposta errada. A certa era: {resposta_certa}\n\nSeu placar continua: {context.user_data.get('pontos', 0)} ponto(s)."
        )

# --- Comando /placar ---
async def placar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pontos = context.user_data.get("pontos", 0)
    await update.message.reply_text(f"📊 Seu placar atual é: {pontos} ponto(s).")

# --- Execução do bot ---
if __name__ == "__main__":
    TOKEN = "Token telegram"  # Substitua se necessário

    app = ApplicationBuilder().token(TOKEN).build()

    # Adicionando todos os comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("proximojogo", proximojogo))
    app.add_handler(CommandHandler("torcida", torcida))
    app.add_handler(CommandHandler("jogadores", jogadores))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CallbackQueryHandler(resposta_quiz))
    app.add_handler(CommandHandler("placar", placar))

    print("🤖 Bot da FURIA rodando...")
    app.run_polling()
