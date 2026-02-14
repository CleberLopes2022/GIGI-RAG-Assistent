const chatHistory = document.getElementById("chat-history");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");

let baseConhecimento = [];

const respostasPadrao = [
  "Hmm... não entendi muito bem 🤔. Pode tentar reformular?",
  "Desculpe, não consegui compreender 🧠. Pode dizer de outro jeito?",
  "Acho que não peguei isso direito 😅. Pode explicar novamente?"
];

// Carregar o JSON base_conhecimento.json ao iniciar
fetch('base_conhecimento.json')
  .then(response => response.json())
  .then(data => {
    baseConhecimento = data;
  })
  .catch(() => {
    console.error('Erro ao carregar base_conhecimento.json');
  });

chatForm.addEventListener("submit", function (e) {
  e.preventDefault();
  const pergunta = userInput.value.trim();
  if (pergunta === "") return;

  adicionarMensagem("Você", pergunta);
  const resposta = gerarResposta(pergunta);
  adicionarMensagem("GIGI", resposta);
  userInput.value = "";
});

function adicionarMensagem(remetente, mensagem) {
  const msgDiv = document.createElement("div");
    // Define classe conforme o remetente
  if (remetente.toLowerCase() === "usuário" || remetente.toLowerCase() === "você") {
    msgDiv.classList.add("mensagem-usuario");
  } else {
    msgDiv.classList.add("mensagem-bot");
  }
  
  msgDiv.innerHTML = `<strong>${remetente}:</strong> ${mensagem}`;
  chatHistory.appendChild(msgDiv);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

function normalizarTexto(texto) {
  return texto
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "") // remove acentos
    .replace(/[^\w\s]/gi, "") // remove pontuação
    .trim();
}

function gerarResposta(pergunta) {
  const perguntaNormalizada = normalizarTexto(pergunta);

  let melhorCorrespondencia = null;
  let maiorSimilaridade = 0;

  for (const item of baseConhecimento) {
    const perguntaBase = normalizarTexto(item.pergunta);
    const palavrasPergunta = perguntaNormalizada.split(" ");
    const palavrasBase = perguntaBase.split(" ");

    const intersecao = palavrasPergunta.filter(p => palavrasBase.includes(p));
    const similaridade = intersecao.length / palavrasBase.length;

    if (similaridade > maiorSimilaridade) {
      maiorSimilaridade = similaridade;
      melhorCorrespondencia = item;
    }
  }

  if (melhorCorrespondencia && maiorSimilaridade > 0.4) {
    return melhorCorrespondencia.resposta;
  }

  return respostasPadrao[Math.floor(Math.random() * respostasPadrao.length)];
}

