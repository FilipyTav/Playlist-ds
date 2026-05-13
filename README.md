# Sistema de Playlist
Simulação de backend de um aplicativo de música

---

##  Arquitetura de Dados

Foram usadas diferentes estruturas de dados para cada funcionalidade:

* **Biblioteca Musical (`Library`):** Gerenciada músicas através de uma **Lista Simplesmente Encadeada**.

* **Fila de Reprodução (`PlaylistQueue`):** Implementada como uma **Fila (Queue)** baseada em **Lista Encadeada Simples**, seguindo a lógica **FIFO** (*First-In, First-Out*). As músicas são reproduzidas na ordem em que foram adicionadas.

* **Histórico de Reprodução (`HistoryQueue`):** Registro sequencial das músicas ouvidas, permitindo a visualização cronológica das faixas reproduzidas.

* **Navegação (Interface): (`Menu`)** Os menus do sistema são controlados por uma **Pilha (Stack)**, seguindo a lógica LIFO (*Last-In, First-Out*). Isso permite que o usuário "entre" em submenus e retorne ao menu anterior.

---

## Estrutura do Projeto

| Diretório / Arquivo | Descrição |
| :--- | :--- |
| `src/main.py` | Ponto de entrada da aplicação. |
| `src/ui.py` | Gerencia a interface de usuário e a lógica de exibição de menus. |
| **src/structs/** | **Núcleo de Estruturas de Dados** |
| ├─ `Library.py` | Classe principal da biblioteca. Gerencia a lista de músicas. |
| ├─ `Music.py` | Define a classe `Music`. |
| ├─ `MusicNode.py` | Nó da lista encadeada. Contém o dado e o ponteiro para o próximo. |
| ├─ `PlaylistQueue.py` | Lógica da fila de espera para reprodução (FIFO). |
| ├─ `HistoryQueue.py` | Armazena e exibe as músicas que já foram reproduzidas. |
| ├─ `MenuStack.py` | Pilha para gerenciar as telas da interface (LIFO). |
| └─ `Menu.py` | Definições das opções e lógica visual dos menus. |
| **src/utils/** | **Auxiliares e Estilização** |
| ├─ `strings.py` | Funções úteis de display de strings. |
| ├─ `input.py` | Tratamento e validação de entradas do usuário no terminal. |
| ├─ `colors.py` | Constantes ANSI para formatação visual no terminal. |
| ├─ `errors.py` | Padronização de mensagens de erro e alertas. |
| └─ `types.py` | Definições de tipos customizados para o sistema. |

---

## Como Executar

### 1. Pré-requisitos
* **Python 3.10** ou superior.

### 2. Instalação
1. Clone o repositório para sua máquina:
```bash
git clone https://github.com/FilipyTav/Playlist-ds.git
cd Playlist-ds
```

### 3. Execução
Execute o arquivo principal:
```bash
python src/main.py
```
