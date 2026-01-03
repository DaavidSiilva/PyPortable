# PyPortable Installer

Uma ferramenta CLI e biblioteca Python para baixar, configurar e gerenciar instalações do Python Portable (Embeddable) automaticamente. Ideal para criar ambientes Python isolados para distribuição sem necessidade de instalação administrativa.

## Funcionalidades

- **Download Automático**: Baixa a versão selecionada do Python Embeddable.
- **Configuração**: Ajusta o arquivo `._pth` para permitir importação de módulos e `site-packages`.
- **Pip & Tools**: Instala automaticamente o `pip`, `setuptools` e `wheel`.
- **Isolamento**: Todo o ambiente fica contido na pasta `.python` (ou onde for configurado).

## Instalação

### Via Código Fonte (Desenvolvimento)

1. Clone o repositório.
2. No diretório raiz, execute:

```bash
pip install .
```

Ou para instalação editável:

```bash
pip install -e .
```

## Uso

### Como CLI

Após instalar, o comando `pyportable` estará disponível no terminal.

**Listar versões disponíveis:**

```bash
pyportable --list
```

**Instalar a versão mais recente na pasta atual (`.python`):**

```bash
pyportable latest
```

**Instalar uma versão específica:**

```bash
pyportable 3.12
```

### Como Biblioteca

Você pode usar o pacote em seus próprios scripts de automação:

```python
from pyportable_installer.cli import main

# Exemplo de chamada direta (simulando argumentos)
import sys
sys.argv = ["pyportable", "latest"]
main()
```

(Futuras versões podem expor uma API mais programática).

## Estrutura do Projeto

- `pyportable_installer/`: Código fonte do pacote.
  - `cli.py`: Lógica principal e interface de linha de comando.
  - `config.py`: Definições de versões e URLs.
- `setup.py`: Script de instalação legado/compatibilidade.
- `pyproject.toml`: Configuração moderna de build.