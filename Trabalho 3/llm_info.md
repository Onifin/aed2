# Informações sobre Modelos de Linguagem Utilizados (LLM)

## Modelos Utilizados

- **GPT-4 (Deep Research Mode)**
- **Gemini 2.5 Pro**

---

## Descrição do Uso dos Modelos

### 1. GPT-4
**Objetivo:** Gerar a base inicial dos dados.

**Prompt Utilizado:**
```
Verifique cada comida descrita na página e crie um json com seus ingredientes baseado nas imagens.

Classifique os ingredientes em uma das seguintes categorias: proteína, carboidrato, gordura, vegetal, fruta, laticínio, tempero.

A lista deve estar no formato json com o nome do prato como chave principal.

Todos os 100 pratos do site devem ser listados.

Cada elemento da lista deve ter o formato do exemplo:

{
"pudim de leite condensado": {
  "carboidrato": ["açúcar"],
  "proteína": ["ovos"],
  "gordura": [],
  "vegetal": [],
  "fruta": [],
  "laticínio": ["leite condensado", "leite integral"],
  "tempero": []
}
}

Site: https://www.penaestrada.blog.br/comidas-tipicas-do-brasil/
```

**Observações:** O JSON gerado apresentou pequenos erros de digitação relacionados à codificação unicode (exemplo: "feijão-fradinho", "azeite de dendê").

---

### 2. Gemini 2.5 Pro
**Objetivo:** Corrigir os erros de codificação no JSON.

**Prompt Utilizado:**
```
Corrija os códigos unicode trocando para as letras acentuadas no json enviado
```

**Observações:** Apenas normalização dos caracteres especiais para garantir a correta apresentação dos ingredientes com acentos.

---

