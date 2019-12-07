# Trabalho de IA 2019 - 2
Trabalho de IA, fazer um chatbot.

Andamento do trabalho pode ser acompanhado pelo link:

https://github.com/CelsoUliana/Chatbot

Melhor modelo entre os 3 foi o de regressão logistica.
de acordo com o comparativo no comparação.txt (que uso os prints de cada um dos chatbot(modelos))


## Integração.

Utilizado com twilio.

Primeiro passo: Cadastro (Profissional ou teste) na site. Gerar auth token.

Setar o token como variável de ambiente. no windows:

cmd:
set TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
set TWILIO_AUTH_TOKEN=your_auth_token

PowerShell:
$Env:TWILIO_ACCOUNT_SID="ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
$Env:TWILIO_AUTH_TOKEN="your_auth_token"

