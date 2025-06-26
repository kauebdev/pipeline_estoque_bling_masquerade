## 1. Coleta e Identificação da Origem dos Dados

**1.1 Recebimento do arquivo de origem**<br>
- Pode ser uma **planilha manual** (`.xlsx` ou `.csv`)<br>
- Ou uma **exportação automática** via **XML** de outro ERP<br>

**1.2 Classificação do tipo de arquivo**<br>
- Se for **Excel ou CSV** → seguir direto para leitura com `pandas`<br>
- Se for **XML** → converter para `DataFrame`, extraindo apenas os campos úteis<br>

---

## 2. Classificação da Planilha (Tipo e Finalidade)

**2.1 Tipo de produto**<br>
- `Acabado`: produto final, vendável<br>
- `Não acabado`: insumos, matéria-prima, semiacabados<br>

**2.2 Tipo de movimentação**<br>
- `Entrada de estoque`<br>
- `Saída de estoque`<br>

**2.3 Padronização inicial da leitura**<br>
- Em planilhas: garantir que o cabeçalho está correto (`skiprows`, `usecols`)<br>
- Em XML: mapear e extrair campos como `código`, `descrição`, `quantidade`, `tipo`, etc.<br>

---

## 3. Extração e Padronização da Estrutura (Extract)

**3.1 Padronizar a estrutura da planilha**<br>
- Corrigir e padronizar nomes das colunas<br>
- Verificar e corrigir tipos de dados (`int`, `float`, `str`)<br>
- Garantir que todas as colunas mínimas estão presentes<br>

**3.2 Corrigir conteúdos inconsistentes**<br>
- Remover espaços desnecessários<br>
- Uniformizar maiúsculas/minúsculas<br>
- Tratar valores nulos, códigos incompletos ou inválidos<br>

---

## 4. Transformação e Validação (Transform)

**4.1 Carregar produtos já existentes no Bling via API**<br>
- Obter lista atual de produtos<br>
- Fazer `merge` com a planilha para identificar:<br>
  - Produtos que **já existem**<br>
  - Produtos que **precisam ser criados**<br>

**4.2 Identificar e separar produtos novos**<br>
- `Não acabados` (insumos, matéria-prima)<br>
- `Acabados` (prontos para venda)<br>

**4.3 Validar os dados**<br>
- Conferir consistência de:<br>
  - Códigos<br>
  - Tipos<br>
  - Quantidades<br>

---

## 5. Carga: Cadastro de Produtos no Bling (Load)

**5.1 Cadastrar produtos novos via API do Bling**<br>
- Endpoint: `/produto`<br>
- Dados mínimos: `código`, `descrição`, `tipo`, `unidade`<br>

**5.2 Verificar resposta da API**<br>
- Confirmar se o cadastro foi bem-sucedido<br>
- Gerar log de sucesso ou erro<br>

---

## 6. Movimentação de Estoque (Entrada / Saída)

**6.1 Gerar pedidos de estoque via API Bling**<br>
- Tipo `compra` → para entrada<br>
- Tipo `venda` → para saída<br>

**6.2 Gerar XML do pedido com:**<br>
- `código` do produto<br>
- `quantidade`<br>
- `valor` (pode ser fixo ou simbólico)<br>
- `cliente/fornecedor` padrão<br>

**6.3 Enviar pedido via API**<br>
- Endpoint: `/pedido`<br>
- O Bling realiza o ajuste de estoque automaticamente<br>

**6.4 Verificar resposta da API**<br>
- Sucesso ou falha por produto<br>
- Gerar log de erros para revisão manual<br>

---

## 7. Logs e Auditoria

**7.1 Gerar log completo do processo**<br>
- Produtos criados<br>
- Pedidos enviados<br>
- Erros encontrados<br>

**7.2 Armazenar arquivos tratados**<br>
- Mover arquivos processados para pasta de backup/versionamento<br>