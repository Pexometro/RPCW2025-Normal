# RPCW2025-Normal

## Integração dos dados na ontologia
Implementei um script jsontottl.py responsável por:

- Carregar os ficheiros JSON fornecidos (conceitos.json, disciplinas.json, obras.json, mestres.json, pg57897.json)

- Criar os indivíduos e relacionamentos com base nos dados

- Normalizar os nomes para evitar conflitos com espaços, acentos e pontuação

- Associar corretamente conceitos a períodos históricos, aplicações e disciplinas

- Associar aprendizes a disciplinas e mestres às disciplinas que ensinam

O output do script foi utilizado para gerar a instância final da ontologia (sapientia_ind.ttl), importando a estrutura definida previamente em sapientia_base.ttl.

## Alteração na Ontologia (Perguntas 24 a 27)
Para responder às últimas questões do enunciado, realizei os seguintes passos:

- Adicionei duas novas propriedades à ontologia, diretamente no Protégé:

    :estudaCom (relaciona um Aprendiz com um Mestre)

    :daBasesPara (relaciona uma Disciplina com uma Aplicacao)

Após editar a ontologia com essas propriedades, voltei a importar a ontologia atualizada no ambiente SPARQL, garantindo que as novas relações estivessem disponíveis para a execução das queries CONSTRUCT e INSERT.

Com isso, foi possível inferir novo conhecimento a partir das relações existentes, cumprindo os requisitos do exercício final.

