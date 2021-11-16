# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1stdWM2jKWlkhPrmtwh8HomBkCDz_5NRe

**Task 07: Querying RDF(s)**
"""

!pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/resources/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

#Namespaces
from rdflib.namespace import RDF, RDFS
ns = Namespace("http://somewhere#")

#RDFlib
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  print('RDFlib: ', s)

#SPARQL
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT
    ?sujeto
  WHERE {
    ?sujeto RDFS:subClassOf ns:Person.
  }
  ''',
  initNs = {"ns": ns, "RDFS": RDFS}
)

for s in g.query(q1):
  print('SPARQL: ',s)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

#Namespaces
from rdflib.namespace import RDF, RDFS
ns = Namespace("http://somewhere#")

#RDFlib
for s, p, o in g.triples((None, RDF.type, None)):
  if o == ns.Person or ((o, RDFS.subClassOf, ns.Person) in g):
    print('RDFlib: ', s)

#SPARQL
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT DISTINCT
    ?sujeto
  WHERE {
    {?sujeto RDF:type ns:Person.} UNION
    {?clase RDFS:subClassOf ns:Person. 
     ?sujeto RDF:type ?clase.} 
  }
  ''',
  initNs = {"ns": ns, "RDF": RDF, "RDFS": RDFS}
)

for s in g.query(q1):
  print('SPARQL: ',s)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

#RDFlib
############
print('RDFlib: ')

#Namespaces
from rdflib.namespace import RDF, RDFS
ns = Namespace("http://somewhere#")

individuals_list = list()
for s, p, o in g.triples((None, RDF.type, None)):
  if o == ns.Person or ((o, RDFS.subClassOf, ns.Person) in g):
    individuals_list.append(s)

grafo_dict_RDFlib = dict()
for i in individuals_list:
  grafo_dict_RDFlib[i] = ['properties: ', [porperties for s,porperties,o in g.triples((i, None, None))]]
  grafo_dict_RDFlib[i].append(['class: ', [o for s, p, o in g.triples((i, RDF.type, None)) if o == ns.Person or ((o, RDFS.subClassOf, ns.Person) in g)]])

#visualizamos el resultado
grafo_dict_RDFlib

#SPARQL
############
print('SPARQL: ')
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery('''
  SELECT DISTINCT
    ?sujeto ?clase
  WHERE {
    {?sujeto RDF:type ns:Person,
     ?clase.} UNION
    {?clase RDFS:subClassOf ns:Person. 
     ?sujeto RDF:type ?clase.} 

  }
  ''',
  initNs = {"ns": ns, "RDF": RDF, "RDFS": RDFS}
)

q2 = prepareQuery('''
  SELECT DISTINCT
    ?sujeto ?properties
  WHERE {
    {?sujeto RDF:type ns:Person,
     ?clase.
     ?sujeto ?properties ?objeto.}
  }
  ''',
  initNs = {"ns": ns, "RDF": RDF, "RDFS": RDFS}
)
grafo_dict_SPARQL = dict()
for s in g.query(q1):
  grafo_dict_SPARQL[s[0]] = ['clase:', s[1]]

for s in g.query(q2):
  grafo_dict_SPARQL[s[0]].append(['properties:', s[1]]) 

#visualizamos el resultado
grafo_dict_SPARQL

