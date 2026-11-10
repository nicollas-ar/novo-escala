function quebrarTexto(contexto, texto, largura) {
  return texto.split(/\r?\n/).flatMap((paragrafo) => {
    const linhas = [];
    let linha = "";
    for (const palavra of paragrafo.trim().split(/\s+/)) {
      const candidata = linha ? linha + " " + palavra : palavra;
      if (linha && contexto.measureText(candidata).width > largura) {
        linhas.push(linha);
        linha = "";
      }
      if (contexto.measureText(palavra).width <= largura) {
        linha = linha ? linha + " " + palavra : palavra;
        continue;
      }
      for (const letra of palavra) {
        if (contexto.measureText(linha + letra).width > largura) {
          linhas.push(linha);
          linha = "";
        }
        linha += letra;
      }
    }
    linhas.push(linha);
    return linhas;
  });
}

function desenharCartao(missa) {
  const canvas = document.createElement("canvas");
  const contexto = canvas.getContext("2d");
  const largura = 1000;
  const margem = 64;
  const textoLargura = largura - margem * 2;
  const blocos = [];
  let y = 65;

  function texto(valor, fonte, cor, altura, x = margem, espaco = textoLargura) {
    contexto.font = fonte;
    const linhas = quebrarTexto(contexto, valor, espaco);
    const topo = y;
    blocos.push(() => {
      contexto.font = fonte;
      contexto.fillStyle = cor;
      linhas.forEach((linha, i) => contexto.fillText(linha, x, topo + i * altura));
    });
    y += linhas.length * altura;
  }

  texto("PARÓQUIA SANTO ANTÔNIO DO LIMÃO", "bold 26px sans-serif", "#fbe9ae", 44);
  texto("Escala de cerimoniários", "bold 58px sans-serif", "#fffaf0", 72);
  texto(missa.nome, "bold 42px sans-serif", "#fffaf0", 54);
  texto(missa.quando, "32px sans-serif", "#fffaf0", 44);
  const fimCabecalho = y + 35;
  y = fimCabecalho + 42;

  for (const pessoa of missa.equipe) {
    const topo = y - 13;
    const indice = blocos.length;
    texto(pessoa[0], "bold 38px sans-serif", "#174631", 46, margem + 22, textoLargura - 44);
    texto(pessoa[1], "31px sans-serif", "#54493e", 38, margem + 22, textoLargura - 44);
    const altura = y - topo + 9;
    blocos.splice(indice, 0, () => {
      contexto.fillStyle = "#f1ebda";
      contexto.fillRect(margem, topo, textoLargura, altura);
    });
    y += 26;
  }

  if (missa.recado) {
    y += 10;
    texto("Recado", "bold 34px sans-serif", "#6c1d2c", 45);
    texto(missa.recado, "30px sans-serif", "#2b2622", 40);
  }

  const altura = y + 35;
  const proporcao = Math.min(1, 4096 / altura);
  canvas.width = Math.ceil(largura * proporcao);
  canvas.height = Math.ceil(altura * proporcao);
  contexto.scale(proporcao, proporcao);
  contexto.textBaseline = "top";
  contexto.fillStyle = "#fffaf0";
  contexto.fillRect(0, 0, largura, altura);
  contexto.fillStyle = "#174631";
  contexto.fillRect(0, 0, largura, fimCabecalho);
  contexto.fillStyle = "#f2b61c";
  contexto.fillRect(0, fimCabecalho, largura, 8);
  blocos.forEach((desenhar) => desenhar());

  // Gera o arquivo no próprio clique para preservar a ativação exigida pelo compartilhamento.
  const base64 = canvas.toDataURL("image/png").split(",")[1];
  const bytes = Uint8Array.from(atob(base64), (caractere) => caractere.charCodeAt(0));
  return new File([bytes], "escala-" + missa.data + ".png", { type: "image/png" });
}

document.querySelectorAll("[data-cartao-escala]").forEach((botao) => {
  botao.addEventListener("click", async () => {
    const aviso = botao.nextElementSibling;
    aviso.textContent = "";
    botao.disabled = true;
    try {
      const missa = JSON.parse(botao.dataset.cartaoEscala);
      const arquivo = desenharCartao(missa);
      const dados = { files: [arquivo] };
      if (navigator.share && navigator.canShare && navigator.canShare(dados)) {
        try {
          await navigator.share(dados);
          return;
        } catch (erro) {
          if (erro.name === "AbortError") return;
        }
      }

      const url = URL.createObjectURL(arquivo);
      const link = document.createElement("a");
      link.href = url;
      link.download = arquivo.name;
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 60000);
      aviso.textContent = "Cartão baixado. Anexe a imagem na conversa do WhatsApp.";
    } catch (erro) {
      aviso.textContent = "Não foi possível gerar o cartão. Tente novamente.";
    } finally {
      botao.disabled = false;
    }
  });
});
