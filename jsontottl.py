# --------------------------------------------------------------------
# RPCW 2025 - Gerar ontologia completa a partir dos JSON
# --------------------------------------------------------------------
import json
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD

# --------------------------------------------------------------------
# Função de normalização de URIs
# --------------------------------------------------------------------
def norm(t):
    return t.strip().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_") \


# --------------------------------------------------------------------
# Inicializar grafo e namespace
# --------------------------------------------------------------------
g = Graph()
EX = Namespace("http://www.example.org/sapientia#")
g.bind("ex", EX)
g.parse("sapientia_base.ttl", format="turtle")

# --------------------------------------------------------------------
# Carregar JSONs
# --------------------------------------------------------------------
with open("conceitos.json", encoding="utf-8") as f: conceitos = json.load(f)["conceitos"]
with open("disciplinas.json", encoding="utf-8") as f: disciplinas = json.load(f)["disciplinas"]
with open("mestres.json", encoding="utf-8") as f: mestres = json.load(f)["mestres"]
with open("obras.json", encoding="utf-8") as f: obras = json.load(f)["obras"]
with open("pg57897.json", encoding="utf-8") as f: aprendizes = json.load(f)

# --------------------------------------------------------------------
# Guardar indivíduos já criados
# --------------------------------------------------------------------
conceitos_criados = set()
tipos_conhecimento_criados = set()

# --------------------------------------------------------------------
# Criar conceito mínimo se necessário
# --------------------------------------------------------------------
def criar_conceito_minimo(nome):
    uri = URIRef(EX + norm(nome))
    if uri not in conceitos_criados:
        g.add((uri, RDF.type, EX.Conceito))
        g.add((uri, EX.temNome, Literal(nome, datatype=XSD.string)))
        conceitos_criados.add(uri)
    return uri

def criar_tipo_conhecimento_minimo(nome):
    uri = URIRef(EX + norm(nome))
    if uri not in tipos_conhecimento_criados:
        g.add((uri, RDF.type, EX.TipoDeConhecimento))
        g.add((uri, EX.temNome, Literal(nome, datatype=XSD.string)))
        tipos_conhecimento_criados.add(uri)
    return uri

# --------------------------------------------------------------------
# Conceitos
# --------------------------------------------------------------------
for c in conceitos:
    c_uri = criar_conceito_minimo(c["nome"])

    # Período histórico
    if "períodoHistórico" in c:
        ph_uri = URIRef(EX + norm(c["períodoHistórico"]))
        g.add((ph_uri, RDF.type, EX.PeriodoHistorico))
        g.add((ph_uri, EX.temNome, Literal(c["períodoHistórico"], datatype=XSD.string)))
        g.add((c_uri, EX.surgeEm, ph_uri))

    # Aplicações
    for app in c.get("aplicações", []):
        app_uri = URIRef(EX + norm(app))
        g.add((app_uri, RDF.type, EX.Aplicacao))
        g.add((app_uri, EX.temNome, Literal(app, datatype=XSD.string)))
        g.add((c_uri, EX.temAplicacaoEm, app_uri))

    # Conceitos relacionados
    for rel in c.get("conceitosRelacionados", []):
        rel_uri = criar_conceito_minimo(rel)
        g.add((c_uri, EX.estáRelacionadoCom, rel_uri))

# --------------------------------------------------------------------
# Disciplinas
# --------------------------------------------------------------------
for d in disciplinas:
    d_uri = URIRef(EX + norm(d["nome"]))
    g.add((d_uri, RDF.type, EX.Disciplina))
    g.add((d_uri, EX.temNome, Literal(d["nome"], datatype=XSD.string)))

    for tipo in d.get("tiposDeConhecimento", []):
        tipo_uri = criar_tipo_conhecimento_minimo(tipo)
        g.add((d_uri, EX.pertenceA, tipo_uri))

    for conceito in d.get("conceitos", []):
        c_uri = criar_conceito_minimo(conceito)
        g.add((c_uri, EX.éEstudadoEm, d_uri))

# --------------------------------------------------------------------
# Mestres
# --------------------------------------------------------------------
for m in mestres:
    m_uri = URIRef(EX + norm(m["nome"]))
    g.add((m_uri, RDF.type, EX.Mestre))
    g.add((m_uri, EX.temNome, Literal(m["nome"], datatype=XSD.string)))

    ph_uri = URIRef(EX + norm(m["períodoHistórico"]))
    g.add((ph_uri, RDF.type, EX.PeriodoHistorico))
    g.add((m_uri, EX.temPeriodoHistorico, ph_uri))

    for d in m.get("disciplinas", []):
        d_uri = URIRef(EX + norm(d))
        g.add((m_uri, EX.ensina, d_uri))

# --------------------------------------------------------------------
# Obras
# --------------------------------------------------------------------
for o in obras:
    o_uri = URIRef(EX + norm(o["titulo"]))
    g.add((o_uri, RDF.type, EX.Obra))
    g.add((o_uri, EX.temTitulo, Literal(o["titulo"], datatype=XSD.string)))

    autor_uri = URIRef(EX + norm(o["autor"]))
    g.add((o_uri, EX.foiEscritoPor, autor_uri))

    for conceito in o.get("conceitos", []):
        c_uri = criar_conceito_minimo(conceito)
        g.add((o_uri, EX.explica, c_uri))

# --------------------------------------------------------------------
# Aprendizes
# --------------------------------------------------------------------
for a in aprendizes:
    a_uri = URIRef(EX + norm(a["nome"]))
    g.add((a_uri, RDF.type, EX.Aprendiz))
    g.add((a_uri, EX.temNome, Literal(a["nome"], datatype=XSD.string)))
    g.add((a_uri, EX.temIdade, Literal(a["idade"], datatype=XSD.integer)))

    for d in a.get("disciplinas", []):
        d_uri = URIRef(EX + norm(d))
        g.add((a_uri, EX.aprende, d_uri))

# --------------------------------------------------------------------
# Gravar ficheiro TTL final
# --------------------------------------------------------------------
print(g.serialize())