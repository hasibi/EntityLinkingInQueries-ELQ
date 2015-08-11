"""
=============================================================================
Greedy Interpretation Finding (GIF) algorithm.

The algorithm takes candidate ranked entities for a query and find query interpretations in a greedy manner.

For detailed information see:
    F. Hasibi, K. Balog, and S. E. Bratsberg. "Entity Linking in Queries: Tasks and Evaluation",
    In Proceedings of ACM SIGIR International Conference on the Theory of Information Retrieval (ICTIR '15), Sep 2015.
    DOI: http://dx.doi.org/10.1145/2808194.2809473

=============================================================================
Usage:
    python GIF.py -in <tsv_file> -th <score_threshold>
e.g.
    python GIF.py -in ERD-dev_MLMcg.tsv -th 20
=============================================================================

Notes:
1. tsv_file is a tab-separated file containing qid, entity, mention, and score.
    tsv files for our baseline runs can be found under: runs/IF/entity_ranking_results/ERD-dev_MLMcg.tsv

2. The output of this code can be directly used by the evaluation scripts.

=============================================================================
@author: Faegheh Hasibi (faegheh.hasibi@idi.nunu.no)
=============================================================================
"""

from __future__ import division
import argparse
import csv


class GIF(object):
    """
    Attributes:
        score_th: score threshold
        query_annots: candidate entity ranking annotations for a query.
    """

    def __init__(self, score_th, query_annots):
        self.score_th = score_th
        self.query_annots = query_annots

    def process_query(self):
        """
        Processes the query annotations and generates the interpretation sets.

        :return: list of query interpretations [{men: en, ..}, ..]
        """
        self.prune()
        self.del_containment_mentions()
        interpretations = self.form_interpretations()
        return interpretations

    def prune(self):
        """Prunes annotations based on a ranking score threshold."""
        valid_annots = {}
        for men_en, score in self.query_annots.iteritems():
            if score >= self.score_th:
                valid_annots[men_en] = score
        self.query_annots = valid_annots
        return valid_annots

    def del_containment_mentions(self):
        """Deletes containment mentions, if they have lower score."""
        valid_annots = dict()
        valid_mens = set()
        for (men, en), score in sorted(self.query_annots.items(), key=lambda item: item[1], reverse=True):
            containment = False
            for valid_men in valid_mens:    
                if (men in valid_men) or (valid_men in men):
                    containment = True
            if not containment:
                valid_annots[(men, en)] = score
                valid_mens.add(men)
        self.query_annots = valid_annots
        return valid_annots

    def form_interpretations(self):
        """
        Forms query interpretations from the given annotations.

        :return list of query interpretations [{men1: en1, ..}, ..]
        """
        q_interprets = [{}]
        for men, en in self.query_annots.keys():
            added = False
            for interpret in q_interprets:
                mentions = interpret.keys()
                mentions.append(men)
                if not self.__is_overlapping(mentions):
                    interpret[men] = en
                    added = True
            if not added:
                q_interprets.append({men: en})
        return q_interprets

    @staticmethod
    def __is_overlapping(mentions):
        """
        Checks if the mentions of a set overlapping or not.
        E.g. {"the", "music man"} is not overlapping
             {"the", "the man", "music"} is overlapping.

        :param mentions: list of mentions
        :return True/False
        """
        words = []
        for men in mentions:
            words += set(men.split())
        if len(words) == len(set(words)):
            return False
        else:
            return True


def to_evaluation_format(interprets):
    """
    Converts interpretations to the proper format for evaluation scripts.

    :param interprets: interpretations of all queries {qid: [{men:en, ..}, ..], ..}
    :return: string, each line is in the format of "qid confidence_score   en1 en2 ... "
    """
    out_str = ""
    for qid, q_interprets in sorted(interprets.items(), key=lambda item: item[0]):
        unique_interprets = set()
        for interpret in q_interprets:
            if len(interpret) == 0:
                continue
            unique_interprets.add(tuple(sorted(set(interpret.values()))))

        for interpret in unique_interprets:
            # For the sake of code readability, we set the confidence score to 1,
            # but it can be set to the average score of entities (in the interpretation set).
            conf_score = "1"
            out_str += qid + "\t" + conf_score + "\t" + "\t".join(interpret) + "\n"
    return out_str


def read_tsv(tsv_file):
    """
    Reads a tsv file and extracts annotations.

    :param tsv_file: a tsv file containing columns for "qid", "freebase_id", "mention"
    :return: query annotations {qid: {(men, en): score, ..}, ..}
    """
    annots = {}
    with open(tsv_file, 'rb') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter="\t", quoting=csv.QUOTE_NONE)
        for line in reader:
            qid = line['qid']
            if qid not in annots:
                annots[qid] = {}
            annots[qid][(line['mention'], line['freebase_id'])] = float(line['score'])
    return annots


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--input", help=".tsv file, containing entity ranking results", type=str)
    parser.add_argument("-th", "--threshold", help="Score threshold for greedy approach", default=None, type=float)
    args = parser.parse_args()

    # Reads input file and finds query interpretations.
    annots = read_tsv(args.input)
    interprets = {}
    for qid, query_annots in annots.iteritems():
        interprets[qid] = GIF(args.threshold, query_annots).process_query()

    # Converts query interpretations to the proper format for evaluation scripts.
    eval_str = to_evaluation_format(interprets)
    output_file = args.input[:args.input.rfind(".")] + "-GIF-th" + str(args.threshold) + ".txt"
    open(output_file, "w").write(eval_str)
    print "Output file:", output_file


if __name__ == "__main__":
    main()