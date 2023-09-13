# Entity Linking in Queries: Tasks and Evaluation

This repository contains resources developed within the following study:

    F. Hasibi, K. Balog, and S. E. Bratsberg. "Entity Linking in Queries: Tasks and Evaluation",
    In Proceedings of ACM SIGIR International Conference on the Theory of Information Retrieval (ICTIR '15), Sep 2015.
    DOI: http://dx.doi.org/10.1145/2808194.2809473

You can check the [paper](https://hasibi.com/files/ictir2015-elq.pdf) and [presentation](http://www.slideshare.net/FaeghehHasibi/icitir2015elq) for detailed information.	

## Tasks

We differentiate between two tasks within the problem area of entity linking in queries: semantic mapping and interpretation finding.

- **Semantic mapping (SM)** is a tool for aiding users with suggestions that could be beneficial for enhancing navigation or for contextualization. The task is to return a ranked list of entities that are semantically related to the query.
- **Interpretation finding (IF)** is a means to machine-understanding of queries, which, in our opinion, is the ultimate goal of entity linking in queries. The task is to return interpretations of the query, where an interpretation is defined as a set of entities, with non-overlapping mentions, that are semantically compatible with the query text.
  

## Test collections

We use the following test collections in the paper:

- **YSQLE** is used for evaluating SM. It is the Yahoo Search Query Log to Entities dataset, available from [Yahoo! Webscope](http://webscope.sandbox.yahoo.com/catalog.php?datatype=l). We restricted entities to the ones present in both DBpedia and Freebase.
- **ERD-dev** is used for evaluating IF. The test set is developed by the Entity Recognition and Disambiguation (ERD) Challenge, and is available from the [ERD website](http://web-ngram.research.microsoft.com/ERD2014).  We use the collection as it is; note that annotations are restricted to entities from a specific Freebase snapshot, provided by the ERD Challenge.
- **Y-ERD** is used for evaluating IF. It is developed as part of our study, based on YSQL. Entities are restricted to ones present in both DBpedia and the Freebase snapshot, provided by the ERD challenge.

### Y-ERD  

The test collection is under ``Y-ERD/`` and contains the following files:

- ``Y-ERD.tsv``: The original Y-ERD test collection that is used in our paper (entities with spelling errors are not linked).
- ``Y-ERD_spell-corrected.tsv``: Spell corrected version of Y-ERD, where the queries with spelling errors are linked to the corresponding entities.
- ``spell_corrected_annots.txt``: The difference between original and spell-corrected Y-ERD; spell-corrected annotations are collected in this file.
- ``common_queries_with_ERD.txt``: Queries that are in common between Y-ERD and ERD-dev/test. These queries are removed from Y-ERD to make it possible to train systems using Y-ERD and evaluate them using ERD-dev/test.


*Note:* All files are tab-delimited. The .tsv files contain a header line, which labels each field.


## Evaluation scripts

  - Semantic mapping uses rank-based evaluation. We use `trec_eval` for that.

  - Results for the interpretation finding task can be evaluted using the "ERD way" (strict) or using "lean evaluation" (proposed in the paper). The corresponding scripts are ``code/evaluator_strict.py`` and ``code/evaluator_lean.py``.


## Qrels

Qrel files are categorised into two groups:

- *Rank-based* under ``qrels/SM/``: The qrels are meant for evaluating semantic mapping using rank-based metrics. They are in standard TREC format. Specifically, the results of Table 4 in the paper are evaluated against ``qrels_SM_YSQLE.txt``.
- *Set-based* under ``qrels/IF/``: The qrels are used to evaluate interpretation finding using set-based metrics. The format is compatible with the evaluation scripts and used for results presented in Tables 5 and 6 of the paper.


## Runs

The baseline runs are categorised into three groups:

- *Mention detection (MD)* under ``runs/MD``: Runs corresponding to Table 3 (in standard TREC format),  evaluated against ``qrels_SM_YSQLE.txt``, ``qrels_SM_Y-ERD.txt``, and ``qrels_SM_ERD-dev.txt``.
- *Semantic Mapping (SM)* under ``runs/SM``: Runs corresponding to Table 4 (in standard TREC format), evaluated against ``qrels_SM_YSQLE.txt``.
- *Interpretation Finding (IF)* under ``runs/IF``: Runs corresponding to Tables 5 and 6 (in our evaluation format), evaluated against ``qrels_IF_Y-ERD.txt`` and ``qrels_IF_ERD-dev.txt``.
    - The naming convention for all files is *XXX_YYY.txt*, where *XXX* represents test collection name (ERD-dev or Y-ERD) and *YYY* represents the method name. Files starting with XXX should be evaluated against ``qrels_IF_XXX.txt``.
    - The entity ranking results are also provided in ``runs/IF/entity-ranking-results`` in tsv format. These files can be used to perform interpretation finding by taking a ranked list of entities as input (e.g., as is done in our GIF algorithm).


## GIF algorithm

The Greedy Interpetation Finding (GIF) algorithm presented in the paper can be found under ``code/GIF.py``.


## Citation

If you use the resources presented in this repository, please cite:

```
@inproceedings{Hasibi:2015:ELQ, 
   author =    {Hasibi, Faegheh and Balog, Krisztian and Bratsberg, Svein Erik},
   title =     {Entity Linking in Queries: Tasks and Evaluation},
   booktitle = {Proceedings of ACM SIGIR International Conference on the Theory of Information Retrieval},
   series =    {ICTIR '15},
   year =      {2015},
   publisher = {ACM}
   DOI =       {http://dx.doi.org/10.1145/2808194.2809473}
} 
```


## Contact

Should you have any questions, please contact Faegheh Hasibi at <f.hasibi@cs.ru.nl>.
