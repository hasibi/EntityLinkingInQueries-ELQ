"""
=============================================================================

This script evaluates query interpretations based on Lean evaluation metrics;
macro averaging of precision, recall and F-measure.

Lean evaluation metrics are average of interpretation_based and entity-based metrics:
    - prec = (prec_entity + prec_inter) / 2
    - recall = (recall_entity + recall_inter) / 2
    - f1 = (f1_entity + f1_inter) / 2

- Interpretation-based metrics compare query interpretations with ground truth.
- Entity-based metrics collapse borders of query interpretations and compare all retrieved entities with ground truth.

For detailed information see:
    F. Hasibi, K. Balog, and S. E. Bratsberg. "Entity Linking in Queries: Tasks and Evaluation",
    In Proceedings of ACM SIGIR International Conference on the Theory of Information Retrieval (ICTIR '15), Sep 2015.
    DOI: http://dx.doi.org/10.1145/2808194.2809473

=============================================================================
Usage:
    python evaluation_erd.py <qrel_file> <result_file>
e.g.
    python evaluation_erd.py qrels_sets_ERD-dev.txt ERD-dev_MLMcg-GIF.txt
=============================================================================

Notes:
1. Qrel and Result files are in the same format:
     - Tab-separated file, where each line indicates an interpretation set:
         qid    confidence_score   en1 en2 ...

2. Qrel file contains all queries, even the ones without any annotation.
    Qrel files can be found under: qrels/set_based/

2. Results files of our experiments can be found under: runs/IF/

=============================================================================
@author: Faegheh Hasibi (faegheh.hasibi@idi.nunu.no)
=============================================================================
"""

from __future__ import division
import sys
from evaluator_erd import Evaluator, parse_file, erd_eval_query


def lean_eval_query(query_qrels, query_results):
    """
    Evaluates a single query.
    Each metrics is the average of interpretation-based and entity-based metrics.

    :param query_qrels: Query interpretations from Qrel [{en1, en2, ..}, ..]
    :param query_results: Query interpretations from result file [{en1, en2, ..}, ..]
    :return: precision, recall, and F1 for a query.
    """
    # Interpretation-based metrics
    inter_metrics = erd_eval_query(query_qrels, query_results)

    # Entity-based metrics
    query_qrel_ens = get_ens(query_qrels)
    query_res_ens = get_ens(query_results)
    entity_metrics = erd_eval_query(query_qrel_ens, query_res_ens)

    # Average of two metrics
    prec = (inter_metrics['prec'] + entity_metrics['prec']) / 2
    rec = (inter_metrics['rec'] + entity_metrics['rec']) / 2
    f = (inter_metrics['f'] + entity_metrics['f']) / 2
    metrics = {'prec': prec, 'rec': rec, 'f': f}
    return metrics


def get_ens(sets):
    """
    Puts all entities appeared in interpretation sets in one set.

    :param sets: [{en1, en2, ...}, {en3, ..}, ...]
    :return: set {en1, en2, en3, ...}
    """
    ens = set()
    for en_set in sets:
        for en in en_set:
            ens.add(en)
    return ens


def main(args):
    if len(args) < 2:
        print "\tUsage: [qrel_file] [result_file]"
        exit(0)
    qrels = parse_file(args[0])
    results = parse_file(args[1])

    evaluator = Evaluator(qrels, results)
    evaluator.eval(lean_eval_query)

if __name__ == '__main__':
    main(sys.argv[1:])
