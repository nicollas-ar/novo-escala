(() => {
  const situacoes = [
    {
      pergunta: "Faltam cinco minutos para a missa e o leitor escalado ainda não chegou. E agora?",
      opcoes: ["Escolher a primeira pessoa que estiver perto do ambão.",
        "Avisar o responsável e confirmar quem está preparado para substituir.",
        "Esperar até a hora da leitura para resolver."],
      certa: 1,
      explicacao: "Avisar com antecedência dá tempo de confirmar a substituição e de a pessoa conferir a leitura."
    },
    {
      pergunta: "Antes da celebração, você vê que o Missal está aberto numa página diferente da que a equipe combinou. O que fazer?",
      opcoes: ["Confirmar com quem preparou o livro antes de mexer na marcação.",
        "Tirar todos os marcadores e deixar o livro fechado.",
        "Abrir na primeira página que tiver a data de hoje."],
      certa: 0,
      explicacao: "Conferir a marcação com quem preparou o Missal ajuda a evitar uma correção errada de última hora."
    },
    {
      pergunta: "Um coroinha novo diz que tem medo de esquecer o que precisa fazer. Como você ajuda?",
      opcoes: ["Entregar uma lista de todas as funções da equipe.",
        "Pedir que ele descubra a função observando na hora.",
        "Explicar a tarefa dele, combinar um sinal e indicar quem pode orientá-lo."],
      certa: 2,
      explicacao: "Uma orientação curta e um sinal discreto dão segurança a quem está começando."
    },
    {
      pergunta: "Você recebeu duas versões da escala com nomes diferentes para a mesma função. Em qual deve confiar?",
      opcoes: ["Na que chegou primeiro no grupo.",
        "Na versão que o coordenador confirmar como válida.",
        "Na que tiver mais pessoas marcadas."],
      certa: 1,
      explicacao: "Confirmar com o coordenador evita que duas pessoas se preparem para a mesma função ou que uma vaga fique descoberta."
    },
    {
      pergunta: "A passagem por onde a equipe vai entrar está bloqueada por cadeiras. Você percebe isso antes da missa. E agora?",
      opcoes: ["Avisar a equipe e combinar a liberação da passagem antes da entrada.",
        "Esperar a procissão chegar para pedir que tirem as cadeiras.",
        "Mudar sozinho o trajeto e esperar que os outros acompanhem."],
      certa: 0,
      explicacao: "Verificar o trajeto antes do início evita improvisos e permite avisar quem está organizando a entrada."
    },
    {
      pergunta: "Durante a missa, alguém da equipe parece em dúvida sobre a própria tarefa. Como ajudar?",
      opcoes: ["Chamar a pessoa em voz alta para ela notar.",
        "Atravessar imediatamente para dar uma explicação completa.",
        "Se for preciso intervir, usar o sinal combinado ou orientar discretamente."],
      certa: 2,
      explicacao: "Uma orientação discreta ajuda a equipe sem desviar a atenção da celebração."
    },
    {
      pergunta: "Você percebe, na véspera, que não vai conseguir servir na missa para a qual foi escalado. O que fazer?",
      opcoes: ["Avisar o coordenador assim que souber e confirmar o encaminhamento da substituição.",
        "Pedir a um amigo para ir no seu lugar sem avisar ninguém.",
        "Avisar só depois da missa para explicar o motivo."],
      certa: 0,
      explicacao: "Quanto mais cedo o aviso, mais tempo o coordenador tem para confirmar uma pessoa disponível e ajustar a escala."
    },
    {
      pergunta: "Durante a preparação, duas pessoas acham que ficaram responsáveis pela mesma tarefa. E agora?",
      opcoes: ["Deixar as duas começarem e decidir depois quem continua.",
        "Conferir a escala com o responsável e combinar a divisão antes do início.",
        "Decidir pela ordem de chegada sem consultar a equipe."],
      certa: 1,
      explicacao: "Confirmar quem faz cada tarefa evita trabalho duplicado e deixa claro quem deve agir na hora."
    },
    {
      pergunta: "Depois da missa, você encontra um material que não sabe onde guardar. O que faz?",
      opcoes: ["Guardar na gaveta mais próxima para liberar a bancada.",
        "Levar para casa e perguntar no próximo encontro.",
        "Perguntar à pessoa responsável pela sacristia onde ele deve ficar."],
      certa: 2,
      explicacao: "Guardar cada material no local combinado ajuda a próxima equipe a encontrar tudo para a celebração."
    },
    {
      pergunta: "O mesmo desencontro de comunicação aconteceu em duas missas seguidas. Qual é o melhor momento para conversar?",
      opcoes: ["Depois da celebração, com calma, para combinar um ajuste com a equipe.",
        "No meio da missa, assim que o desencontro acontecer.",
        "Na próxima celebração, sem conversar antes, para ver se alguém percebe."],
      certa: 0,
      explicacao: "Revisar juntos o que ocorreu depois da missa permite acertar um sinal ou uma divisão de tarefas para a próxima vez."
    }
  ];

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

  let indice = 0;
  let acertos = 0;

  function mostrarSituacao(moverFoco) {
    const atual = situacoes[indice];
    progresso.textContent = "Situação " + (indice + 1) + " de " + situacoes.length;
    pergunta.textContent = atual.pergunta;
    opcoes.replaceChildren();
    feedback.textContent = "";
    feedback.className = "";
    continuar.hidden = true;

    atual.opcoes.forEach((texto, numero) => {
      const botao = document.createElement("button");
      botao.type = "button";
      botao.className = "btn btn-contorno";
      botao.textContent = texto;
      botao.addEventListener("click", () => responder(atual, numero));
      opcoes.append(botao);
    });

    if (moverFoco) pergunta.focus();
  }

  function responder(atual, numero) {
    if (!continuar.hidden) return;
    const acertou = numero === atual.certa;
    if (acertou) acertos++;

    Array.from(opcoes.children).forEach((botao, posicao) => {
      botao.disabled = true;
      if (posicao === atual.certa) botao.className = "btn btn-verde";
      else if (posicao === numero) botao.className = "btn btn-vinho";
    });

    const inicio = acertou ? "Acertou! " : "Melhor resposta: " + atual.opcoes[atual.certa] + " ";
    feedback.className = acertou ? "aviso aviso-ok" : "aviso aviso-aviso";
    feedback.textContent = inicio + atual.explicacao;
    proxima.textContent = indice + 1 === situacoes.length ? "Ver resultado" : "Próxima situação";
    continuar.hidden = false;
    proxima.focus();
  }

  proxima.addEventListener("click", () => {
    if (continuar.hidden) return;
    indice++;
    if (indice < situacoes.length) {
      mostrarSituacao(true);
    } else {
      rodada.hidden = true;
      resultado.hidden = false;
      pontuacao.textContent = "Você acertou " + acertos + " de " + situacoes.length + " situações.";
      pontuacao.focus();
    }
  });

  elemento("reiniciar").addEventListener("click", () => {
    indice = 0;
    acertos = 0;
    resultado.hidden = true;
    rodada.hidden = false;
    mostrarSituacao(true);
  });

  document.getElementById("e-agora").hidden = false;
  mostrarSituacao(false);
})();
