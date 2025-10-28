# DIO-Desafio-de-Projeto-2
# Ransomware & Keylogger

> **AVISO IMPORTANTE:** este repositório contém **simulações educacionais**, porém todo cuidado deve ser tomado.  
> **NÃO** execute os scripts em máquinas de produção nem com dados reais. Use **apenas** em VM isolada (Windows 10) com snapshot. Nunca publique chaves nem credenciais.

---

## Objetivo do projeto

Demonstrar, em ambiente controlado, os fluxos básicos de:
- **Ransomware (simulado)** — enumeração de arquivos, criação de cópias criptografadas dos arquivos e geração de mensagem de resgate;
- **Keylogger (simulado)** — captura de teclas em um listener controlado e demonstração de envio.

O foco é educativo: entender o funcionamento, coletar evidências e propor medidas de defesa.

---

## Estrutura do repositório
```
/ (raiz do repositório)
├── README.md
├── YARA.md
├── requirements.txt
├── .gitignore
├── /simulations
|   └── /test_files **(mais arquivos podem ser inclusos)**
|   │   ├── dados.txt
|   │   ├── senhas.txt 
│   ├── ransomware_sim.py
│   ├── descriptografar_sim.py
│   ├── keylogger_sim.py
│   └── keylogger_email_sim.py
├── /images
│   └── exemplo_execucao.png
└── /artifacts
    └── log_execucao.txt
```

     
O que cada arquivo faz (resumido)  
  
ransomware.py — Cria chave de criptografia, percorre test_files/, cria cópias cifradas dos arquivos sobrescrevendo originais, grava um arquivo de resgate e aapresenta em tela cheia, foi criado rotina para que os arquivos ja criptografados nao seja criptografados mais de uma vez caso o "MALWARE" seja executado constantemente antes da execução do descritografador.  

descriptografar.py — lê os dados da pasta  test_files valida header e tenta restaurar os arquivos sobrescrevendo os arquivos critografados usando a mesma chave usada para a criptografia.  

keylogger.py — registra teclas em log com timestamp; É um app-controlado (listener).  

keylogger_email.py — faz envio das teclas digitadas no periodo de 60, constantes do log ao e-mail configurado, zerando o log e recomençando a partir dai;

em ambos scrits do keyloger existe uma lista de teclas que devem ser ignoradas, sem com isso prejudicar a funcionalidade do keylogger, em ambos os scripts de keyloger existem teclas para encerramento sem a necessidade de "matar" o processo.

## Requisitos

Python 3.8+

Bibliotecas (veja requirements.txt): cryptography, pynput

Instalação (Windows):

pip install -r requirements.txt

Preparação segura (passo a passo)

VM isolada: crie uma VM Windows 10 e desative compartilhamentos de pastas sensíveis.

Snapshot: tire um snapshot/checkpoint antes de qualquer teste.

Criar pasta de teste: crie test_files/ com cópias de arquivos não sensíveis (txt, imagens, docs de exemplo).

Nunca comite chaves (*.key) no repositório.

Como executar (comandos e explicações)  
1 — ver o que seria feito

Lista arquivos candidatos e codifica:

python simulations\ransomware.py

2 — Executar o ransomware
python simulations\ransomware.py


Cria test_files/ com arquivos.

Cria LEIA ISSO.TXT.

--fullscreen abre uma janela com a mensagem de resgate (apenas visual).

3 — Restaurar
python simulations\descriptografar.py


Valida os arquivos e grava arquivos restaurados em test_files

4 — Keylogger
python simulations\keylogger.py
# pressione ESC para encerrar


O app encerra quando ESC é pressionado.

5 — Keylogger com envio
python simulations\keylogger_email.py

O "envio" é feito para o e-mail configurado.


## Medidas de segurança e deteção (para o relatório)

# A — Indicadores observáveis (IOCs)

Arquivos criados: LEIA ISSO.TXT


# B — Como detectar

Heurísticas EDR: detecção de criação massiva de arquivos; acessos a muitos arquivos em sequência; processos Python invocando I/O intenso.

Regras [YARA](https://github.com/ADFservice/DIO-Desafio-de-Projeto-2/YARA.md) (ex.: busca por LEIA ISSO.TXT)

Monitoramento de processos persistentes e mudanças em serviços/autorun.

# C — Mitigação e resposta

Isolar host e coletar evidências (imagem, logs, dump de memória).

Restaurar de backup verificado; não pagar resgate.

Hardening: least-privilege, aplicação de patches, application allowlisting, EDR com heurísticas.

Treinamento de usuários contra phishing (vetor comum).
