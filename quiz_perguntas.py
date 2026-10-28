"""Banco de perguntas do quiz.

Formato de cada linha:  pergunta|resposta certa|errada 1|errada 2|errada 3
(não use o caractere "|" dentro dos textos). Para acrescentar perguntas, basta
incluir novas linhas em FACIL, MEDIO ou DIFICIL. A ordem das perguntas e das
alternativas é sorteada a cada rodada, então a posição aqui não importa.
"""

FACIL = r'''
Qual objeto litúrgico guarda a água e o vinho usados na missa?|As galhetas|O turíbulo|A naveta|O sacrário
Em qual recipiente o vinho é consagrado na missa?|No cálice|Na patena|Na galheta|No cibório
Qual objeto é usado para queimar o incenso?|O turíbulo|A naveta|O aspersório|O círio
Como se chama o pequeno recipiente que guarda o incenso antes de ele ser colocado no turíbulo?|Naveta|Galheta|Cibório|Aspersório
Onde ficam guardadas as hóstias consagradas na igreja?|No sacrário|Na credência|No ambão|Na sacristia
Qual livro contém as orações da missa?|O Missal|O Lecionário|O Hinário|O Catecismo
Qual livro contém as leituras bíblicas proclamadas na missa?|O Lecionário|O Missal|O Catecismo|O Ritual de Bênçãos
Como se chama o local de onde é proclamada a Palavra de Deus?|Ambão|Altar|Credência|Sacrário
Como se chama a mesa onde o padre celebra a Eucaristia?|Altar|Ambão|Credência|Batistério
Qual é a veste branca usada pelos coroinhas e cerimoniários?|Alva|Casula|Dalmática|Mitra
Qual veste o padre usa por cima da alva, mudando de cor conforme o tempo litúrgico?|Casula|Pálio|Solidéu|Capelo
Como se chama a faixa que o padre coloca em volta do pescoço?|Estola|Cíngulo|Pala|Manípulo
Qual objeto é usado para aspergir (espalhar) água benta?|Aspersório|Turíbulo|Báculo|Patena
Qual cor litúrgica é usada no Advento e na Quaresma?|Roxo|Verde|Vermelho|Branco
Qual cor litúrgica é usada no Tempo Comum?|Verde|Roxo|Branco|Vermelho
Qual cor litúrgica é usada no Natal e na Páscoa?|Branco|Verde|Roxo|Preto
Qual cor litúrgica é usada no Domingo de Pentecostes?|Vermelho|Azul|Verde|Roxo
Qual cor litúrgica é usada nas festas de mártires?|Vermelho|Verde|Roxo|Rosa
Quantos sacramentos tem a Igreja Católica?|Sete|Cinco|Dez|Doze
Qual é o primeiro sacramento que uma pessoa recebe?|Batismo|Crisma|Eucaristia|Matrimônio
Qual elemento é essencial para o sacramento do Batismo?|Água|Vinho|Fogo|Terra
Em que se transformam o pão e o vinho na consagração?|No Corpo e no Sangue de Cristo|Em água benta|Em símbolos sem presença real|Em alimento comum abençoado
Quantos livros tem a Bíblia católica?|73|66|27|46
Quantos livros tem o Novo Testamento?|27|46|39|12
Qual é o primeiro livro da Bíblia?|Gênesis|Êxodo|Salmos|Mateus
Qual é o último livro da Bíblia?|Apocalipse|Atos dos Apóstolos|Judas|Malaquias
Quantos são os evangelistas?|Quatro|Três|Doze|Sete
Qual destes é um dos quatro evangelistas?|Lucas|Paulo|Pedro|Barnabé
Quantos apóstolos Jesus escolheu?|Doze|Sete|Setenta|Dez
Quem foi o primeiro papa?|São Pedro|São Paulo|São João|Santo André
Qual apóstolo traiu Jesus?|Judas Iscariotes|Tomé|Pedro|Filipe
Em qual cidade Jesus nasceu?|Belém|Nazaré|Jerusalém|Cafarnaum
Em qual cidade Jesus cresceu?|Nazaré|Belém|Jericó|Betânia
Quem batizou Jesus no rio Jordão?|João Batista|Pedro|Zacarias|Elias
Qual foi o primeiro milagre de Jesus relatado no Evangelho de João?|Transformou água em vinho em Caná|Multiplicou os pães|Curou um cego|Ressuscitou Lázaro
Em qual dia da semana celebramos a Ressurreição do Senhor?|Domingo|Sábado|Sexta-feira|Quinta-feira
Quantos dias dura a Quaresma?|40 dias|30 dias|50 dias|7 dias
Em qual dia começa a Quaresma?|Quarta-feira de Cinzas|Domingo de Ramos|Sexta-feira Santa|Domingo de Páscoa
Como se chama o domingo que antecede a Páscoa?|Domingo de Ramos|Pentecostes|Corpus Christi|Epifania
Em qual data celebramos o Natal?|25 de dezembro|24 de dezembro|1º de janeiro|6 de janeiro
Quem anunciou a Maria que ela seria mãe de Jesus?|O anjo Gabriel|O anjo Miguel|O anjo Rafael|São José
Qual é o nome do esposo de Maria?|José|Joaquim|Zacarias|Simeão
Quais presentes os Reis Magos levaram ao Menino Jesus?|Ouro, incenso e mirra|Ouro, prata e bronze|Mirra, vinho e pão|Incenso, azeite e mel
Quem é a padroeira do Brasil?|Nossa Senhora Aparecida|Nossa Senhora de Fátima|Nossa Senhora de Lourdes|Nossa Senhora do Carmo
Em que data se celebra Nossa Senhora Aparecida?|12 de outubro|8 de dezembro|15 de agosto|13 de maio
Em que data se celebra Santo Antônio?|13 de junho|24 de junho|29 de junho|4 de outubro
Pelo que Santo Antônio é invocado popularmente?|Para encontrar objetos perdidos|Para proteger marinheiros|Para curar dor de dente|Para proteger os músicos
Santo Antônio de Pádua foi frade da ordem fundada por qual santo?|São Francisco de Assis|São Domingos|Santo Inácio de Loyola|São Bento
Quem é o padroeiro dos coroinhas?|São Tarcísio|São Cristóvão|São Judas Tadeu|São Lourenço
Qual santo, amigo dos animais, nasceu em Assis e fundou os franciscanos?|São Francisco de Assis|Santo Antônio|São Bento|São Tomás de Aquino
Qual oração começa com "Ave, Maria, cheia de graça"?|Ave-Maria|Salve-Rainha|Glória|Credo
Qual oração Jesus ensinou aos apóstolos?|Pai-Nosso|Ave-Maria|Creio em Deus Pai|Glória ao Pai
Quantos são os mandamentos da Lei de Deus (Decálogo)?|Dez|Sete|Doze|Cinco
Quem recebeu de Deus os Dez Mandamentos no monte Sinai?|Moisés|Abraão|Davi|Elias
Quem construiu a arca para sobreviver ao dilúvio?|Noé|Moisés|Abraão|Jonas
Qual jovem derrotou o gigante Golias?|Davi|Sansão|Saul|Josué
Quem passou três dias dentro de um grande peixe?|Jonas|Daniel|Jó|Tobias
Quem foi lançado na cova dos leões?|Daniel|José do Egito|Elias|Sansão
Quantas dezenas tem um terço?|Cinco|Três|Dez|Quinze
Os mistérios do Rosário são gozosos, luminosos, dolorosos e...?|Gloriosos|Alegres|Santos|Eucarísticos
O que significa "Aleluia"?|Louvai ao Senhor|Senhor, tende piedade|Assim seja|Santo, santo, santo
O que significa "Amém"?|Assim seja|Louvado seja|Vá em paz|Glória a Deus
O que significa "Kyrie, eleison"?|Senhor, tende piedade|Glória a Deus|Cordeiro de Deus|Corações ao alto
O que significa a palavra "Eucaristia"?|Ação de graças|Pão do céu|Ceia pascal|Comunhão dos santos
Qual parte da missa vem logo depois da homilia, aos domingos?|Profissão de fé (Credo)|Ato penitencial|Rito da paz|Bênção final
Qual gesto se faz diante do Santíssimo Sacramento no sacrário?|Genuflexão|Aplauso|Sinal da paz|Apenas um aceno de mão
Qual é a última parte da missa?|Ritos finais|Liturgia da Palavra|Liturgia Eucarística|Ritos iniciais
Quais são as duas grandes partes centrais da missa?|Liturgia da Palavra e Liturgia Eucarística|Ritos iniciais e ritos finais|Homilia e Credo|Oferendas e Paz
Quem é o sucessor de São Pedro e chefe visível da Igreja Católica?|O papa|O cardeal|O bispo diocesano|O diácono
Em qual cidade fica o Vaticano?|Roma|Milão|Assis|Jerusalém
Qual cor de fumaça indica que um novo papa foi eleito?|Branca|Preta|Vermelha|Azul
Como se chama a reunião dos cardeais que elege o papa?|Conclave|Sínodo|Concílio|Consistório
Qual é o grau mais alto do sacramento da Ordem?|Bispo|Diácono|Acólito|Leitor
Como se chama o chapéu pontudo usado pelo bispo nas celebrações?|Mitra|Solidéu|Barrete|Capelo
Como se chama o bastão pastoral do bispo?|Báculo|Cetro|Lança|Pálio
Qual sacramento perdoa os pecados?|Penitência (Confissão)|Unção dos Enfermos|Crisma|Matrimônio
Qual sacramento é celebrado pelos noivos?|Matrimônio|Ordem|Crisma|Unção dos Enfermos
Qual sacramento conforta e fortalece os doentes?|Unção dos Enfermos|Batismo|Crisma|Penitência
Qual sacramento também é chamado de Crisma?|Confirmação|Batismo|Ordem|Eucaristia
Qual tempo litúrgico prepara a Igreja para o Natal?|Advento|Quaresma|Tempo Pascal|Tempo Comum
Quantos domingos tem o Advento?|Quatro|Seis|Dois|Sete
Como se chama a grande vela acesa na Vigília Pascal?|Círio Pascal|Vela do Advento|Lamparina do sacrário|Vela de batismo
Qual é a cor opcional do 3º domingo do Advento (Gaudete)?|Rosa|Azul|Dourado|Cinza
O que indica a lamparina acesa perto do sacrário?|A presença de Cristo na Eucaristia|Que a missa vai começar|Que há confissões|Que é domingo
Como se chama o lugar onde os fiéis se confessam?|Confessionário|Sacristia|Credência|Átrio
Como se chama o local onde se guardam as vestes e os objetos litúrgicos?|Sacristia|Presbitério|Nave|Batistério
Como se chama a mesinha lateral onde ficam galhetas e cálice antes do ofertório?|Credência|Ambão|Cátedra|Batistério
Como se chama a parte da igreja onde fica a assembleia?|Nave|Abside|Sacristia|Presbitério
Como se chama a pia onde se batiza?|Pia batismal|Lavabo|Crismeira|Cibório
Qual é o nome do servidor que leva a cruz processional?|Cruciferário|Turiferário|Ceroferário|Naveteiro
Qual é o nome do servidor que leva o turíbulo?|Turiferário|Cruciferário|Ceroferário|Mitrífero
Qual é o nome do servidor que leva as velas (tochas) na procissão?|Ceroferário|Turiferário|Cruciferário|Naveteiro
Qual dia da Semana Santa lembra a Última Ceia e o lava-pés?|Quinta-feira Santa|Sexta-feira Santa|Sábado Santo|Domingo de Ramos
Em qual dia lembramos a morte de Jesus na cruz?|Sexta-feira Santa|Quinta-feira Santa|Domingo de Ramos|Sábado Santo
Qual celebração, na noite do Sábado Santo, anuncia a Ressurreição e começa com a bênção do fogo novo?|Vigília Pascal|Missa do Crisma|Via-Sacra|Domingo de Ramos
Qual festa celebra a vinda do Espírito Santo sobre os apóstolos?|Pentecostes|Epifania|Ascensão|Corpus Christi
Qual festa celebra a presença real de Cristo na Eucaristia, com procissão e tapetes de rua?|Corpus Christi|Cristo Rei|Epifania|Pentecostes
Qual festa celebra a visita dos Reis Magos?|Epifania|Ascensão|Assunção|Transfiguração
Quantos dias depois da Páscoa, segundo Atos dos Apóstolos, Jesus subiu ao céu?|40 dias|3 dias|50 dias|7 dias
Qual apóstolo duvidou da Ressurreição até ver as chagas de Jesus?|Tomé|Pedro|Filipe|Mateus
Qual evangelista é simbolizado pela águia?|João|Marcos|Lucas|Mateus
Qual evangelista é simbolizado pelo leão?|Marcos|Lucas|João|Mateus
Qual evangelista, segundo a tradição, era médico?|Lucas|Marcos|Mateus|João
Quem escreveu o livro dos Atos dos Apóstolos?|Lucas|Paulo|Pedro|Tiago
Qual apóstolo era cobrador de impostos antes de seguir Jesus?|Mateus|João|André|Tadeu
Quem foi chamado de "Apóstolo dos gentios"?|São Paulo|São Pedro|São Tiago|São Barnabé
Qual oração começa com "Creio em Deus Pai todo-poderoso"?|Credo|Glória|Santo|Salve-Rainha
Qual oração começa com "Salve, Rainha, Mãe de misericórdia"?|Salve-Rainha|Ave-Maria|Magnificat|Pai-Nosso
Como é chamada a missa celebrada à meia-noite do Natal?|Missa do Galo|Missa do Crisma|Missa de Sétimo Dia|Missa Pascal
O que é a homilia?|A explicação da Palavra de Deus feita pelo ministro ordenado|O Pai-Nosso|O cântico de entrada|A coleta das ofertas
Qual é o livro sagrado dos cristãos?|A Bíblia|O Alcorão|Os Vedas|O Talmude
Quais são as três pessoas da Santíssima Trindade?|Pai, Filho e Espírito Santo|Pai, Maria e José|Pai, Filho e anjo Gabriel|Deus, Maria e Jesus
Qual animal costuma representar o Espírito Santo?|A pomba|O cordeiro|A águia|O leão
Em qual dia a Igreja celebra todos os santos?|1º de novembro|2 de novembro|31 de outubro|25 de dezembro
Em qual dia a Igreja reza pelos fiéis falecidos?|2 de novembro|1º de novembro|31 de outubro|8 de dezembro
Em qual data se celebra a Imaculada Conceição?|8 de dezembro|15 de agosto|25 de março|1º de janeiro
Em qual data se celebra a Assunção de Nossa Senhora?|15 de agosto|8 de dezembro|12 de outubro|1º de novembro
Qual é o padroeiro da nossa paróquia, no Limão?|Santo Antônio|São Francisco|São José|São Pedro
Em qual rio Jesus foi batizado?|Jordão|Nilo|Tigre|Eufrates
Em qual lugar Jesus fez a Última Ceia com os apóstolos, segundo a tradição?|Cenáculo|Templo de Jerusalém|Monte das Oliveiras|Casa de Pedro
'''

MEDIO = r'''
Qual é o nome do pano retangular sobre o qual são colocados o cálice e a patena no altar?|Corporal|Pala|Purificatório|Manustérgio
Qual pano é usado para limpar o cálice depois da comunhão?|Purificatório|Corporal|Toalha do lavabo|Pala
Como se chama a peça quadrada e rígida que cobre a boca do cálice?|Pala|Corporal|Véu de ombros|Estola
Qual veste litúrgica o diácono usa sobre a alva?|Dalmática|Casula|Pluvial|Pálio
Como se chama a veste em forma de capa, usada em bênçãos solenes e procissões?|Pluvial|Casula|Alva|Dalmática
Como se chama o véu que o padre usa nos ombros para segurar a custódia na bênção do Santíssimo?|Véu de ombros (umeral)|Pala|Corporal|Pálio
Como se chama o objeto em que a hóstia é exposta para a adoração?|Custódia (ostensório)|Cibório|Patena|Naveta
Qual vaso sagrado tem tampa e guarda as hóstias que serão distribuídas na comunhão?|Cibório (âmbula)|Patena|Galheta|Aspersório
O que significa a sigla INRI colocada na cruz?|Jesus Nazareno, Rei dos Judeus|Jesus Nosso Rei Imortal|Jesus no Reino Interior|Jerusalém, Nazaré, Reino e Igreja
Qual rito costuma ser feito na Missa da Ceia do Senhor, lembrando o gesto de Jesus?|Lava-pés|Bênção das palmas|Adoração da Cruz|Bênção do fogo novo
Qual rito é feito na celebração da Sexta-feira Santa?|Adoração da Cruz|Lava-pés|Bênção das palmas|Procissão de Corpus Christi
Em qual celebração o padre abençoa o fogo novo e acende o Círio Pascal?|Vigília Pascal|Missa do Crisma|Domingo de Ramos|Quarta-feira de Cinzas
Quais óleos são abençoados na Missa do Crisma?|Crisma, dos catecúmenos e dos enfermos|Apenas azeite comum|Água benta e sal|Incenso e mirra
Quem preside a Missa do Crisma?|O bispo diocesano|O diácono|O sacristão|O coroinha
O que simboliza o incenso na liturgia?|A oração que sobe a Deus|Apenas perfume para a igreja|Um aviso de silêncio|A proteção contra insetos
Qual canto precede imediatamente a proclamação do Evangelho?|Aclamação ao Evangelho (Aleluia)|Glória|Santo|Cordeiro de Deus
Qual canto não se diz na Quaresma?|Aleluia|Santo|Cordeiro de Deus|Pai-Nosso
O Glória é omitido em quais tempos litúrgicos?|Advento e Quaresma|Natal e Páscoa|Tempo Comum e Natal|Somente na Sexta-feira Santa
O que é o prefácio?|A parte inicial da Oração Eucarística, que termina com o Santo|A oração do Pai-Nosso|A leitura do Evangelho|A bênção final
Qual destas frases faz parte da consagração do pão?|"Tomai, todos, e comei: isto é o meu Corpo"|"Eu te batizo"|"Ide em paz"|"O Senhor esteja convosco"
Como se chama a parte da Oração Eucarística em que se invoca o Espírito Santo sobre as oferendas?|Epiclese|Anamnese|Doxologia|Prefácio
Como se chama a parte em que a Igreja faz memória da morte e ressurreição do Senhor?|Anamnese|Epiclese|Doxologia|Intercessões
Como se chama a conclusão solene da Oração Eucarística ("Por Cristo, com Cristo e em Cristo")?|Doxologia|Epiclese|Prefácio|Coleta
Como se chama a oração do padre que conclui os ritos iniciais ("oração do dia")?|Coleta|Prefácio|Secreta|Poscomunhão
Como se chama a parte da missa em que se apresentam o pão e o vinho?|Preparação das oferendas|Ato penitencial|Rito da paz|Homilia
De qual expressão em latim costuma-se derivar a palavra "missa"?|Ite, missa est|Pax vobiscum|Dominus vobiscum|Kyrie eleison
Qual idioma foi usado oficialmente na liturgia romana por séculos?|Latim|Grego|Hebraico|Aramaico
Qual língua Jesus provavelmente falava no dia a dia?|Aramaico|Latim|Egípcio|Persa
Em qual língua foi escrito originalmente o Novo Testamento?|Grego|Latim|Hebraico|Árabe
Em qual língua foi escrita a maior parte do Antigo Testamento?|Hebraico|Grego|Latim|Árabe
Quem traduziu a Bíblia para o latim, na versão chamada Vulgata?|São Jerônimo|Santo Agostinho|São Bento|São Gregório Magno
Qual é o primeiro domingo do Ano Litúrgico?|Primeiro domingo do Advento|Domingo de Páscoa|Domingo de Ramos|1º de janeiro
Como se chama o período de três dias que começa na Quinta-feira Santa e vai até a Vigília Pascal?|Tríduo Pascal|Oitava de Natal|Quaresma|Tempo Comum
Qual solenidade encerra o Ano Litúrgico, no último domingo do Tempo Comum?|Cristo Rei do Universo|Corpus Christi|Pentecostes|Santíssima Trindade
Qual solenidade é celebrada no domingo depois de Pentecostes?|Santíssima Trindade|Corpus Christi|Cristo Rei|Epifania
Quantos dias dura o Tempo Pascal, da Páscoa até Pentecostes?|50 dias|40 dias|30 dias|7 dias
Em qual ano do ciclo dominical (A, B, C) se lê principalmente o Evangelho de Mateus?|Ano A|Ano B|Ano C|Ano D
Qual evangelho é lido principalmente no Ano C?|Lucas|Mateus|Marcos|João
Quais são os sacramentos da iniciação cristã?|Batismo, Crisma e Eucaristia|Penitência, Unção e Matrimônio|Ordem, Matrimônio e Unção|Batismo, Matrimônio e Ordem
Quais são os sacramentos a serviço da comunhão?|Ordem e Matrimônio|Batismo e Crisma|Penitência e Unção dos Enfermos|Eucaristia e Penitência
Quais são os sacramentos de cura?|Penitência e Unção dos Enfermos|Batismo e Eucaristia|Ordem e Matrimônio|Crisma e Eucaristia
Quais sacramentos imprimem caráter e por isso não são repetidos?|Batismo, Crisma e Ordem|Eucaristia e Penitência|Matrimônio e Unção|Penitência e Eucaristia
Quem é o ministro ordinário do sacramento da Confirmação?|O bispo|O diácono|O catequista|O leitor
Quais são os três graus do sacramento da Ordem?|Diaconato, presbiterado e episcopado|Acólito, leitor e padre|Padre, cardeal e papa|Diácono, cardeal e bispo
Quem são os ministros do sacramento do Matrimônio na Igreja latina?|Os próprios noivos|O padre|O bispo|As testemunhas
Qual é a matéria da Eucaristia?|Pão de trigo e vinho de uva|Qualquer pão e suco de fruta|Água e sal|Pão e água
Quais palavras formam o sacramento do Batismo?|"Eu te batizo em nome do Pai e do Filho e do Espírito Santo"|"Eu te abençoo"|"Recebe o Espírito"|"Vai em paz"
Quais são os três atos do penitente no sacramento da Penitência?|Contrição, confissão e satisfação|Fé, esperança e caridade|Jejum, esmola e oração|Absolvição, comunhão e crisma
Segundo os mandamentos da Igreja, com que frequência mínima se deve confessar quem tem pecado grave?|Ao menos uma vez ao ano|Todo mês|Toda semana|Uma vez na vida
Quantos são os mandamentos da Igreja?|Cinco|Dez|Sete|Três
Qual é o tempo mínimo de jejum antes de comungar?|Uma hora|Doze horas|Vinte e quatro horas|Não há jejum
Quais são as virtudes teologais?|Fé, esperança e caridade|Prudência, justiça e fortaleza|Humildade, paciência e castidade|Sabedoria, ciência e piedade
Quais são as virtudes cardeais?|Prudência, justiça, fortaleza e temperança|Fé, esperança e caridade|Paz, alegria e bondade|Humildade, obediência e pobreza
Quantos são os dons do Espírito Santo?|Sete|Nove|Doze|Três
Quantos são os pecados capitais?|Sete|Dez|Cinco|Doze
Qual destes é um dos pecados capitais?|Gula|Mentira|Roubo|Blasfêmia
Em qual discurso Jesus proclama as Bem-aventuranças?|Sermão da Montanha|Discurso da Última Ceia|Sermão no Templo|Parábola do semeador
Quantas são as obras de misericórdia corporais?|Sete|Dez|Doze|Quatro
Qual era o nome do papa Francisco antes de ser eleito?|Jorge Mario Bergoglio|Karol Wojtyła|Joseph Ratzinger|Angelo Roncalli
Qual papa polonês governou a Igreja de 1978 a 2005?|João Paulo II|Bento XVI|Paulo VI|João Paulo I
Quem foi o papa alemão que renunciou em 2013?|Bento XVI|João Paulo II|Francisco|Pio XII
Quem foi eleito papa em maio de 2025?|Leão XIV|Francisco|Bento XVI|João Paulo II
Quem convocou o Concílio Vaticano II?|São João XXIII|Pio XII|Paulo VI|João Paulo II
Qual dogma afirma que Maria foi preservada do pecado original desde a concepção?|Imaculada Conceição|Assunção|Maternidade divina|Virgindade perpétua
Qual dogma afirma que Maria foi elevada em corpo e alma à glória do céu?|Assunção|Imaculada Conceição|Anunciação|Visitação
Qual oração, rezada de manhã, ao meio-dia e à noite, lembra a Anunciação do anjo a Maria?|Ângelus|Magnificat|Salve-Rainha|Glória
Como se chama o cântico de Maria quando visita sua prima Isabel?|Magnificat|Benedictus|Nunc dimittis|Te Deum
Quem é a mãe de Maria, segundo a tradição?|Santa Ana|Santa Isabel|Santa Mônica|Santa Rita
Em qual cidade Nossa Senhora apareceu a Bernadette?|Lourdes|Fátima|Guadalupe|Aparecida
Em qual país Nossa Senhora apareceu a três pastorinhos em 1917?|Portugal|Espanha|França|México
Em qual rio pescadores encontraram a imagem de Nossa Senhora Aparecida?|Rio Paraíba do Sul|Rio Tietê|Rio São Francisco|Rio Amazonas
Em qual ano a imagem de Nossa Senhora Aparecida foi encontrada?|1717|1822|1500|1917
Qual santa é conhecida como a "Pequena Flor"?|Santa Teresinha do Menino Jesus|Santa Clara|Santa Rita|Santa Mônica
Quem foi a mãe de Santo Agostinho?|Santa Mônica|Santa Ana|Santa Clara|Santa Helena
Qual santo escreveu a Suma Teológica?|São Tomás de Aquino|Santo Agostinho|São Boaventura|Santo Anselmo
Qual santo fundou a Companhia de Jesus, os jesuítas?|Santo Inácio de Loyola|São Francisco de Assis|São Domingos|São Bento
Qual santo é considerado o pai do monaquismo no Ocidente?|São Bento|Santo Antão|São Francisco|São Bernardo
Quem fundou a Ordem dos Pregadores, os dominicanos?|São Domingos de Gusmão|São Francisco|Santo Inácio|São João Bosco
Qual foi o primeiro santo nascido no Brasil, canonizado em 2007?|Frei Galvão|José de Anchieta|Padre Cícero|Dom Bosco
Qual jesuíta ajudou a fundar a cidade de São Paulo, em 1554?|José de Anchieta|Frei Galvão|Padre Vieira|Dom Bosco
Qual foi a primeira mulher nascida no Brasil a ser canonizada, em 2019?|Santa Dulce dos Pobres|Madre Paulina|Santa Rita|Santa Bárbara
Quem foi chamado por Deus a deixar sua terra e é conhecido como pai na fé?|Abraão|Moisés|Noé|Davi
Qual patriarca recebeu o nome de Israel?|Jacó|Isaac|José|Abraão
Quantas pragas Deus enviou ao Egito, segundo o livro do Êxodo?|Dez|Sete|Doze|Quarenta
Qual ave Noé soltou e voltou com um ramo de oliveira?|Pomba|Corvo|Águia|Pardal
Qual rei construiu o primeiro Templo de Jerusalém?|Salomão|Davi|Ezequias|Herodes
Qual profeta foi levado ao céu num carro de fogo?|Elias|Eliseu|Isaías|Jeremias
Qual livro da Bíblia reúne 150 orações e cânticos?|Salmos|Provérbios|Cântico dos Cânticos|Eclesiastes
Quem foi vendido pelos irmãos e se tornou governador do Egito?|José|Benjamim|Rúben|Judá
Como se chamam os cinco primeiros livros da Bíblia?|Pentateuco|Evangelhos|Profetas|Sapienciais
Quem escreveu a maior parte das cartas do Novo Testamento?|São Paulo|São Pedro|São João|São Tiago
Qual apóstolo, segundo a tradição, foi crucificado de cabeça para baixo?|São Pedro|São André|São Filipe|São Tomé
Qual discípulo é conhecido como "o discípulo amado"?|São João|São Tiago|Judas Tadeu|Matias
Quem foi escolhido para ocupar o lugar de Judas entre os Doze?|Matias|Barnabé|Silas|Estêvão
Quem foi o primeiro mártir cristão?|Santo Estêvão|São Pedro|São Paulo|São Tiago
Em qual caminho Saulo teve a visão que o converteu?|Caminho de Damasco|Caminho de Jericó|Caminho de Emaús|Caminho de Belém
Em qual povoado Jesus ressuscitado partiu o pão com dois discípulos?|Emaús|Betânia|Caná|Magdala
Quem foi a primeira pessoa a ver Jesus ressuscitado, segundo o Evangelho de João?|Maria Madalena|Marta|Maria de Betânia|Isabel
Quem lavou os pés dos discípulos na Última Ceia?|Jesus|Pedro|João|Maria
Qual imperador concedeu liberdade aos cristãos pelo Edito de Milão, em 313?|Constantino|Nero|Diocleciano|Teodósio
Qual imperador romano é lembrado por perseguir os cristãos depois do incêndio de Roma, em 64?|Nero|Constantino|Augusto|Trajano
Como se chamam as galerias subterrâneas em que os primeiros cristãos enterravam seus mortos?|Catacumbas|Basílicas|Claustros|Capelas
Qual cidade foi a capital do Império Romano do Oriente?|Constantinopla|Alexandria|Antioquia|Atenas
Quem iniciou a Reforma Protestante, em 1517?|Martinho Lutero|João Calvino|Henrique VIII|Erasmo de Roterdã
Qual concílio respondeu à Reforma Protestante?|Concílio de Trento|Concílio de Niceia|Concílio Vaticano I|Concílio de Calcedônia
O que significa a palavra "católica"?|Universal|Antiga|Romana|Cristã
O que significa a palavra grega "ekklesía", origem de "Igreja"?|Assembleia convocada|Casa de oração|Templo sagrado|Rebanho
Como se chama o livro que reúne a doutrina católica, publicado em 1992?|Catecismo da Igreja Católica|Código de Direito Canônico|Suma Teológica|Missal Romano
Quem promulgou o Catecismo da Igreja Católica, em 1992?|João Paulo II|Paulo VI|Bento XVI|João Paulo I
Em qual cidade está o túmulo de Santo Antônio, na Basílica do Santo?|Pádua|Lisboa|Assis|Florença
Em qual cidade nasceu São Francisco?|Assis|Pádua|Roma|Florença
Em qual cidade nasceu Santo Antônio, também chamado de Santo Antônio de Lisboa?|Lisboa|Pádua|Roma|Assis
Qual é o nome do servidor que leva a naveta ao lado do turiferário?|Naveteiro|Cruciferário|Ceroferário|Mitrífero
Como se chama o rito em que o padre lava as mãos antes da Oração Eucarística?|Lavabo|Epiclese|Aspersão|Anamnese
Como se chama o rito em que o padre parte a hóstia durante o canto do Cordeiro de Deus?|Fração do pão|Ofertório|Consagração|Epiclese
Quantas estações tem a Via-Sacra tradicional?|Quatorze|Sete|Doze|Quinze
Quantos mistérios tem o Rosário completo, com os luminosos?|Vinte|Quinze|Dez|Vinte e cinco
Quais mistérios se meditam às quintas-feiras, no costume atual?|Luminosos|Gozosos|Dolorosos|Gloriosos
Em quais dias se costuma meditar os mistérios gloriosos?|Quartas-feiras e domingos|Terças e sextas|Segundas e sábados|Quintas-feiras
Qual é o primeiro mistério glorioso?|A Ressurreição de Jesus|A Ascensão de Jesus|A Assunção de Maria|A vinda do Espírito Santo
Qual é o primeiro mistério gozoso?|A Anunciação do anjo a Maria|O Nascimento de Jesus|A Visitação|A Apresentação no Templo
Qual é o quinto mistério doloroso?|A crucificação e morte de Jesus|A coroação de espinhos|Jesus carrega a cruz|A flagelação
Qual destes não é um mistério gozoso?|A Transfiguração|A Visitação|A Anunciação|O Nascimento de Jesus
Qual destes é um mistério luminoso?|As bodas de Caná|A Anunciação|A flagelação|A Assunção de Maria
Qual cor se usa na solenidade de Cristo Rei?|Branco|Vermelho|Verde|Roxo
Qual costume é comum a partir do 5º domingo da Quaresma, em muitas igrejas?|Cobrir cruzes e imagens com panos roxos|Acender todas as luzes do altar|Cantar o Aleluia|Usar vestes douradas
O que a Igreja celebra em 25 de dezembro?|O Natal do Senhor|A Epifania|A Anunciação|A Ascensão
Qual dia da semana é o dia do Senhor para os cristãos?|Domingo|Sábado|Segunda-feira|Sexta-feira
O que é a Quarta-feira de Cinzas?|O início da Quaresma, com jejum e imposição das cinzas|O fim do Natal|A festa de Pentecostes|A Vigília Pascal
O que o padre diz ao impor as cinzas, em uma das fórmulas possíveis?|"Convertei-vos e crede no Evangelho"|"Ide em paz"|"O Senhor esteja convosco"|"Eu te batizo"
Quem é o padroeiro dos sacerdotes e párocos, o Cura d'Ars?|São João Maria Vianney|São Pedro|São Tiago|São Judas Tadeu
Quem fundou a Congregação Salesiana, dedicada aos jovens?|São João Bosco|São Francisco de Sales|Santo Inácio|São Domingos Sávio
'''

DIFICIL = r'''
Qual foi o primeiro concílio ecumênico, realizado em 325?|Niceia I|Constantinopla I|Éfeso|Calcedônia
Qual concílio condenou o arianismo e definiu que o Filho é consubstancial ao Pai?|Concílio de Niceia (325)|Concílio de Éfeso (431)|Concílio de Trento|Concílio de Latrão IV
Qual concílio definiu a divindade do Espírito Santo e completou o Credo Niceno-Constantinopolitano?|Constantinopla I (381)|Niceia I (325)|Éfeso (431)|Calcedônia (451)
Qual concílio proclamou Maria "Theotokos" (Mãe de Deus), contra Nestório?|Éfeso (431)|Niceia (325)|Calcedônia (451)|Trento (1545)
Qual concílio definiu que Cristo tem duas naturezas, divina e humana, em uma só pessoa?|Calcedônia (451)|Niceia I|Éfeso|Constantinopla II
Qual concílio autorizou a veneração das imagens (ícones), contra a iconoclastia?|Niceia II (787)|Calcedônia|Constantinopla I|Trento
Qual concílio condenou o monotelismo, afirmando duas vontades em Cristo?|Constantinopla III (680–681)|Niceia I|Éfeso|Latrão IV
Qual concílio medieval usou oficialmente o termo "transubstanciação" e exigiu confissão anual?|Latrão IV (1215)|Trento|Vaticano I|Lyon II
Qual concílio definiu os sete sacramentos e reafirmou o cânon bíblico em resposta à Reforma?|Trento (1545–1563)|Latrão IV|Vaticano I|Constantinopla IV
Qual concílio definiu a infalibilidade papal e o primado de jurisdição?|Vaticano I (1869–1870)|Vaticano II|Trento|Calcedônia
Qual concílio produziu as constituições Lumen Gentium, Dei Verbum, Sacrosanctum Concilium e Gaudium et Spes?|Vaticano II|Vaticano I|Trento|Latrão IV
Qual constituição do Vaticano II trata da sagrada liturgia?|Sacrosanctum Concilium|Lumen Gentium|Dei Verbum|Gaudium et Spes
Qual constituição do Vaticano II trata da Igreja (a "Luz dos povos")?|Lumen Gentium|Dei Verbum|Sacrosanctum Concilium|Gaudium et Spes
Qual constituição do Vaticano II trata da Revelação divina?|Dei Verbum|Lumen Gentium|Gaudium et Spes|Sacrosanctum Concilium
Qual constituição do Vaticano II trata da Igreja no mundo atual?|Gaudium et Spes|Dei Verbum|Lumen Gentium|Sacrosanctum Concilium
Qual papa encerrou o Concílio Vaticano II, em 1965?|Paulo VI|João XXIII|João Paulo I|Pio XII
Qual papa convocou o Concílio de Trento?|Paulo III|Pio IV|Leão X|Júlio II
Qual papa convocou o Concílio Vaticano I?|Pio IX|Leão XIII|Pio X|Gregório XVI
Quantos concílios ecumênicos a Igreja Católica reconhece?|21|7|12|25
Qual concílio, narrado em Atos 15, discutiu se os gentios precisavam ser circuncidados?|Concílio de Jerusalém|Concílio de Niceia|Concílio de Antioquia|Concílio de Éfeso
O Credo Niceno-Constantinopolitano resultou de quais concílios?|Niceia I e Constantinopla I|Éfeso e Calcedônia|Trento e Vaticano I|Latrão e Lyon
Como se chama a separação entre as Igrejas do Ocidente e do Oriente, em 1054?|Cisma do Oriente|Cisma do Ocidente|Reforma Anglicana|Cisma de Avinhão
Qual concílio pôs fim ao Grande Cisma do Ocidente?|Concílio de Constança|Concílio de Trento|Concílio de Niceia|Concílio de Lyon
Em que ano foi proclamado o dogma da Imaculada Conceição?|1854|1950|1870|1517
Qual papa proclamou o dogma da Imaculada Conceição?|Pio IX|Pio XII|Leão XIII|João XXIII
Qual documento proclamou o dogma da Imaculada Conceição?|Ineffabilis Deus|Munificentissimus Deus|Humani Generis|Pastor Aeternus
Qual papa proclamou o dogma da Assunção de Maria, em 1950?|Pio XII|Pio IX|Paulo VI|Pio X
Qual documento proclamou o dogma da Assunção?|Munificentissimus Deus|Ineffabilis Deus|Pastor Aeternus|Lumen Gentium
Qual documento do Vaticano I definiu a infalibilidade papal?|Pastor Aeternus|Dei Filius|Rerum Novarum|Mystici Corporis
Qual dogma afirma que Maria permaneceu virgem antes, durante e depois do parto?|Virgindade perpétua|Imaculada Conceição|Assunção|Anunciação
Como se chama a doutrina de que o pão e o vinho mudam de substância, mantendo as aparências?|Transubstanciação|Transfiguração|Encarnação|Predestinação
Como se chama a heresia que negava a divindade plena de Cristo, condenada em Niceia?|Arianismo|Nestorianismo|Pelagianismo|Docetismo
Qual heresia afirmava que o ser humano pode se salvar sem a graça de Deus?|Pelagianismo|Arianismo|Nestorianismo|Monofisismo
Qual heresia dividia Cristo em duas pessoas e foi condenada em Éfeso?|Nestorianismo|Arianismo|Docetismo|Gnosticismo
Qual heresia afirmava que Cristo só parecia ter um corpo humano?|Docetismo|Arianismo|Pelagianismo|Donatismo
Como se chama a expressão "e do Filho", acrescentada ao Credo no Ocidente?|Filioque|Homoousios|Theotokos|Ex cathedra
Qual termo grego do Concílio de Niceia significa "da mesma substância"?|Homoousios|Theotokos|Logos|Kenosis
O que significa a expressão "ex cathedra"?|Do alto da cátedra (ensinamento solene do papa)|Da sacristia|Do altar|Do púlpito
O que é uma encíclica?|Carta circular do papa a toda a Igreja|Decreto de um concílio|Oração oficial da missa|Livro de ritos
Qual encíclica de Leão XIII, de 1891, inaugurou a Doutrina Social da Igreja moderna?|Rerum Novarum|Laudato Si'|Humanae Vitae|Populorum Progressio
Qual encíclica do papa Francisco, de 2015, trata do cuidado da casa comum?|Laudato Si'|Fratelli Tutti|Lumen Fidei|Deus Caritas Est
Qual encíclica de Paulo VI, de 1968, trata da regulação da natalidade?|Humanae Vitae|Populorum Progressio|Ecclesiam Suam|Mater et Magistra
Qual foi a primeira encíclica de Bento XVI, sobre o amor?|Deus Caritas Est|Spe Salvi|Caritas in Veritate|Lumen Fidei
Qual encíclica de João Paulo II, de 1995, trata do valor da vida humana?|Evangelium Vitae|Redemptor Hominis|Fides et Ratio|Veritatis Splendor
Quais são as quatro partes do Catecismo da Igreja Católica?|Profissão da fé, celebração do mistério cristão, vida em Cristo e oração cristã|Gênesis, Êxodo, Levítico e Números|Fé, esperança, caridade e justiça|Batismo, Crisma, Eucaristia e Ordem
Como se chama o código de leis da Igreja latina, promulgado em 1983?|Código de Direito Canônico|Catecismo|Ordenação Geral|Compêndio Social
Qual papa reformou o calendário em 1582, criando o calendário gregoriano?|Gregório XIII|Gregório Magno|Pio V|Urbano VIII
Qual papa promulgou o Missal Romano após o Concílio de Trento, em 1570?|São Pio V|São Pio X|Pio XII|Paulo VI
Qual papa promulgou o Missal Romano da reforma litúrgica do Vaticano II?|Paulo VI|João XXIII|Pio XII|João Paulo II
Qual documento reúne as normas gerais para celebrar a missa?|Instrução Geral do Missal Romano|Código de Direito Canônico|Catecismo|Compêndio da Doutrina Social
Como se chama o livro litúrgico com os ritos dos sacramentos e bênçãos administrados pelo padre?|Ritual Romano|Pontifical Romano|Martirológio|Gradual
Como se chama o livro litúrgico que lista as comemorações dos santos de cada dia?|Martirológio Romano|Lecionário|Gradual|Ritual
Qual livro litúrgico contém a oração oficial da Igreja ao longo do dia?|Liturgia das Horas|Missal|Lecionário|Evangeliário
Quais são as duas horas principais da Liturgia das Horas?|Laudes e Vésperas|Terça e Noa|Completas e Ofício das Leituras|Matinas e Sexta
Qual hora da Liturgia das Horas é rezada antes de dormir?|Completas|Laudes|Vésperas|Terça
Qual cântico de Zacarias é rezado nas Laudes?|Benedictus|Magnificat|Nunc dimittis|Te Deum
Qual cântico de Maria é rezado nas Vésperas?|Magnificat|Benedictus|Nunc dimittis|Gloria in excelsis
Qual cântico de Simeão é rezado nas Completas?|Nunc dimittis|Magnificat|Benedictus|Te Deum
O que é o Te Deum?|Um hino de ação de graças|Um salmo de penitência|Uma oração de ordenação|Uma antífona de Natal
Qual ministério instituído é conferido para servir ao altar?|Acolitado|Subdiaconato|Ostiário|Exorcistado
Como se chama o ministério instituído para a proclamação da Palavra de Deus?|Leitorado|Acolitado|Diaconato|Sacristão
Qual papa instituiu, em 2021, o ministério de Catequista (Antiquum Ministerium)?|Francisco|Bento XVI|João Paulo II|Paulo VI
Como se chama a faixa de lã branca usada pelo papa e pelos arcebispos metropolitanos?|Pálio|Mitra|Dalmática|Pluvial
Como se chama o período entre a morte (ou renúncia) de um papa e a eleição do próximo?|Sede vacante|Consistório|Conclave|Sínodo
Qual é o número máximo de cardeais eleitores, com menos de 80 anos, previsto para o conclave?|120|72|200|60
Qual santo é chamado de "Doutor Angélico"?|São Tomás de Aquino|Santo Agostinho|São Boaventura|Santo Anselmo
Qual título de Doutor da Igreja foi dado a Santo Antônio de Pádua?|Doutor Evangélico|Doutor Angélico|Doutor Seráfico|Doutor da Graça
Qual papa declarou Santo Antônio Doutor da Igreja, em 1946?|Pio XII|Pio X|Leão XIII|João XXIII
Em qual ano morreu Santo Antônio de Pádua?|1231|1181|1300|1095
Quem foi a primeira mulher declarada Doutora da Igreja, em 1970?|Santa Teresa de Ávila|Santa Catarina de Sena|Santa Teresinha|Santa Hildegarda
Quais são os quatro grandes doutores da Igreja do Ocidente na Antiguidade?|Ambrósio, Agostinho, Jerônimo e Gregório Magno|Tomás, Boaventura, Anselmo e Bernardo|Francisco, Domingos, Bento e Inácio|Pedro, Paulo, Tiago e João
Qual santo escreveu "Confissões"?|Santo Agostinho|São Jerônimo|São Tomás de Aquino|São Bento
Qual santo escreveu uma famosa Regra monástica no século VI?|São Bento|São Francisco|Santo Inácio|São Bruno
Quem foi bispo de Hipona?|Santo Agostinho|Santo Ambrósio|São Jerônimo|São Gregório Magno
Quem batizou Santo Agostinho?|Santo Ambrósio|São Jerônimo|São Gregório Magno|Santa Mônica
Qual santo traduziu a Bíblia para o latim vivendo em Belém?|São Jerônimo|Santo Agostinho|Santo Ambrósio|São Basílio
Qual destes livros é deuterocanônico (está na Bíblia católica, mas não na protestante)?|Tobias|Rute|Jó|Josué
Quais evangelhos são chamados de sinóticos?|Mateus, Marcos e Lucas|Mateus, Marcos e João|Lucas, João e Atos|Marcos, Lucas e João
Qual profeta anunciou "eis que a virgem conceberá"?|Isaías|Jeremias|Ezequiel|Daniel
Qual livro profético contém a visão dos ossos secos?|Ezequiel|Isaías|Daniel|Oseias
Qual foi o último juiz de Israel, que ungiu Saul e Davi?|Samuel|Elias|Natã|Gedeão
Qual imperador ordenou o recenseamento no tempo do nascimento de Jesus, segundo Lucas?|César Augusto|Tibério|Nero|Constantino
Quem era o governador romano da Judeia que condenou Jesus?|Pôncio Pilatos|Herodes Antipas|Caifás|César Augusto
Quem era o sumo sacerdote no julgamento de Jesus diante do Sinédrio?|Caifás|Nicodemos|José de Arimateia|Gamaliel
Em qual monte, segundo a tradição, Jesus se transfigurou?|Tabor|Sinai|Carmelo|Nebo
Em qual monte Jesus foi crucificado?|Gólgota (Calvário)|Sião|Moriá|Nebo
Em qual momento da missa o Evangeliário ou o livro do Evangelho é incensado?|Antes da proclamação do Evangelho|Depois da bênção final|Durante o Credo|Durante a homilia
Qual cor litúrgica se usa na Sexta-feira Santa?|Vermelho|Preto|Roxo|Branco
Qual cor litúrgica se usa no Domingo de Ramos?|Vermelho|Roxo|Verde|Branco
Além do roxo e do branco, qual cor pode ser usada nas missas de defuntos?|Preto|Verde|Rosa|Vermelho
Como se chama o 4º domingo da Quaresma, em que se pode usar a cor rosa?|Laetare|Gaudete|Quasimodo|Septuagésima
Como se chama o 3º domingo do Advento?|Gaudete|Laetare|Quasimodo|Septuagésima
Como se chama o 2º domingo da Páscoa, instituído por João Paulo II no ano 2000?|Domingo da Divina Misericórdia|Domingo da Boa Nova|Domingo da Santíssima Trindade|Domingo da Ascensão
Em qual celebração os sinos tocam durante o Glória e depois ficam em silêncio até a Vigília Pascal?|Missa da Ceia do Senhor (Quinta-feira Santa)|Domingo de Ramos|Sexta-feira Santa|Missa do Galo
Em qual data se celebra a solenidade de São Pedro e São Paulo?|29 de junho|24 de junho|13 de junho|2 de julho
Em qual data se celebra o nascimento de São João Batista?|24 de junho|29 de junho|13 de junho|1º de julho
Em qual data se celebra a Anunciação do Senhor?|25 de março|8 de dezembro|2 de fevereiro|15 de agosto
Em qual data se celebra a Apresentação do Senhor?|2 de fevereiro|25 de março|6 de janeiro|8 de setembro
Em qual data se celebra a Natividade de Nossa Senhora?|8 de setembro|8 de dezembro|15 de agosto|12 de outubro
Em qual data se celebra a Exaltação da Santa Cruz?|14 de setembro|3 de maio|1º de novembro|8 de dezembro
Em qual data se celebra a Transfiguração do Senhor?|6 de agosto|15 de agosto|29 de junho|1º de novembro
Em qual data se celebra a solenidade de São José, esposo de Maria?|19 de março|1º de maio|25 de março|8 de dezembro
Em qual data se celebra São José Operário?|1º de maio|19 de março|13 de junho|2 de novembro
Em qual data se celebra São Francisco de Assis?|4 de outubro|13 de junho|29 de setembro|1º de novembro
Em qual data se celebram os santos arcanjos Miguel, Gabriel e Rafael?|29 de setembro|2 de outubro|4 de outubro|8 de novembro
Em qual data se celebram os santos Anjos da Guarda?|2 de outubro|29 de setembro|4 de outubro|1º de novembro
Quem é o padroeiro universal da Igreja?|São José|São Pedro|São Paulo|Santo Antônio
Qual papa instituiu a festa de Corpus Christi para toda a Igreja, em 1264?|Urbano IV|Gregório IX|Inocêncio III|Pio V
Quem inspirou a festa de Corpus Christi, a partir de visões, em Liège?|Santa Juliana de Mont Cornillon|Santa Clara|Santa Catarina de Sena|Santa Brígida
Qual santo é o autor do hino eucarístico Tantum Ergo?|São Tomás de Aquino|Santo Ambrósio|São Francisco|São Bernardo
Qual papa é tradicionalmente ligado ao canto gregoriano?|São Gregório Magno|São Pio X|Santo Ambrósio|São Leão Magno
Qual imperador convocou o Concílio de Niceia, em 325?|Constantino|Teodósio|Justiniano|Carlos Magno
Quem foi coroado imperador pelo papa Leão III no ano 800?|Carlos Magno|Constantino|Otão I|Henrique IV
Qual papa enviou Santo Agostinho de Cantuária para evangelizar a Inglaterra?|Gregório Magno|Leão Magno|Urbano II|Inocêncio III
Qual papa pregou a Primeira Cruzada, no Concílio de Clermont, em 1095?|Urbano II|Inocêncio III|Bento XIV|Gregório VII
Qual papa instituiu os mistérios luminosos do Rosário, em 2002?|João Paulo II|Bento XVI|Paulo VI|Pio XII
Qual papa convocou o Ano Santo Extraordinário da Misericórdia, em 2015?|Francisco|Bento XVI|João Paulo II|Paulo VI
Qual é o último mistério luminoso?|A instituição da Eucaristia|O Batismo de Jesus|As bodas de Caná|A Transfiguração
'''


def _ler(bloco, nivel):
    perguntas = []
    for linha in bloco.strip().splitlines():
        linha = linha.strip()
        if not linha:
            continue
        partes = [p.strip() for p in linha.split("|") if p.strip()]
        # linhas malformadas (menos de 4 alternativas) são ignoradas
        if len(partes) < 3:
            continue
        pergunta, certa, *erradas = partes
        perguntas.append({"p": pergunta, "c": certa, "e": erradas, "n": nivel})
    return perguntas


def carregar():
    """Todas as perguntas, como lista de dicts: p (pergunta), c (certa), e (erradas), n (nível 1–3)."""
    return _ler(FACIL, 1) + _ler(MEDIO, 2) + _ler(DIFICIL, 3)
