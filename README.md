# GamePriceWars: Comparador Automatizado de Preços ⚔️🎮

**Disciplina:** Automação e Programabilidade em Redes
**Projeto:** Comparador de Preços de Jogos Digitais (Steam vs. Epic Games)
**Tecnologia:** Python + Selenium WebDriver

---

## 🚀 Instruções de Execução

Siga os passos abaixo para executar a automação em seu ambiente local.

### 1. Pré-requisitos

- **Python 3.8+** instalado.
- **Google Chrome** instalado.

### 2. Instalação das Dependências

Abra o terminal na pasta raiz do projeto e execute:

```bash
pip install -r requirements.txt
```

_(O arquivo `requirements.txt` deve conter apenas a biblioteca `selenium`)_

### 3\. Como Rodar

Execute o script principal:

```bash
python3 main.py
```

**Fluxo de Execução:**

1.  O terminal solicitará o **nome do jogo** (ex: `Maneater`, `Cyberpunk 2077`).
2.  O navegador abrirá automaticamente (maximizado) e realizará a busca em tempo real.
3.  O comparativo de preços será exibido no console.
4.  Uma **evidência visual (screenshot)** será salva automaticamente na pasta `screenshots/`.

---

# 📄 Relatório Técnico

## 1\. Visão Geral e Motivação

O mercado de jogos digitais caracteriza-se pela alta volatilidade de preços e fragmentação entre diversas lojas. Realizar a comparação manual é uma tarefa repetitiva e ineficiente, exigindo navegação em interfaces distintas e interpretação visual de promoções.

O projeto **GamePriceWars** automatiza este fluxo, utilizando técnicas de _Web Scraping_ para extrair, normalizar e comparar dados, permitindo ao usuário identificar a melhor oferta econômica em segundos, eliminando o erro humano.

## 2\. Objetivos da Automação

O script foi desenvolvido para atender estritamente aos requisitos acadêmicos propostos na disciplina:

- **Interação Multi-site:** Navegação autônoma em dois domínios com estruturas DOM heterogêneas (Steam e Epic Games).
- **Sincronização:** Uso de esperas explícitas (`WebDriverWait`) para lidar com carregamento assíncrono (AJAX), garantindo que o script aguarde os elementos estarem prontos antes de interagir.
- **Tratamento de Erros:** Implementação de blocos `try/except` para garantir a resiliência da automação caso um jogo não seja encontrado ou o layout mude.
- **Evidência:** Geração automática de logs visuais (screenshots) organizados em diretório específico.

## 3\. Abordagem Técnica

### 3.1 Arquitetura Modular

O código segue o padrão de modularização, separando a lógica de cada loja em classes especialistas (`SteamScraper` e `EpicScraper`). Isso facilita a manutenção e a escalabilidade do projeto.

### 3.2 Estratégias de Seleção (Locators)

Para garantir robustez, foram utilizadas estratégias variadas de seleção de elementos:

- **Steam:** A automação prioriza a busca direta via URL (`GET /search/?term=`) para maior estabilidade. A extração de preços utiliza o atributo oculto `data-price-final` (quando disponível), que fornece o valor numérico exato em centavos, evitando erros de _parsing_ de string.
- **Epic Games:** Devido ao uso de classes CSS dinâmicas/ofuscadas (geradas por React), a estratégia de seleção baseia-se em **XPath** contextual e busca por texto.

## 4\. Desafios Enfrentados e Soluções

### Desafio 1: Bloqueios de Segurança e SSL

- **Problema:** Em ambientes macOS e redes corporativas, falhas de certificado SSL (`NotOpenSSLWarning`) impediam o carregamento das páginas.
- **Solução:** Configuração avançada das `ChromeOptions` para ignorar erros de certificado e desabilitar flags de automação (`--disable-blink-features=AutomationControlled`), simulando um navegador de usuário real.

### Desafio 2: Elementos Dinâmicos na Epic Games

- **Problema:** A Epic Games não utiliza IDs fixos ou classes semânticas para os preços, o que dificultava a extração via seletores CSS tradicionais.
- **Solução:** Implementação de **Expressões Regulares (Regex)** para varrer o conteúdo textual do cartão do jogo e identificar padrões monetários (`R$ XX,XX`), tornando a extração independente da estrutura HTML.

### Desafio 3: Normalização de Dados

- **Problema:** As fontes retornam dados em formatos incompatíveis (ex: "R$ 50,00", "Gratuito", "Free", "1999" centavos).
- **Solução:** Desenvolvimento da função utilitária `limpar_preco`, que padroniza qualquer entrada para o tipo `float`, permitindo comparações matemáticas precisas.

## 5\. Resultados e Evidências

O sistema organiza automaticamente as evidências visuais. Ao final da execução, uma imagem `resultado_NomeDoJogo.png` é salva no diretório `/screenshots` para auditoria.

**Exemplo de Saída do Console:**

```text
RELATÓRIO DE PREÇOS: MANEATER
==================================================
📍 Steam: Maneater
   Preço: R$ 79,00
------------------------------
📍 Epic Games: Maneater
   Preço: R$ 193,99
------------------------------
==================================================
🏆 MELHOR OFERTA: Steam (R$ 79.00)

📸 Evidência salva em: screenshots/resultado_Maneater.png
```

## 6\. Conclusão

O projeto **GamePriceWars** cumpre todos os critérios de avaliação, demonstrando o uso prático do **Selenium WebDriver** para transformar dados não estruturados da web em informação útil para tomada de decisão.
