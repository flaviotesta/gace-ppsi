# Histórico de versões — GACE-PPSI

## v1.2.0 — julho de 2026

- Segurança (importação): a leitura de avaliações anteriores passa a validar o esquema do arquivo — só aceita a estrutura conhecida, converte as respostas à escala de 1 a 7 e descarta qualquer conteúdo estranho. Corrige uma exposição a conteúdo malicioso em que um arquivo .json adulterado poderia injetar código na tela de diagnóstico e no relatório. Arquivos exportados por versões anteriores continuam sendo importados normalmente.
- Segurança (defesa em profundidade): adicionada Política de Segurança de Conteúdo (CSP) que restringe o aplicativo a si mesmo — a única conexão de rede permitida é a checagem manual de versão; toda saída de texto passou a ser escapada no relatório executivo.
- Acessibilidade: o questionário passou a expor a escala como grupo de opções (radiogroup) navegável por teclado (setas, Início/Fim), com estado anunciável por leitores de tela e realce de foco visível — aderente às diretrizes de acessibilidade.
- Transparência: a folha de método explicita que respostas e identificação são gravadas apenas no navegador local, até o usuário concluir ou apagar.
- Registro de adoção: o rodapé do relatório executivo convida a instituição a registrar a adoção no repositório, compondo as evidências de impacto do produto.
- Sem alterações no instrumento, na escala, nos domínios, nos benchmarks ou nas regras de cálculo. Hash SHA-256 desta versão: 76e2fc7b6e0f257aaf6b5a75e0e911904e9cfb6c1b556639fbf3a45f0bff9c2d

## v1.1.1 — julho de 2026

- Correção: o resultado da verificação de atualizações agora rola automaticamente até a área visível (antes, o aviso aparecia no topo da página e podia passar despercebido).
- Selo DOI (Zenodo) adicionado ao README; DOI incluído na folha de método do aplicativo.
- Sem alterações no instrumento nem nos cálculos.

## v1.1 — julho de 2026

- Nova identidade visual: logomarca própria (escudo em três camadas), padrão visual institucional moderno, ilustrações vetoriais originais e navegação por etapas.
- Relatório executivo ampliado: síntese com indicadores e classificação automática do perfil do programa; radar das 8 capacidades e gráficos comparativos com o padrão nacional; narrativa automática de forças, fragilidades e leitura em camadas.
- Recomendações desdobradas: cada prioridade passa a incluir evidência, linhas de ação, indicadores de acompanhamento sugeridos, referenciais públicos de apoio e atores a envolver; plano de ação em dois horizontes (0–6 e 6–18 meses); recomendações também para as demais capacidades frágeis.
- Atualização normativa: referência à Política Nacional de Segurança da Informação atualizada para o Decreto nº 12.572/2025.
- Privacidade reforçada: removidos os campos de registro opcional de índices de maturidade do PPSI — o diagnóstico não solicita nenhum dado de conformidade da instituição, apenas a percepção do respondente.
- Licença formalizada como Creative Commons CC BY 4.0.
- Distribuição exclusivamente por download (sem versão hospedada) e verificação de atualizações manual: um botão consulta o arquivo público de versão do repositório, sem transmitir nenhum dado da avaliação; atualizar é sempre escolha do usuário.
- Sem alterações no instrumento: itens, escala, domínios, benchmarks e regras de cálculo idênticos à v1.0. Avaliações exportadas na v1.0 podem ser importadas normalmente.

## v1.0 — julho de 2026

- Versão inicial do produto técnico-tecnológico: instrumento de 18 itens (8 capacidades, 10 itens de efetividade), comparação com o padrão nacional de 58 IFES, leitura em camadas, priorização baseada em evidência, relatório executivo para impressão, rascunho local e exportação/importação em JSON.
