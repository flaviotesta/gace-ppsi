#!/usr/bin/env node
/* Teste de fumaça do GACE-PPSI, executado pela Action .github/workflows/testes.yml
   a cada alteração no aplicativo ou no manifesto de versão.

   Verifica invariantes que protegem as promessas do produto:
   1. versao.json é um JSON válido e sua versão bate com a constante VERSAO_APP do HTML;
   2. o arquivo é autocontido: nenhum script, folha de estilo ou imagem é carregado de fora;
   3. o aplicativo monta sem erro no jsdom e o instrumento está íntegro
      (18 itens, cada um com escala de 7 pontos = 126 botões de resposta);
   4. as funções essenciais existem (escape, exportação, importação, relatório).

   Uso local (opcional): npm install jsdom && node .github/scripts/teste_ci.js
*/
const fs = require("fs");
const path = require("path");
const { JSDOM, VirtualConsole } = require("jsdom");

const RAIZ = process.cwd();
const ARQ_APP = path.join(RAIZ, "GACE-PPSI.html");
const ARQ_VERSAO = path.join(RAIZ, "versao.json");

let falhas = 0;
function checar(condicao, mensagem) {
  if (condicao) {
    console.log("  ok  -", mensagem);
  } else {
    falhas += 1;
    console.error("  FALHA -", mensagem);
  }
}

console.log("1) Manifesto de versão");
const html = fs.readFileSync(ARQ_APP, "utf-8");
const manifesto = JSON.parse(fs.readFileSync(ARQ_VERSAO, "utf-8"));
const constante = (html.match(/VERSAO_APP\s*=\s*"([^"]+)"/) || [])[1];
checar(typeof manifesto.versao === "string" && manifesto.versao.length > 0,
  `versao.json tem o campo "versao" (${manifesto.versao})`);
checar(constante === manifesto.versao,
  `VERSAO_APP do HTML (${constante}) confere com o versao.json (${manifesto.versao})`);

console.log("2) Autocontenção (nenhum recurso externo)");
const externos = [];
for (const m of html.matchAll(/<(script|link|img|iframe|source)\b[^>]*>/gi)) {
  const tag = m[0];
  const alvo = (tag.match(/\b(?:src|href)\s*=\s*"([^"]+)"/i) || [])[1] || "";
  if (/^https?:\/\//i.test(alvo)) externos.push(tag.slice(0, 90));
}
checar(externos.length === 0,
  externos.length === 0
    ? "nenhuma tag carrega script/estilo/imagem de endereço externo"
    : `encontradas ${externos.length} tags externas: ${externos.join(" | ")}`);

console.log("3) Montagem do aplicativo e integridade do instrumento");
const consoleVirtual = new VirtualConsole();
let erroPagina = null;
consoleVirtual.on("jsdomError", (e) => { erroPagina = e; });
const dom = new JSDOM(html, {
  runScripts: "dangerously",
  url: "https://gace-ppsi.teste/",
  virtualConsole: consoleVirtual,
  beforeParse(janela) {
    // o jsdom não implementa rolagem; o aplicativo a usa apenas para navegação visual
    janela.scrollTo = () => {};
    janela.HTMLElement.prototype.scrollIntoView = function () {};
  },
});
const doc = dom.window.document;
checar(erroPagina === null,
  erroPagina === null ? "inicialização sem erro de script" : `erro na inicialização: ${erroPagina}`);
const itens = doc.querySelectorAll(".item").length;
const botoesEscala = doc.querySelectorAll(".item button").length;
checar(itens === 18, `instrumento com 18 itens montados (encontrados: ${itens})`);
checar(botoesEscala === 126,
  `escala íntegra: ${botoesEscala} botões de resposta (esperado 18 × 7 = 126)`);
checar(doc.getElementById("inst") !== null, 'campo de identificação da instituição ("inst") presente');

console.log("4) Funções essenciais");
for (const fn of ["esc", "exportarJSON", "importarJSON", "gerarRelatorio", "pacote"]) {
  checar(dom.window.eval(`typeof ${fn}`) === "function", `função ${fn}() definida`);
}

if (falhas > 0) {
  console.error(`\n${falhas} verificação(ões) falharam.`);
  process.exit(1);
}
console.log("\nTodas as verificações passaram.");
