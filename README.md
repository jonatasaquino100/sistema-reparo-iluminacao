# Reparo de Iluminação Pública

Este é um sistema de controle de pedidos para o reparo de iluminação pública. Ele permite que os usuários registrem e consultem pedidos de reparo, incluindo o endereço do local e o tipo de problema de iluminação (como lâmpada queimada ou acesa o tempo todo).

## Funcionalidades

1. **Consulta de Endereço por CEP**: O usuário pode inserir um CEP para obter o endereço correspondente.
2. **Geração de Pedido**: Após inserir o CEP, número da casa e o tipo de problema, o usuário pode gerar um pedido, que será registrado com um número de protocolo único.
3. **Consulta de Pedidos**: O usuário pode consultar os pedidos já feitos, informando o número do protocolo.
4. **Armazenamento Local**: Os pedidos são armazenados em um arquivo JSON local para persistência de dados.

## Requisitos

- Python 3.x
- Bibliotecas:
  - `tkinter` (para a interface gráfica)
  - `requests` (para consulta de CEP via API)
  - `json` (para manipulação de dados em formato JSON)
  - `os` (para verificar a existência do arquivo de pedidos)

Você pode instalar as dependências com o comando:

```bash
pip install requests
```

## Como Usar

1. **Executando o Programa**  
   Basta rodar o script Python. A interface gráfica será aberta, permitindo a interação com o sistema.

2. **Consulta de CEP**  
   Insira um CEP válido no campo de texto e clique no botão **"Buscar Endereço"**. O sistema fará uma consulta na API do ViaCEP e exibirá o endereço correspondente abaixo do campo.

3. **Gerar Pedido**  
   - Preencha os campos obrigatórios:  
     - **CEP**: Insira o CEP da rua.
     - **Número da casa**: Insira o número da residência.
     - **Tipo de problema**: Escolha o problema a ser informado (ex: lâmpada queimada, acesa o tempo todo, etc).
   - Clique no botão **"Gerar Pedido"**. O sistema irá gerar um número de protocolo único para o pedido e salvará os dados no arquivo `pedidos.json`.

4. **Consultar Meus Pedidos**  
   - Clique no botão **"Meus Pedidos"**.
   - Uma nova janela será aberta onde você poderá inserir o número do protocolo.
   - Após digitar o número do protocolo, clique no botão **"Buscar"**. O sistema exibirá os detalhes do pedido, caso o protocolo exista.
   - Caso o protocolo não seja encontrado, será exibida uma mensagem de erro.

## Estrutura do Arquivo de Dados

Os pedidos são armazenados em um arquivo JSON chamado `pedidos.json`, que contém os seguintes campos:

- `protocolo`: Número único de identificação do pedido.
- `cep`: O CEP informado pelo usuário.
- `endereco`: O endereço completo obtido a partir do CEP.
- `numero`: O número da casa.
- `problema`: O tipo de problema informado pelo usuário.

Exemplo de estrutura de um pedido no arquivo JSON:

```json
[
    {
        "protocolo": 1,
        "cep": "12345-678",
        "endereco": "Rua Exemplo - Bairro Exemplo - Cidade/UF",
        "numero": "100",
        "problema": "Lâmpada queimada"
    }
]
