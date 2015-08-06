# Entity Linking in Queries: Tasks and Evaluation

Entity Linking in Queries (ELQ) is the task of finding all query interpretations, where each interpretation is a set of semantically related entities.

This task is studied in the following paper and all resources developed within the study are presented in this repository.

    [1] F. Hasibi, K. Balog, and S. E. Bratsberg. "Entity Linking in Queries: Tasks and Evaluation",
    In Proceedings of ACM SIGIR International Conference on the Theory of Information Retrieval (ICTIR '15), Sep 2015.
    DOI: http://dx.doi.org/10.1145/2808194.2809473
	


## Test collections

Two test collections has been developed by the Entity Recognition and Disambiguation (ERD) challenge, referred to as ERD-dev and ERD-test.
The ERD-dev test collection is available from the [ERD website][erd], but the ERD-test is not available for offline processing and can be only accessed through ERD evaluation platform.
[erd]: http://web-ngram.research.microsoft.com/ERD2014/default.aspx?wa=wsignin1.0


Due to the limitations of ERD-dev/test (detailed in [1]), **Y-ERD** test collection is developed.
The test collection is under ``Y-ERD/`` and contains the following files:

-  ``Y-ERD.tsv``: The original Y-ERD test collection, as described in [1].
-  ``Y-ERD_spell-corrected.tsv``: Spell corrected version of Y-ERD, where the queries with spelling errors are linked to the corresponding entities.
- ``spell_corrected_annots.txt``: The difference between original and spell-corrected Y-ERD; spell-corrected annotations are collected in this file.
- ``common_queries_with_ERD.txt``: Queries that are in common between Y-ERD and ERD-dev/test. These queries are removed from Y-ERD to make it possible to train systems using Y-ERD and evaluate them using ERD-dev/test.


## Evaluation scripts

Two evaluation metrics are presented for the ELQ task: ERD-eval and Lean-eval. The corresponding scripts can be found in ``code/evaluator_strict.py`` and ``code/evaluator_lean.py``.

## Qrels

Qrel files are categorised into two groups:

- *Rank-based* under ``qrels/ranked-based/``: The qrels are meant for rank-based evaluation and are in standard TREC format. The results of Table 7 are evaluated against ``qrels_rank_YSQLE.txt``.
- *Set-based* under ``qrels/set-based/``: The qrels are used to evaluate end-to-end performance of an ELQ system using set-based metrics. The format is compatible with the evaluation scripts and used for results of Tables 8 and 9.


## Baseline runs

The baseline runs are categorised into three groups:

- *Mention detection (MD)* under ``runs/MD``: Runs corresponding to Table 6 (in standard TREC format).
- *Semantic Mapping (SM)* under ``runs/SM``: Runs corresponding to Table 9 (in standard TREC format).
- *Interpretation Finding (IF)* under ``runs/IF``: Runs corresponding to Tables 8 and 9 (in our evaluation format).
    - The naming convention for all files is *XXX_YYY.txt*, where *XXX* represents test collection name (ERD-dev or Y-ERD) and *YYY* represents the method name.
	- The entity ranking results are also provided in ``runs/IF/entity-ranking-results`` ins tsv format. This files can be used to test an interpretation finding method, without performing entity ranking (e.g. our GIF algorithm).


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

If you have any questions, feel free to contact *Faegheh Hasibi* at <faegheh.hasibi@idi.ntnu.no>
