document.getElementById("start-chat").addEventListener("click", function () {
  // Redireciona o usuário para o Telegram
  window.open("https://t.me/SEU_BOT_DO_TELEGRAM", "_blank");
});

document.getElementById("start-quiz").addEventListener("click", function () {
  alert("Você iniciou o quiz!");
});

// Função para buscar os próximos jogos da FURIA
async function buscarProximosJogos() {
  const response = await fetch("https://hltv-api.vercel.app/api/matches");
  const jogos = await response.json();

  const jogosFuria = jogos.filter(
    (jogo) =>
      jogo.team1.name.includes("FURIA") || jogo.team2.name.includes("FURIA")
  );

  const listaJogos = document.getElementById("jogos-lista");
  listaJogos.innerHTML = "";

  if (jogosFuria.length > 0) {
    jogosFuria.forEach((jogo) => {
      const jogoElement = document.createElement("div");
      jogoElement.innerHTML = `
              <p><strong>${jogo.event.name}</strong> - ${jogo.team1.name} vs ${
        jogo.team2.name
      }</p>
              <p><em>${new Date(jogo.date).toLocaleString()}</em></p>
          `;
      listaJogos.appendChild(jogoElement);
    });
  } else {
    listaJogos.innerHTML = "<p>Nenhum jogo da FURIA encontrado no momento.</p>";
  }
}

// Carrega os próximos jogos quando a página for carregada
window.onload = buscarProximosJogos;
