# Política de Segurança — GACE-PPSI

O GACE-PPSI é um aplicativo de avaliação institucional de execução **100% local**: um único arquivo HTML, sem instalação, sem servidor e **sem transmissão de dados**. A única conexão de rede prevista é a checagem **manual** de novas versões (botão "Verificar atualizações", que consulta o arquivo `versao.json` deste repositório). Qualquer outro comportamento de rede é anômalo e deve ser reportado.

## Versões com suporte

| Versão | Situação |
| ------ | -------- |
| 1.1.x  | Suportada (versão vigente) |
| 1.0.x  | Sem suporte — atualize pela página de releases |

Use sempre o arquivo publicado na [página de releases](https://github.com/flaviotesta/gace-ppsi/releases/latest) e confira o hash SHA-256 divulgado. Cópias obtidas de outras fontes não são cobertas por esta política.

## Como reportar uma vulnerabilidade

- **Não abra issue pública** para assuntos de segurança.
- Preferencialmente, use o recurso **"Report a vulnerability"** na aba *Security* deste repositório (reporte privado).
- Alternativamente, escreva para **flavio.testa@uffs.edu.br** com o assunto `[SEGURANÇA GACE-PPSI]`, descrevendo o comportamento observado, a versão do aplicativo, o navegador utilizado e, se possível, os passos para reprodução. Não inclua dados reais de avaliação institucional.

## Compromissos

- Confirmação de recebimento em até **7 dias úteis**.
- Avaliação da procedência e da severidade, com retorno sobre o encaminhamento.
- Correções publicadas como nova versão na página de releases, com registro no `CHANGELOG` e novo hash SHA-256.
- Crédito público ao pesquisador ou pesquisadora que reportar, se assim desejar.

## Superfícies de interesse

Relatos são especialmente bem-vindos sobre: a **importação de arquivos JSON** de avaliações anteriores, a **geração do relatório executivo**, a **checagem de versão** e qualquer situação em que o aplicativo tente acessar a rede fora do fluxo descrito acima.
