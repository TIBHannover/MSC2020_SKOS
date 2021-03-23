# MSC 2020 - SKOSification procedure

State of this document: draft

- missing information is marked as [x]
- discussion points are given as question-answer-pairs, where questions are marked as 'Q\d:' and answers given directly below by 'A\d:'

This document describes how the SKOS version 2020 has been created.
The current version is available at <https://github.com/runnwerth/MSC2020_SKOS/blob/main/msc-2020-suggestion2-incomplete.ttl>

[[_TOC_]]

## General information on the 2010 SKOS version of MSC and its creation

Legacy modelling decisions for the MSC 2010 SKOS version are described in the following papers:

- Christoph Lange, Patrick Ion, Anastasia Dimou, Charalampos Bratsas, Wolfram Sperber, Michael Kohlhase, and Ioannis Antoniou: Bringing Mathematics to the Web of Data: The Case of the Mathematics Subject Classification. In: E. Simperl et al. (Eds.): ESWC 2012, LNCS 7295, pp. 763–777, 2012 .
- tbd: others, e.g. <http://msc2010.org/resources/MSC/2010/info/>

These were followed wherever possible.

## Input for the SKOS version of MSC 2020

The input for creating the SKOS was an export from the [x] database provided by [x] as a .xslx-file with the following structure:

### Sheet 1: MSC 2020

| code | text | description |
| ---      |  ------  |----------|
| 00-01   | Introductory exposition (textbooks, tutorial papers, etc.) pertaining to mathematics in general   | Introductory exposition (textbooks, tutorial papers, etc.) pertaining to mathematics in general   |

### Sheet 2: MSC 2010

This sheet was structured just like sheet 1 but containing data from MSC 2010.

### Sheet 3: Transformation

| MSC2010 | MSC2020 | (A)ufspaltung / (N)eu / (V)erschiebung / (Z)usammenführung |
| ---      |  ------  |----------|
| 00   |  | |
|  | 00A27, 00A64 | N |
| 00A73, 00A79 | 00A79 | Z |
| 01 | |  |
| 01-08 |  | gelöscht |

## Tools used during the creation of the SKOS version of MSC 2020

- OpenRefine 3.4.1
- Protégé 5.5.0 with memory set to 3641 MB via Java -Xmx setting

We used OpenRefine to create all the basic triples for the MSC 2020. The output of our work with OpenRefine is a table in which some columns contain usable RDF triples. These can be exported and imported into a preprepared .tt-file declaring all the namespaces and containing additional data, e.g. metadata.

Some additions have been made with Protégé's SPARQL-Plug-In snap. The respective queries are documented in the .ttl-file as `rdfs:comment` of `msc:`.

Introduction and materials related to the used tools:  

- [OpenRefine user documentation](https://docs.openrefine.org/)
- [General Refine Expression Language (GREL)](https://docs.openrefine.org/manual/expressions#grel-general-refine-expression-language)
- [GREL Functions](https://docs.openrefine.org/manual/grelfunctions)
- [Introduction to Open Refine by the Library of Illinois](https://guides.library.illinois.edu/openrefine/grel)
- [Introduction to Open Refine at programminghistorian.org](https://programminghistorian.org/en/lessons/fetch-and-parse-data-with-openrefine)

## Definition of modelling tasks

To create a complete SKOS version of MSC 2020 that resembles the structure of MSC 2020 requires to perform the following tasks:

Task 0: Set up a basic .tt-file.

- declaration of namespaces
- declaration of imports
- declaration of metadata

Task 1: Basic triples

- create identifiers for each class
- define the rdf:type of elements
- create basic triples (skos:prefLabel, skos:notation, skos:scopeNote, skos:inScheme) from information in the table

Task 2: Concept hierarchy

- create the concept hierarchy (skos:broader/skos:narrower)

Task 3: Internal references

- create internal references between MSC skos:Concepts (mscvocab:seeMainly, mscvoab:seeAlso, mscvocab:seeConditionally)
- create instances of rdf:Statement to describe the condition that holds for an `mscvocab:seeConditionally` relation between two MSC concepts

Task 4: Historical references [still open, see <https://github.com/runnwerth/MSC2020_SKOS/issues/6>]

- create links between MSC 2020 concepts and MSC 2010 and add descriptions of the changes

Task 5: Create collections

- create instances of skos:Collection and define which are its `skos:member`.

Task 6: Create MSC-specific scope notes

- create instances of `mscvocab:NotUseScopeNote`, `mscvocab:UseScopeNote` and `mscvocab:MustUseScopeNote`

Q1: The tasks have not been performed in that order, which is why some of the OpenRefine operations documented below are not given in a consecutive order (e.g. *Task2: Concept hierarchy* has been done after introducing a filter criterium for *Task 3: Internal references* so that Step 7 will be described after Steps 8-x). Is that confusing?

## Documentation of modelling steps

In the following we will describe the basic modelling tasks that have been performed.

### Task 0: Set up a basic .tt-file

The triples we generate with OpenRefine operations can - after export from OpenRefine - be copypasted into this file. OpenRefine export option: Do not quote text.

```Turtle
@prefix : <http://msc.org/resources/MSC/msc2020/> .
@prefix msc: <http://msc.org/resources/MSC/msc2020/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix mscvocab: <http://msc.org/resources/MSC/msc2020/mscvocab#> .
@base <http://msc.org/resources/MSC/msc2020/> .
@prefix dc11: <http://purl.org/dc/elements/1.1/> .
@prefix dc: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .

<http://msc.org/resources/MSC/msc2020/> 
              rdf:type owl:Ontology , skos:ConceptScheme;
              owl:imports mscvocab: ,
                          rdf: ,
                          <http://www.w3.org/2004/02/skos/core> ;
              dc11:description "Mathematics Subject Classification 2020 Edition"@en ;
              dc11:title "MSC2020";
              rdfs:label "MSC 2020"@en, "Mathematics Subject Classification 2020"@en .
```

### Task 1: Basic triples

#### **Step 1: Create an OpenRefine project with the .xlsx-file**

The project was set up with the following paramaters checked in:

- parse data as: Excel file
- parse next 1 line(s) as column headers
- store blank rows
- store blank cells as nulls
- store file source (file name, URLs) in each row

OpenRefine allows different kinds of operations on the cells and tables of the table. These operations are documented and exportable as json-Code and can thus be re-used on the same or similar data in a different project. The documented operations performed in OpenRefine make use of the imported table's index in the json-Code. The same import parameters should be used when setting up a new project of the data since otherwise the OpenRefine operations would refer to incorrect indices the table resulting from the import.

#### **Step 2: Create identifiers for each class**

The identifiers for each class will be added by adding a new column to the table using the value of each cell in in column `code`.

```json
[
    [
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "code",
    "expression": "grel:\"<http://msc.org/resources/MSC/msc2020/\"+value+\">\"",
    "onError": "store-error",
    "newColumnName": "Concept Identifier",
    "columnInsertIndex": 2,
    "description": "Create column Concept Identifier at index 2 based on column code using expression grel:\"<http://msc.org/resources/MSC/msc2020/\"+value+\">\""
  }
]
```

To keep this table slightly more readable and to better distinguish import data from new data, we move the new column to the end of the table:

```json
[
      {
    "op": "core/column-move",
    "columnName": "Concept Identifier",
    "index": 4,
    "description": "Move column Concept Identifier to position 4"
  }
]
```

#### **Step 3: Create the lable triples**

As labels we use the text in column `text` and the label is created as follows:

```json
[
    {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "text",
    "expression": "grel:cells['Concept Identifier'].value+\"skos:prefLabel\"+\" \\\"\"+value+\"\\\"\"+\"@en .\"",
    "onError": "store-error",
    "newColumnName": "Label triple",
    "columnInsertIndex": 3,
    "description": "Create column Label triple at index 3 based on column text using expression grel:cells['Concept Identifier'].value+\"skos:prefLabel\"+\" \\\"\"+value+\"\\\"\"+\"@en .\""
  },
  {
    "op": "core/column-move",
    "columnName": "Label triple",
    "index": 5,
    "description": "Move column Label triple to position 5"
  }
]
```

#### **Step 4: Create rdf:type statement**

MSC entries are typed as skos:Concept.

```json
[
    {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "Concept Identifier",
    "expression": "grel:value+\" a skos:Concept .\"",
    "onError": "store-error",
    "newColumnName": "typification triple",
    "columnInsertIndex": 5,
    "description": "Create column typification triple at index 5 based on column Concept Identifier using expression grel:value+\" a skos:Concept .\""
  },
  {
    "op": "core/column-move",
    "columnName": "typification triple",
    "index": 6,
    "description": "Move column typification triple to position 6"
  }
]
```

#### **Step 5: Create skos:inScheme statement**

```json
[
    {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "Concept Identifier",
    "expression": "grel:value+\" skos:inScheme <http://msc.org/resources/MSC/msc2020/> .\"",
    "onError": "store-error",
    "newColumnName": "skos:in Scheme triple",
    "columnInsertIndex": 5,
    "description": "Create column skos:in Scheme triple at index 5 based on column Concept Identifier using expression grel:value+\" skos:inScheme <http://msc.org/resources/MSC/msc2020/> .\""
  },
  {
    "op": "core/column-move",
    "columnName": "skos:in Scheme triple",
    "index": 7,
    "description": "Move column skos:in Scheme triple to position 7"
  }
]
```

#### **Step 6: Create skos:notation statement**

```json
[
    {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "code",
    "expression": "grel:cells['Concept Identifier'].value+\" skos:notation \"+\"\\\"\"+value+\"\\\"^^xsd:string .\"",
    "onError": "store-error",
    "newColumnName": "notation triples",
    "columnInsertIndex": 2,
    "description": "Create column notation triples at index 2 based on column code using expression grel:cells['Concept Identifier'].value+\" skos:notation \"+\"\\\"\"+value+\"\\\"^^xsd:string .\""
  },
  {
    "op": "core/column-move",
    "columnName": "notation triples",
    "index": 8,
    "description": "Move column notation triples to position 8"
  }
]
```

### Task 2: Concept Hierarchy

We wanted to give the hierarchical relation by skos:broader, leaving skos:narrower implied. This required to assign each lover-level concept to the appropriate super-ordinate concept. This can be done with OpenRefine or Protégé and a SPARQL `CONSTRUCT` query. We describe the OpenRefine process:

#### **Step 8: Create a column for each concept's superordinate's identifier**

Due to the MSC's great notation, this is a matter of some replacements and concatenations:

```json
[
    {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "text",
          "name": "code",
          "columnName": "code",
          "query": "xx",
          "mode": "text",
          "caseSensitive": false,
          "invert": true
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "Concept Identifier",
    "expression": "grel:value.replace(/-\\d\\d/, \"-XX\").replace(/\\d\\d>/, \"xx>\")",
    "onError": "store-error",
    "newColumnName": "Identifier skos:broader",
    "columnInsertIndex": 5,
    "description": "Create column Identifier skos:broader at index 5 based on column Concept Identifier using expression grel:value.replace(/-\\d\\d/, \"-XX\").replace(/\\d\\d>/, \"xx>\")"
  },
  {
    "op": "core/column-move",
    "columnName": "Identifier skos:broader",
    "index": 10,
    "description": "Move column Identifier skos:broader to position 10"
  }
]
```

#### **Step 9: Create the skos:broader statements**

```json
[
    {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "Identifier skos:broader",
    "expression": "grel:cells['Concept Identifier'].value+\" skos:broader \"+value+\" .\"",
    "onError": "store-error",
    "newColumnName": "Hierarchy triples",
    "columnInsertIndex": 11,
    "description": "Create column Hierarchy triples at index 11 based on column Identifier skos:broader using expression grel:cells['Concept Identifier'].value+\" skos:broader \"+value+\" .\""
  },
  {
    "op": "core/column-move",
    "columnName": "Identifier skos:broader",
    "index": 9,
    "description": "Move column Identifier skos:broader to position 9"
  },
  {
    "op": "core/column-move",
    "columnName": "Hierarchy triples",
    "index": 10,
    "description": "Move column Hierarchy triples to position 10"
  }
]
```

### Task 3: Internal References

Internal references between MSC concepts are described in column `description` of our input file. There are three types of internal references between MSC concepts which are captured by mscvocabs three object properties:

- mscvocab:seeAlso
- mscvocab:seeMainly
- mscvocab:seeConditionally

Next to these kinds of reference, the text in the column ´description´ shows other types of information, e.g. it repeats the content from column `text` or other natural language text describing a condition under which a reference between two concepts holds. Textual information in this column is often very homogeneous and standardised to a certain degree and can therefore easily be transformed to triples working with mscvocabs object properties. However, there are also some irregularities e.g. there seems to be no standardised order of information types in the column, and on some occasions, there are some deviations from the regular notation in this column.

To be able to create relations between MSC concepts which are `owl:NamedIndividuals` resp. instances of skos:Concept, we needed to extract the notations of these related concepts from the column to perform further steps like identifier creation and triple creation as done before in *Task 1: Basic triples*. Due to the different types of information, the non-standardised order of their occurrence and the irregularities, this required a huge number of steps. The basic aim of these steps was to split the whole set of relevant cells of the column `description` up into columns where all cells contain the same type of information and to split up multi-valued cells with only one value per cell. The values in these new columns can then be used as objects of triples and are either URIs or literals.

Here is an example of a relevant cell with multiple types of information:

| code | text | description |
| --- | --- | --- |
|03B45| Modal logic (including the logic of norms) | Modal logic (including the logic of norms) \{For knowledge and belief, see 03B42; for temporal logic, see 03B44; for provability logic, see also 03F45\}|

To adress the "multi-valuedness" and irregularities in this column, we tried to split the cells up according to their shared regularies (using text factes, selection, inversion and text filters) until there was only an irregular rest left. We will not describe all the factes and filters in detail, here, but they and all operations done on column `description` and resulting new columns are documented below in *Step 10: Taiming the `description` column*.

In the given example, from the column `description` we took the information that `03B45` links to the concepts `03B42`, `03B44`, `03F45` and that there is a condition applying to these relations, which is given as natural language text, e.g. `For knowledge and belief`. For the relation between the concepts, we use a self-defined property `mscvocab:seeConditionally`, e.g.:

`<http://msc.org/resources/MSC/msc2020/03B45> mscvocab:seeConditionally <http://msc.org/resources/MSC/msc2020/03B42>`

While this is straightforward, providing the condition requires an additional structural solution, e.g. an annotation on a relation or referring to the relation by its own identifier and making statements about this resource (reification). We decided to follow the solution of MSC 2010 as much as possible and used reification. The entity representing the statement to be commented on, is typed as an instance of `mscvocab:SeeForStatement`, a subclass of rdf:Statement newly introduced to mscvocab 2020. Different from MSC 2010, we described a statement's `rdf:subject`, `rdf:predicate`, and `rdf:object` (instead of `mscvocab:forTarget` as used by MSC 2010). We provided the condition for the `mscovab:seeConditionally` relation between two concepts via `mscvocab:scope` just like MSC 2010:

```turtle
msc:SeeForStatement-03B45-to-03B42 rdf:type owl:NamedIndividual ,
                                            mscvocab:SeeForStatement ;
                                   rdf:object <http://msc.org/resources/MSC/msc2020/03B42> ;
                                   rdf:predicate mscvocab:seeConditionally ;
                                   rdf:subject <http://msc.org/resources/MSC/msc2020/03B45> ;
                                   mscvocab:scope "For knowledge and belief"^^rdf:XMLLiteral .
```

Q2: Where should we introduce mscvocab? Should we comment on the fact, that we started without it? I think I did not very much refer to it before... And the OpenRefine code snippets are all using properties like `msc:seeAlso` because we defined them within the file/namespace of the MSC data - which is very confusing.

Just like in MSC 2010, we also wanted to make the relation between a concept and a statement it is the `rdf:subject` of, explicit by `mscvocab:seeFor`:

`<http://msc.org/resources/MSC/msc2020/03B45> mscvocab:seeFor msc:SeeForStatement-03B45-to-03B42 .`

#### **Step 7: Set a filter criterion for working on Task 3**

In this preparatory step we filter out all cells that do not have any internal references, i.e. cells whose content is identical to the content of column `text`.

```json
[
    {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "text",
    "expression": "grel:if(cells['description'].value == value , true, false)",
    "onError": "store-error",
    "newColumnName": "comparison text/description",
    "columnInsertIndex": 3,
    "description": "Create column comparison text/description at index 3 based on column text using expression grel:if(cells['description'].value == value , true, false)"
  },
  {
    "op": "core/column-move",
    "columnName": "comparison text/description",
    "index": 9,
    "description": "Move column comparison text/description to position 9"
  }
]


#### **Step 10: Taiming the `description` column**

Step 10 incluedes a great number of very fine-grained operations, sometimes even edits on single cells. The following code will not be re-usable in future MSC SKOS conversions and is limited to the data at hand.

```json
[
    {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "comparison text/description",
          "expression": "value",
          "columnName": "comparison text/description",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": false,
                "l": "false"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "description",
          "expression": "value",
          "columnName": "description",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "None of the above, but in this section",
                "l": "None of the above, but in this section"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "baseColumnName": "description",
    "expression": "grel:value",
    "onError": "store-error",
    "newColumnName": "description - extract 1",
    "columnInsertIndex": 4,
    "description": "Create column description - extract 1 at index 4 based on column description using expression grel:value"
  },
  {
    "op": "core/column-move",
    "columnName": "description - extract 1",
    "index": 12,
    "description": "Move column description - extract 1 to position 12"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "comparison text/description",
          "expression": "value",
          "columnName": "comparison text/description",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": false,
                "l": "false"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "text",
          "name": "description",
          "columnName": "description",
          "query": "\\[See also \\d",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        }
      ],
      "mode": "record-based"
    },
    "baseColumnName": "description",
    "expression": "grel:value",
    "onError": "store-error",
    "newColumnName": "description extract 2",
    "columnInsertIndex": 4,
    "description": "Create column description extract 2 at index 4 based on column description using expression grel:value"
  },
  {
    "op": "core/column-move",
    "columnName": "description extract 2",
    "index": 13,
    "description": "Move column description extract 2 to position 13"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "comparison text/description",
          "expression": "value",
          "columnName": "comparison text/description",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": false,
                "l": "false"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "text",
          "name": "description",
          "columnName": "description",
          "query": "\\{For ",
          "mode": "text",
          "caseSensitive": false,
          "invert": false
        }
      ],
      "mode": "record-based"
    },
    "baseColumnName": "description",
    "expression": "grel:value",
    "onError": "store-error",
    "newColumnName": "description - extract 3 \\{For",
    "columnInsertIndex": 4,
    "description": "Create column description - extract 3 \\{For at index 4 based on column description using expression grel:value"
  },
  {
    "op": "core/column-move",
    "columnName": "description - extract 3 \\{For",
    "index": 14,
    "description": "Move column description - extract 3 \\{For to position 14"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "comparison text/description",
          "expression": "value",
          "columnName": "comparison text/description",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": false,
                "l": "false"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "text",
          "name": "description",
          "columnName": "description",
          "query": "[See mainly",
          "mode": "text",
          "caseSensitive": false,
          "invert": false
        }
      ],
      "mode": "record-based"
    },
    "baseColumnName": "description",
    "expression": "grel:value",
    "onError": "store-error",
    "newColumnName": "description - extract 4 [See mainly",
    "columnInsertIndex": 4,
    "description": "Create column description - extract 4 [See mainly at index 4 based on column description using expression grel:value"
  },
  {
    "op": "core/column-move",
    "columnName": "description - extract 4 [See mainly",
    "index": 15,
    "description": "Move column description - extract 4 [See mainly to position 15"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "comparison text/description",
          "expression": "value",
          "columnName": "comparison text/description",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": false,
                "l": "false"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "text",
          "name": "description",
          "columnName": "description",
          "query": "[Consider also classification numbers pertaining to Section 01-XX]",
          "mode": "text",
          "caseSensitive": false,
          "invert": false
        }
      ],
      "mode": "record-based"
    },
    "baseColumnName": "description",
    "expression": "grel:value",
    "onError": "store-error",
    "newColumnName": "description - extract 5",
    "columnInsertIndex": 4,
    "description": "Create column description - extract 5 at index 4 based on column description using expression grel:value"
  },
  {
    "op": "core/column-move",
    "columnName": "description - extract 5",
    "index": 16,
    "description": "Move column description - extract 5 to position 16"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "comparison text/description",
          "expression": "value",
          "columnName": "comparison text/description",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": false,
                "l": "false"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "description - extract 1",
          "expression": "value",
          "columnName": "description - extract 1",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "list",
          "name": "description extract 2",
          "expression": "value",
          "columnName": "description extract 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "list",
          "name": "description - extract 3 \\{For",
          "expression": "value",
          "columnName": "description - extract 3 \\{For",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "list",
          "name": "description - extract 4 [See mainly",
          "expression": "value",
          "columnName": "description - extract 4 [See mainly",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "list",
          "name": "description - extract 5",
          "expression": "value",
          "columnName": "description - extract 5",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "baseColumnName": "description",
    "expression": "grel:value",
    "onError": "set-to-blank",
    "newColumnName": "description - extract 6 rest",
    "columnInsertIndex": 4,
    "description": "Create column description - extract 6 rest at index 4 based on column description using expression grel:value"
  },
  {
    "op": "core/column-move",
    "columnName": "description - extract 6 rest",
    "index": 17,
    "description": "Move column description - extract 6 rest to position 17"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "description - extract 1",
          "expression": "value",
          "columnName": "description - extract 1",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "None of the above, but in this section",
                "l": "None of the above, but in this section"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "description - extract 1",
    "expression": "grel:cells[\"Concept Identifier\"].value+\" skos:scopeNote \\\"\"+value+\"\\\"@en .\"",
    "onError": "store-error",
    "newColumnName": "skos:scopeNote \"None of the above\"@en",
    "columnInsertIndex": 13,
    "description": "Create column skos:scopeNote \"None of the above\"@en at index 13 based on column description - extract 1 using expression grel:cells[\"Concept Identifier\"].value+\" skos:scopeNote \\\"\"+value+\"\\\"@en .\""
  },
  {
    "op": "core/column-split",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "description extract 2",
          "expression": "value",
          "columnName": "description extract 2",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "description extract 2",
    "guessCellType": true,
    "removeOriginalColumn": false,
    "mode": "separator",
    "separator": "[",
    "regex": false,
    "maxColumns": 2,
    "description": "Split column description extract 2 by separator"
  },
  {
    "op": "core/multivalued-cell-split",
    "columnName": "description extract 2 2",
    "keyColumnName": "File",
    "mode": "separator",
    "separator": "];",
    "regex": false,
    "description": "Split multi-valued cells in column description extract 2 2"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "File",
    "description": "Fill down cells in column File"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "code",
    "description": "Fill down cells in column code"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "text",
    "description": "Fill down cells in column text"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "description",
    "description": "Fill down cells in column description"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Concept Identifier",
    "description": "Fill down cells in column Concept Identifier"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "comparison text/description",
    "description": "Fill down cells in column comparison text/description"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "description extract 2 2",
          "expression": "value",
          "columnName": "description extract 2 2",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "text",
          "name": "description extract 2 2",
          "columnName": "description extract 2 2",
          "query": "^See also",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        },
        {
          "type": "text",
          "name": "description extract 2 2",
          "columnName": "description extract 2 2",
          "query": "\\d\\b\\]|x\\b\\]|,|x\\b|5\\b",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "description extract 2 2",
    "expression": "grel:value",
    "onError": "store-error",
    "newColumnName": "description extract 2 2 1",
    "columnInsertIndex": 17,
    "description": "Create column description extract 2 2 1 at index 17 based on column description extract 2 2 using expression grel:value"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "description extract 2 2",
          "expression": "value",
          "columnName": "description extract 2 2",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "text",
          "name": "description extract 2 2",
          "columnName": "description extract 2 2",
          "query": "^See also|^ ",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        },
        {
          "type": "text",
          "name": "description extract 2 2",
          "columnName": "description extract 2 2",
          "query": "\\d\\b\\]|x\\b\\]|,|x\\b|5\\b",
          "mode": "regex",
          "caseSensitive": false,
          "invert": true
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "description extract 2 2",
    "expression": "grel:value",
    "onError": "store-error",
    "newColumnName": "dewcription extract 2 2 2 (rest)",
    "columnInsertIndex": 17,
    "description": "Create column dewcription extract 2 2 2 (rest) at index 17 based on column description extract 2 2 using expression grel:value"
  },
  {
    "op": "core/column-move",
    "columnName": "dewcription extract 2 2 2 (rest)",
    "index": 18,
    "description": "Move column dewcription extract 2 2 2 (rest) to position 18"
  },
  {
    "op": "core/multivalued-cell-split",
    "columnName": "description extract 2 2 1",
    "keyColumnName": "File",
    "mode": "separator",
    "separator": "\\{",
    "regex": false,
    "description": "Split multi-valued cells in column description extract 2 2 1"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "File",
    "description": "Fill down cells in column File"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "code",
    "description": "Fill down cells in column code"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "text",
    "description": "Fill down cells in column text"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "description",
    "description": "Fill down cells in column description"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Concept Identifier",
    "description": "Fill down cells in column Concept Identifier"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "comparison text/description",
    "description": "Fill down cells in column comparison text/description"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "description extract 2 2 1",
          "expression": "value",
          "columnName": "description extract 2 2 1",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "text",
          "name": "description extract 2 2 1",
          "columnName": "description extract 2 2 1",
          "query": "^For",
          "mode": "regex",
          "caseSensitive": false,
          "invert": true
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "description extract 2 2 1",
    "expression": "grel:value.replace(\"See also\", \"\").replace(\"]\", \"\")",
    "onError": "store-error",
    "newColumnName": "see also reference",
    "columnInsertIndex": 18,
    "description": "Create column see also reference at index 18 based on column description extract 2 2 1 using expression grel:value.replace(\"See also\", \"\").replace(\"]\", \"\")"
  },
  {
    "op": "core/multivalued-cell-split",
    "columnName": "see also reference",
    "keyColumnName": "File",
    "mode": "separator",
    "separator": ", ",
    "regex": false,
    "description": "Split multi-valued cells in column see also reference"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "File",
    "description": "Fill down cells in column File"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "code",
    "description": "Fill down cells in column code"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "text",
    "description": "Fill down cells in column text"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "description",
    "description": "Fill down cells in column description"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Concept Identifier",
    "description": "Fill down cells in column Concept Identifier"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "comparison text/description",
    "description": "Fill down cells in column comparison text/description"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "see also reference",
    "expression": "value.trim()",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column see also reference using expression value.trim()"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "see also reference",
          "expression": "value",
          "columnName": "see also reference",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "text",
          "name": "see also reference",
          "columnName": "see also reference",
          "query": "\\d\\d[A-Z]\\d\\d|\\d\\d-XX|\\d\\d-xx|\\d\\d[A-Z]xx|\\d\\d-\\d\\d",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        },
        {
          "type": "text",
          "name": "see also reference",
          "columnName": "see also reference",
          "query": "and|especially|in particular",
          "mode": "regex",
          "caseSensitive": false,
          "invert": true
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "see also reference",
    "expression": "grel:cells[\"Concept Identifier\"].value+\" msc:seeAlso \"+\"<http://msc.org/resources/MSC/msc2020/\"+value+\"> .\"",
    "onError": "store-error",
    "newColumnName": "msc:seeAlso ?y",
    "columnInsertIndex": 19,
    "description": "Create column msc:seeAlso ?y at index 19 based on column see also reference using expression grel:cells[\"Concept Identifier\"].value+\" msc:seeAlso \"+\"<http://msc.org/resources/MSC/msc2020/\"+value+\"> .\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:seeAlso ?y",
          "expression": "value",
          "columnName": "msc:seeAlso ?y",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "list",
          "name": "see also reference",
          "expression": "value",
          "columnName": "see also reference",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "08B05 and 08B10",
                "l": "08B05 and 08B10"
              }
            },
            {
              "v": {
                "v": "and 82D25",
                "l": "and 82D25"
              }
            },
            {
              "v": {
                "v": "14Lxx and 20Gxx",
                "l": "14Lxx and 20Gxx"
              }
            },
            {
              "v": {
                "v": "especially 53C70",
                "l": "especially 53C70"
              }
            },
            {
              "v": {
                "v": "especially 51F15",
                "l": "especially 51F15"
              }
            },
            {
              "v": {
                "v": "in particular 03C60",
                "l": "in particular 03C60"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "see also reference",
    "expression": "grel:value.replace(\"in particular \", \"\").replace(\"especially \", \"\")",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column see also reference using expression grel:value.replace(\"in particular \", \"\").replace(\"especially \", \"\")"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:seeAlso ?y",
          "expression": "value",
          "columnName": "msc:seeAlso ?y",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "list",
          "name": "see also reference",
          "expression": "value",
          "columnName": "see also reference",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "08B05 and 08B10",
                "l": "08B05 and 08B10"
              }
            },
            {
              "v": {
                "v": "and 82D25",
                "l": "and 82D25"
              }
            },
            {
              "v": {
                "v": "14Lxx and 20Gxx",
                "l": "14Lxx and 20Gxx"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "see also reference",
    "expression": "grel:value.replace(\"and \", \"|\").replace(\" \", \"\")",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column see also reference using expression grel:value.replace(\"and \", \"|\").replace(\" \", \"\")"
  },
  {
    "op": "core/multivalued-cell-split",
    "columnName": "see also reference",
    "keyColumnName": "File",
    "mode": "separator",
    "separator": "|",
    "regex": false,
    "description": "Split multi-valued cells in column see also reference"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "File",
    "description": "Fill down cells in column File"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "code",
    "description": "Fill down cells in column code"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "text",
    "description": "Fill down cells in column text"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "description",
    "description": "Fill down cells in column description"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Concept Identifier",
    "description": "Fill down cells in column Concept Identifier"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "comparison text/description",
    "description": "Fill down cells in column comparison text/description"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:seeAlso ?y",
          "expression": "value",
          "columnName": "msc:seeAlso ?y",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "list",
          "name": "see also reference",
          "expression": "value",
          "columnName": "see also reference",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "Hodge conjecture",
                "l": "Hodge conjecture"
              }
            },
            {
              "v": {
                "v": "Krull dimension (associative rings and algebras)",
                "l": "Krull dimension (associative rings and algebras)"
              }
            },
            {
              "v": {
                "v": "etc.",
                "l": "etc."
              }
            },
            {
              "v": {
                "v": "Laurent polynomial rings (associative algebraic aspects)",
                "l": "Laurent polynomial rings (associative algebraic aspects)"
              }
            }
          ],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "see also reference",
    "expression": "grel:cells[\"Concept Identifier\"].value+\" msc:seeAlso <http://msc.org/resources/MSC/msc2020/\"+value+\"> .\"",
    "onError": "store-error",
    "newColumnName": "msc:seeAlso ?y 2",
    "columnInsertIndex": 19,
    "description": "Create column msc:seeAlso ?y 2 at index 19 based on column see also reference using expression grel:cells[\"Concept Identifier\"].value+\" msc:seeAlso <http://msc.org/resources/MSC/msc2020/\"+value+\"> .\""
  },
  {
    "op": "core/column-move",
    "columnName": "msc:seeAlso ?y 2",
    "index": 20,
    "description": "Move column msc:seeAlso ?y 2 to position 20"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "dewcription extract 2 2 2 (rest)",
          "expression": "value",
          "columnName": "dewcription extract 2 2 2 (rest)",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": " elliptic complexes",
                "l": " elliptic complexes"
              }
            },
            {
              "v": {
                "v": " module theory in a category-theoretic context; Morita equivalence and duality",
                "l": " module theory in a category-theoretic context; Morita equivalence and duality"
              }
            },
            {
              "v": {
                "v": " mixture models",
                "l": " mixture models"
              }
            }
          ],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "dewcription extract 2 2 2 (rest)",
    "expression": "grel:cells[\"Concept Identifier\"].value+\" skos:scopeNote \"+\"\\\"\"+value.replace(\"]\", \"\\\"\")+\"@en ;skos:editorialNote \\\"Add the relations to --00 subcategories in other sections with SPARQL and regex filters\\\"@en .\"",
    "onError": "store-error",
    "newColumnName": "skos:scopeNote 2",
    "columnInsertIndex": 22,
    "description": "Create column skos:scopeNote 2 at index 22 based on column dewcription extract 2 2 2 (rest) using expression grel:cells[\"Concept Identifier\"].value+\" skos:scopeNote \"+\"\\\"\"+value.replace(\"]\", \"\\\"\")+\"@en ;skos:editorialNote \\\"Add the relations to --00 subcategories in other sections with SPARQL and regex filters\\\"@en .\""
  },
  {
    "op": "core/multivalued-cell-split",
    "columnName": "description - extract 5",
    "keyColumnName": "File",
    "mode": "separator",
    "separator": "[",
    "regex": false,
    "description": "Split multi-valued cells in column description - extract 5"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "File",
    "description": "Fill down cells in column File"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "code",
    "description": "Fill down cells in column code"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "text",
    "description": "Fill down cells in column text"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "description",
    "description": "Fill down cells in column description"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "comparison text/description",
    "description": "Fill down cells in column comparison text/description"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Concept Identifier",
    "description": "Fill down cells in column Concept Identifier"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "description - extract 5",
          "expression": "value",
          "columnName": "description - extract 5",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "Consider also classification numbers pertaining to Section 01-XX]",
                "l": "Consider also classification numbers pertaining to Section 01-XX]"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "description - extract 5",
    "expression": "grel:cells[\"Concept Identifier\"].value+\" skos:scopeNote \\\"\"+value.replace(\"]\", \"\")+\"\\\"@en .\"",
    "onError": "store-error",
    "newColumnName": "skos:scopeNote \"Consider history classes\"",
    "columnInsertIndex": 26,
    "description": "Create column skos:scopeNote \"Consider history classes\" at index 26 based on column description - extract 5 using expression grel:cells[\"Concept Identifier\"].value+\" skos:scopeNote \\\"\"+value.replace(\"]\", \"\")+\"\\\"@en .\""
  },
  {
    "op": "core/column-split",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "description - extract 4 [See mainly",
          "expression": "value",
          "columnName": "description - extract 4 [See mainly",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "description - extract 4 [See mainly",
    "guessCellType": true,
    "removeOriginalColumn": false,
    "mode": "separator",
    "separator": "[",
    "regex": false,
    "maxColumns": 2,
    "description": "Split column description - extract 4 [See mainly by separator"
  },
  {
    "op": "core/multivalued-cell-split",
    "columnName": "description - extract 4 [See mainly 2",
    "keyColumnName": "File",
    "mode": "separator",
    "separator": ";",
    "regex": false,
    "description": "Split multi-valued cells in column description - extract 4 [See mainly 2"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "File",
    "description": "Fill down cells in column File"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "code",
    "description": "Fill down cells in column code"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "text",
    "description": "Fill down cells in column text"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "description",
    "description": "Fill down cells in column description"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Concept Identifier",
    "description": "Fill down cells in column Concept Identifier"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "comparison text/description",
    "description": "Fill down cells in column comparison text/description"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "description - extract 4 [See mainly 2",
          "expression": "value",
          "columnName": "description - extract 4 [See mainly 2",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "text",
          "name": "description - extract 4 [See mainly 2",
          "columnName": "description - extract 4 [See mainly 2",
          "query": "^See mainly",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "description - extract 4 [See mainly 2",
    "expression": "grel:value.replace(\"See mainly \", \"\").replace(\"]\", \"\").replace(\", and also \", \"|\").replace(\", \", \"|\")",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column description - extract 4 [See mainly 2 using expression grel:value.replace(\"See mainly \", \"\").replace(\"]\", \"\").replace(\", and also \", \"|\").replace(\", \", \"|\")"
  },
  {
    "op": "core/multivalued-cell-split",
    "columnName": "description - extract 4 [See mainly 2",
    "keyColumnName": "File",
    "mode": "separator",
    "separator": "|",
    "regex": false,
    "description": "Split multi-valued cells in column description - extract 4 [See mainly 2"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "File",
    "description": "Fill down cells in column File"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "code",
    "description": "Fill down cells in column code"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "text",
    "description": "Fill down cells in column text"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "description",
    "description": "Fill down cells in column description"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Concept Identifier",
    "description": "Fill down cells in column Concept Identifier"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "comparison text/description",
    "description": "Fill down cells in column comparison text/description"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "description - extract 4 [See mainly 2",
          "expression": "value",
          "columnName": "description - extract 4 [See mainly 2",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "text",
          "name": "description - extract 4 [See mainly 2",
          "columnName": "description - extract 4 [See mainly 2",
          "query": "see also",
          "mode": "text",
          "caseSensitive": false,
          "invert": true
        }
      ],
      "mode": "row-based"
    },
    "columnName": "description - extract 4 [See mainly 2",
    "expression": "grel:value.replace(\"especially \", \"\")",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column description - extract 4 [See mainly 2 using expression grel:value.replace(\"especially \", \"\")"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "description - extract 4 [See mainly 2",
          "expression": "value",
          "columnName": "description - extract 4 [See mainly 2",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "text",
          "name": "description - extract 4 [See mainly 2",
          "columnName": "description - extract 4 [See mainly 2",
          "query": "see also",
          "mode": "text",
          "caseSensitive": false,
          "invert": true
        }
      ],
      "mode": "row-based"
    },
    "columnName": "description - extract 4 [See mainly 2",
    "expression": "grel:value.replace(/.+y /, \"\").replace(\"]\", \"\")",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column description - extract 4 [See mainly 2 using expression grel:value.replace(/.+y /, \"\").replace(\"]\", \"\")"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "description - extract 4 [See mainly 2",
          "expression": "value",
          "columnName": "description - extract 4 [See mainly 2",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "text",
          "name": "description - extract 4 [See mainly 2",
          "columnName": "description - extract 4 [See mainly 2",
          "query": "see also",
          "mode": "text",
          "caseSensitive": false,
          "invert": true
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "description - extract 4 [See mainly 2",
    "expression": "grel:cells[\"Concept Identifier\"].value+\" msc:seeMainly <http://msc.org/resources/MSC/msc2020/\"+value+\"> .\"",
    "onError": "store-error",
    "newColumnName": "msc:seeMainly",
    "columnInsertIndex": 27,
    "description": "Create column msc:seeMainly at index 27 based on column description - extract 4 [See mainly 2 using expression grel:cells[\"Concept Identifier\"].value+\" msc:seeMainly <http://msc.org/resources/MSC/msc2020/\"+value+\"> .\""
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "description - extract 4 [See mainly 2",
          "expression": "value",
          "columnName": "description - extract 4 [See mainly 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": " see also 46S10, 47S10]",
                "l": " see also 46S10, 47S10]"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "msc:seeAlso ?y",
          "expression": "value",
          "columnName": "msc:seeAlso ?y",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "description - extract 4 [See mainly 2",
    "expression": "grel:value.replace(\" see also \", \"\").replace(\"]\", \"\").replace(\", \", \"|\")",
    "onError": "store-error",
    "newColumnName": "missed see also reference",
    "columnInsertIndex": 27,
    "description": "Create column missed see also reference at index 27 based on column description - extract 4 [See mainly 2 using expression grel:value.replace(\" see also \", \"\").replace(\"]\", \"\").replace(\", \", \"|\")"
  },
  {
    "op": "core/multivalued-cell-split",
    "columnName": "missed see also reference",
    "keyColumnName": "File",
    "mode": "separator",
    "separator": "|",
    "regex": false,
    "description": "Split multi-valued cells in column missed see also reference"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "File",
    "description": "Fill down cells in column File"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "code",
    "description": "Fill down cells in column code"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "text",
    "description": "Fill down cells in column text"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "description",
    "description": "Fill down cells in column description"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Concept Identifier",
    "description": "Fill down cells in column Concept Identifier"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "comparison text/description",
    "description": "Fill down cells in column comparison text/description"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "missed see also reference",
          "expression": "value",
          "columnName": "missed see also reference",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "46S10",
                "l": "46S10"
              }
            },
            {
              "v": {
                "v": "47S10",
                "l": "47S10"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "missed see also reference",
    "expression": "grel:cells[\"Concept Identifier\"].value+\" msc:seeAlso <http://msc.org.resources/MSC/msc2020/\"+value+\"> .\"",
    "onError": "store-error",
    "newColumnName": "msc:seeAlso ?y 3",
    "columnInsertIndex": 28,
    "description": "Create column msc:seeAlso ?y 3 at index 28 based on column missed see also reference using expression grel:cells[\"Concept Identifier\"].value+\" msc:seeAlso <http://msc.org.resources/MSC/msc2020/\"+value+\"> .\""
  },
  {
    "op": "core/column-split",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "description - extract 3 \\{For",
          "expression": "value",
          "columnName": "description - extract 3 \\{For",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "text",
          "name": "description - extract 3 \\{For",
          "columnName": "description - extract 3 \\{For",
          "query": "\\{",
          "mode": "text",
          "caseSensitive": false,
          "invert": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "description - extract 3 \\{For",
    "guessCellType": true,
    "removeOriginalColumn": false,
    "mode": "separator",
    "separator": "\\{",
    "regex": false,
    "maxColumns": 2,
    "description": "Split column description - extract 3 \\{For by separator"
  },
  {
    "op": "core/multivalued-cell-split",
    "columnName": "description - extract 3 \\{For 2",
    "keyColumnName": "File",
    "mode": "separator",
    "separator": ";",
    "regex": false,
    "description": "Split multi-valued cells in column description - extract 3 \\{For 2"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "File",
    "description": "Fill down cells in column File"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "code",
    "description": "Fill down cells in column code"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "text",
    "description": "Fill down cells in column text"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "description",
    "description": "Fill down cells in column description"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Concept Identifier",
    "description": "Fill down cells in column Concept Identifier"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "comparison text/description",
    "description": "Fill down cells in column comparison text/description"
  },
  {
    "op": "core/multivalued-cell-split",
    "columnName": "description - extract 3 \\{For 2",
    "keyColumnName": "File",
    "mode": "separator",
    "separator": "[",
    "regex": false,
    "description": "Split multi-valued cells in column description - extract 3 \\{For 2"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "File",
    "description": "Fill down cells in column File"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "code",
    "description": "Fill down cells in column code"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "text",
    "description": "Fill down cells in column text"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "description",
    "description": "Fill down cells in column description"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Concept Identifier",
    "description": "Fill down cells in column Concept Identifier"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "comparison text/description",
    "description": "Fill down cells in column comparison text/description"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "text",
          "name": "description - extract 3 \\{For 2",
          "columnName": "description - extract 3 \\{For 2",
          "query": "^See also",
          "mode": "regex",
          "caseSensitive": false,
          "invert": true
        },
        {
          "type": "text",
          "name": "description - extract 3 \\{For 2",
          "columnName": "description - extract 3 \\{For 2",
          "query": ", see",
          "mode": "text",
          "caseSensitive": false,
          "invert": true
        }
      ],
      "mode": "row-based"
    },
    "columnName": "description - extract 3 \\{For 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "For WKB methods see 34E20\\}"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "For WKB methods, see 34E20\\}"
      }
    ],
    "description": "Mass edit cells in column description - extract 3 \\{For 2"
  },
  {
    "op": "core/column-split",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "description - extract 3 \\{For 2",
          "expression": "value",
          "columnName": "description - extract 3 \\{For 2",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "text",
          "name": "description - extract 3 \\{For 2",
          "columnName": "description - extract 3 \\{For 2",
          "query": "^See also",
          "mode": "regex",
          "caseSensitive": false,
          "invert": true
        }
      ],
      "mode": "row-based"
    },
    "columnName": "description - extract 3 \\{For 2",
    "guessCellType": true,
    "removeOriginalColumn": false,
    "mode": "separator",
    "separator": ", see",
    "regex": false,
    "maxColumns": 2,
    "description": "Split column description - extract 3 \\{For 2 by separator"
  },
  {
    "op": "core/column-rename",
    "oldColumnName": "description - extract 3 \\{For 2 1",
    "newColumnName": "msc:scope",
    "description": "Rename column description - extract 3 \\{For 2 1 to msc:scope"
  },
  {
    "op": "core/column-rename",
    "oldColumnName": "description - extract 3 \\{For 2 2",
    "newColumnName": "msc:ForTarget",
    "description": "Rename column description - extract 3 \\{For 2 2 to msc:ForTarget"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:scope",
          "expression": "value",
          "columnName": "msc:scope",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "msc:scope",
    "expression": "value.trim()",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column msc:scope using expression value.trim()"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": "\\d\\d[A-Z]\\d\\d\\\\}",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": ",",
          "mode": "text",
          "caseSensitive": false,
          "invert": true
        }
      ],
      "mode": "row-based"
    },
    "columnName": "msc:ForTarget",
    "expression": "grel:value.replace(\"\\\\}\", \"\").replace(\"also \",  \"\").replace(\"especially \", \"\").replace(\"mainly \", \"\")",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column msc:ForTarget using expression grel:value.replace(\"\\\\}\", \"\").replace(\"also \",  \"\").replace(\"especially \", \"\").replace(\"mainly \", \"\")"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": "also",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": ",",
          "mode": "text",
          "caseSensitive": false,
          "invert": true
        }
      ],
      "mode": "row-based"
    },
    "columnName": "msc:ForTarget",
    "expression": "grel:value.replace(\"also \", \"\")",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column msc:ForTarget using expression grel:value.replace(\"also \", \"\")"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": "\\d\\d\\\\}",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": ",",
          "mode": "text",
          "caseSensitive": false,
          "invert": true
        }
      ],
      "mode": "row-based"
    },
    "columnName": "msc:ForTarget",
    "expression": "grel:value.replace(\"\\\\}\", \"\")",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column msc:ForTarget using expression grel:value.replace(\"\\\\}\", \"\")"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": "XX\\\\}",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": ",",
          "mode": "text",
          "caseSensitive": false,
          "invert": true
        }
      ],
      "mode": "row-based"
    },
    "columnName": "msc:ForTarget",
    "expression": "grel:value.replace(\"\\\\}\", \"\")",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column msc:ForTarget using expression grel:value.replace(\"\\\\}\", \"\")"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": "~",
          "mode": "text",
          "caseSensitive": false,
          "invert": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": ",",
          "mode": "text",
          "caseSensitive": false,
          "invert": true
        }
      ],
      "mode": "row-based"
    },
    "columnName": "msc:ForTarget",
    "expression": "grel:value.replace(\"~\", \"\")",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column msc:ForTarget using expression grel:value.replace(\"~\", \"\")"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": " 00A79 and Sections 70-XX through 86-XX",
                "l": " 00A79 and Sections 70-XX through 86-XX"
              }
            },
            {
              "v": {
                "v": " the classification number -04 in that area\\}",
                "l": " the classification number -04 in that area\\}"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": ",",
          "mode": "text",
          "caseSensitive": false,
          "invert": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": "\\d\\d, \\d\\d",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "msc:ForTarget",
    "expression": "grel:value.replace(\", \", \"|\")",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column msc:ForTarget using expression grel:value.replace(\", \", \"|\")"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": " 00A79 and Sections 70-XX through 86-XX",
                "l": " 00A79 and Sections 70-XX through 86-XX"
              }
            },
            {
              "v": {
                "v": " the classification number -04 in that area\\}",
                "l": " the classification number -04 in that area\\}"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": ",",
          "mode": "text",
          "caseSensitive": false,
          "invert": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": "xx, \\d\\d",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "msc:ForTarget",
    "expression": "grel:value.replace(\", \", \"|\")",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column msc:ForTarget using expression grel:value.replace(\", \", \"|\")"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": " 74Axx, or other parts of 74-XX\\}",
                "l": " 74Axx, or other parts of 74-XX\\}"
              }
            },
            {
              "v": {
                "v": " the classification number -04 in that area\\}",
                "l": " the classification number -04 in that area\\}"
              }
            },
            {
              "v": {
                "v": " 00A79 and Sections 70-XX through 86-XX",
                "l": " 00A79 and Sections 70-XX through 86-XX"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": "}",
          "mode": "text",
          "caseSensitive": false,
          "invert": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": "",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "msc:ForTarget",
    "expression": "grel:value.replace(\"\\\\}\", \"\")",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column msc:ForTarget using expression grel:value.replace(\"\\\\}\", \"\")"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": " 00A79 and Sections 70-XX through 86-XX",
                "l": " 00A79 and Sections 70-XX through 86-XX"
              }
            },
            {
              "v": {
                "v": " 74Axx, or other parts of 74-XX\\}",
                "l": " 74Axx, or other parts of 74-XX\\}"
              }
            },
            {
              "v": {
                "v": " the classification number -04 in that area\\}",
                "l": " the classification number -04 in that area\\}"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": "also|mainly|in particular|especially",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        },
        {
          "type": "text",
          "name": "msc:ForTarget",
          "columnName": "msc:ForTarget",
          "query": "",
          "mode": "regex",
          "caseSensitive": false,
          "invert": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "msc:ForTarget",
    "expression": "grel:value.replace(\"especially \", \"\").replace(\"also \", \"\").replace(\"mainly \", \"\")",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column msc:ForTarget using expression grel:value.replace(\"especially \", \"\").replace(\"also \", \"\").replace(\"mainly \", \"\")"
  },
  {
    "op": "core/multivalued-cell-split",
    "columnName": "msc:ForTarget",
    "keyColumnName": "File",
    "mode": "separator",
    "separator": "|",
    "regex": false,
    "description": "Split multi-valued cells in column msc:ForTarget"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "File",
    "description": "Fill down cells in column File"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "code",
    "description": "Fill down cells in column code"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "text",
    "description": "Fill down cells in column text"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "description",
    "description": "Fill down cells in column description"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Concept Identifier",
    "description": "Fill down cells in column Concept Identifier"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "comparison text/description",
    "description": "Fill down cells in column comparison text/description"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": " 00A79 and Sections 70-XX through 86-XX",
                "l": " 00A79 and Sections 70-XX through 86-XX"
              }
            },
            {
              "v": {
                "v": " 74Axx, or other parts of 74-XX\\}",
                "l": " 74Axx, or other parts of 74-XX\\}"
              }
            },
            {
              "v": {
                "v": " the classification number -04 in that area\\}",
                "l": " the classification number -04 in that area\\}"
              }
            }
          ],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "code",
    "expression": "value.trim()",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column code using expression value.trim()"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": " 00A79 and Sections 70-XX through 86-XX",
                "l": " 00A79 and Sections 70-XX through 86-XX"
              }
            },
            {
              "v": {
                "v": " 74Axx, or other parts of 74-XX\\}",
                "l": " 74Axx, or other parts of 74-XX\\}"
              }
            },
            {
              "v": {
                "v": " the classification number -04 in that area\\}",
                "l": " the classification number -04 in that area\\}"
              }
            }
          ],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "msc:ForTarget",
    "expression": "value.trim()",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column msc:ForTarget using expression value.trim()"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": " 00A79 and Sections 70-XX through 86-XX",
                "l": " 00A79 and Sections 70-XX through 86-XX"
              }
            },
            {
              "v": {
                "v": " 74Axx, or other parts of 74-XX\\}",
                "l": " 74Axx, or other parts of 74-XX\\}"
              }
            },
            {
              "v": {
                "v": " the classification number -04 in that area\\}",
                "l": " the classification number -04 in that area\\}"
              }
            }
          ],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "msc:ForTarget",
    "expression": "grel:\"<http://msc.org/resources/MSC/msc2020/seeForStatement-\"+cells[\"code\"].value+\"-to-\"+value+\">\"",
    "onError": "store-error",
    "newColumnName": "For-x-see-y statement identifier",
    "columnInsertIndex": 28,
    "description": "Create column For-x-see-y statement identifier at index 28 based on column msc:ForTarget using expression grel:\"<http://msc.org/resources/MSC/msc2020/seeForStatement-\"+cells[\"code\"].value+\"-to-\"+value+\">\""
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "msc:scope",
    "description": "Fill down cells in column msc:scope"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "description - extract 3 \\{For 2",
    "description": "Fill down cells in column description - extract 3 \\{For 2"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "description - extract 3 \\{For",
    "description": "Fill down cells in column description - extract 3 \\{For"
  },
  {
    "op": "core/fill-down",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "description - extract 3 \\{For 1",
    "description": "Fill down cells in column description - extract 3 \\{For 1"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": " 00A79 and Sections 70-XX through 86-XX",
                "l": " 00A79 and Sections 70-XX through 86-XX"
              }
            },
            {
              "v": {
                "v": " 74Axx, or other parts of 74-XX\\}",
                "l": " 74Axx, or other parts of 74-XX\\}"
              }
            },
            {
              "v": {
                "v": " the classification number -04 in that area\\}",
                "l": " the classification number -04 in that area\\}"
              }
            }
          ],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "For-x-see-y statement identifier",
    "expression": "grel:value+\"a msc:seeForStatement ; rdf:subject \"+cells[\"Concept Identifier\"].value+\"; rdf:predicate msc:seeFor ; rdf:object <http://msc.org/resources/MSC/msc2020/\"+cells[\"msc:ForTarget\"].value+\"> ; msc:scope \\\"\"+cells[\"msc:scope\"].value+\"\\\"^^rdf:XMLLiteral .\"",
    "onError": "store-error",
    "newColumnName": "For-x-see-y statements",
    "columnInsertIndex": 29,
    "description": "Create column For-x-see-y statements at index 29 based on column For-x-see-y statement identifier using expression grel:value+\"a msc:seeForStatement ; rdf:subject \"+cells[\"Concept Identifier\"].value+\"; rdf:predicate msc:seeFor ; rdf:object <http://msc.org/resources/MSC/msc2020/\"+cells[\"msc:ForTarget\"].value+\"> ; msc:scope \\\"\"+cells[\"msc:scope\"].value+\"\\\"^^rdf:XMLLiteral .\""
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "msc:ForTarget",
          "expression": "value",
          "columnName": "msc:ForTarget",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": " 00A79 and Sections 70-XX through 86-XX",
                "l": " 00A79 and Sections 70-XX through 86-XX"
              }
            },
            {
              "v": {
                "v": " 74Axx, or other parts of 74-XX\\}",
                "l": " 74Axx, or other parts of 74-XX\\}"
              }
            },
            {
              "v": {
                "v": " the classification number -04 in that area\\}",
                "l": " the classification number -04 in that area\\}"
              }
            }
          ],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "For-x-see-y statement identifier",
    "expression": "grel:cells[\"Concept Identifier\"].value+\" msc:seeFor \"+value+\" .\"",
    "onError": "store-error",
    "newColumnName": "seeFor triples",
    "columnInsertIndex": 29,
    "description": "Create column seeFor triples at index 29 based on column For-x-see-y statement identifier using expression grel:cells[\"Concept Identifier\"].value+\" msc:seeFor \"+value+\" .\""
  }
]
```

Some triples could not be created in this process and have been added manually or by the help of SPARQL queries in Protege. The details on that need to be reconstructed from the [commit history](https://github.com/runnwerth/MSC2020_SKOS/commits/main) or issues resulting from *Step 10*:

- [issue 3](https://github.com/runnwerth/MSC2020_SKOS/issues/3)
- [issue 7](https://github.com/runnwerth/MSC2020_SKOS/issues/7)

The SPARQL queries are documented in the Turtle file as an `rdfs:comment` on `msc:` .

#### **Step 11: Take text from column `description` over to the SKOS version as a scopeNote**

In the end, we decided that it would be a good idea to store the text from column `description` as a skos:scopeNote - just to make sure.

```json
[
      {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "comparison text/description",
          "expression": "value",
          "columnName": "comparison text/description",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": false,
                "l": "false"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "baseColumnName": "description",
    "expression": "grel:cells[\"Concept Identifier\"].value+\"skos:scopeNote \\\"\"+value+\"\\\"@en .\"",
    "onError": "store-error",
    "newColumnName": "scopeNote for descriptions that differ from text",
    "columnInsertIndex": 4,
    "description": "Create column scopeNote for descriptions that differ from text at index 4 based on column description using expression grel:cells[\"Concept Identifier\"].value+\"skos:scopeNote \\\"\"+value+\"\\\"@en .\""
  },
  {
    "op": "core/column-move",
    "columnName": "scopeNote for descriptions that differ from text",
    "index": 40,
    "description": "Move column scopeNote for descriptions that differ from text to position 40"
  }
]
```

### Task 4: Historical references

[still open, see <https://github.com/runnwerth/MSC2020_SKOS/issues/6>]

### Task 5: Create collections

See SPARQL queries documented in [msc-2020-suggestion2-incomplete.ttl](https://github.com/runnwerth/MSC2020_SKOS/blob/main/msc-2020-suggestion2-incomplete.ttl).

### Task 6: Create MSC-specific scope notes

Sub-task 1 `mscvocab:NotUseScopeNote`

- identify relevant concepts --> value of `skos:prefLabel` contains the text fragment "do not use"
- create instances for `mscvocab:NotUseScopeNote` for each identfied  concept
- create triples between a) the skos:Concept and the newly created instances of `mscvocab:NotUseScopeNote` with `skos:scopeNote`, b) between the newly created instances of `mscvocab:NotUseScopeNote` and the value of `skos:prefLabel` with `mscvocab:scope`

Sub-task 3 `mscvocab:MustUseScopeNote`

- Proceed as before. Filter criterion ist "must".

Sub-task 2 `mscvocab:UseScopeNote`

- Proceed as before. Filter criterion is ". Use".
