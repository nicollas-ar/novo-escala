import { situacoes } from "./e-agora-questoes.js";

(() => {
  const elemento = (nome) => document.getElementById("e-agora-" + nome);
  const pergunta = elemento("pergunta");
  const progresso = elemento("progresso");
  const opcoes = elemento("opcoes");
  const feedback = elemento("feedback");
  const continuar = elemento("continuar");
  const proxima = elemento("proxima");
  const rodada = elemento("rodada");
  const resultado = elemento("resultado");
  const pontuacao = elemento("pontuacao");

  const tamanhoRodada = 10;
  let indice = 0;
  let acertos = 0;
  let perguntas;

  function embaralhar(itens) {
    const lista = [...itens];
    for (let i = lista.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [lista[i], lista[j]] = [lista[j], lista[i]];
    }
    return lista;
  }

  function mostrarSituacao(moverFoco) {
    const [enunciado, correta, alternativaA, alternativaB, explicacao] = perguntas[indice];
    const alternativas = embaralhar([correta, alternativaA, alternativaB]);
    progresso.textContent = "Situação " + (indice + 1) + " de " + perguntas.length;
    pergunta.textContent = enunciado;
    opcoes.replaceChildren();
    feedback.textContent = "";
    feedback.className = "";
    continuar.hidden = true;

    alternativas.forEach((texto) => {
      const botao = document.createElement("button");
      botao.type = "button";
      botao.className = "btn btn-contorno";
      botao.textContent = texto;
      botao.addEventListener("click", () => responder(correta, texto, explicacao));
      opcoes.append(botao);
    });

    if (moverFoco) pergunta.focus();
  }

  function responder(correta, escolhida, explicacao) {
    if (!continuar.hidden) return;
    const acertou = escolhida === correta;
    if (acertou) acertos++;

    Array.from(opcoes.children).forEach((botao) => {
      botao.disabled = true;
      if (botao.textContent === correta) botao.className = "btn btn-verde";
      else if (botao.textContent === escolhida) botao.className = "btn btn-vinho";
    });

    const inicio = acertou ? "Acertou! " : "Melhor resposta: " + correta + " ";
    feedback.className = acertou ? "aviso aviso-ok" : "aviso aviso-aviso";
    feedback.textContent = inicio + explicacao;
    proxima.textContent = indice + 1 === perguntas.length ? "Ver resultado" : "Próxima situação";
    continuar.hidden = false;
    proxima.focus();
  }

  proxima.addEventListener("click", () => {
    if (continuar.hidden) return;
    indice++;
    if (indice < perguntas.length) {
      mostrarSituacao(true);
    } else {
      rodada.hidden = true;
      resultado.hidden = false;
      pontuacao.textContent = "Você acertou " + acertos + " de " + perguntas.length + " situações.";
      pontuacao.focus();
    }
  });

  function iniciar(moverFoco) {
    perguntas = embaralhar(situacoes).slice(0, tamanhoRodada);
    indice = 0;
    acertos = 0;
    resultado.hidden = true;
    rodada.hidden = false;
    mostrarSituacao(moverFoco);
  }

  elemento("reiniciar").addEventListener("click", () => iniciar(true));
  document.getElementById("e-agora").hidden = false;
  iniciar(false);
})();
