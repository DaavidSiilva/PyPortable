# PyPortable Installer

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/d929d0dc-f63a-4dcf-b16c-7f457fb5d7f9" />


Uma ferramenta CLI e biblioteca Python para baixar, configurar e gerenciar instalações do Python Portable (Embeddable) automaticamente. Ideal para criar ambientes Python isolados para distribuição sem necessidade de instalação administrativa.

## Funcionalidades

- **Download Automático**: Baixa a versão selecionada do Python Embeddable.
- **Configuração**: Ajusta o arquivo `._pth` para permitir importação de módulos e `site-packages`.
- **Pip & Tools**: Instala automaticamente o `pip`, `setuptools` e `wheel`.
- **Isolamento**: Todo o ambiente fica contido na pasta `.python` (ou onde for configurado).

## Instalação

## Instalação

Instale diretamente do PyPI:

```bash
pip install pyportable
```

### Instalação Local (Desenvolvimento)

1. Clone o repositório.
2. No diretório raiz, execute:

```bash
pip install .
```

## Uso

### Como CLI

Após instalar, o comando `pyportable` estará disponível no seu terminal (CMD, PowerShell ou Bash).

1. Abra o prompt de comando (CMD) ou PowerShell.
2. Navegue até a pasta onde deseja criar o ambiente Python.
3. Execute os comandos abaixo:

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

## Estrutura do Projeto

- `pyportable/`: Código fonte do pacote.
  - `cli.py`: Lógica principal e interface de linha de comando.
  - `config.py`: Definições de versões e URLs.
- `setup.py`: Script de instalação legado/compatibilidade.
- `pyproject.toml`: Configuração moderna de build.
