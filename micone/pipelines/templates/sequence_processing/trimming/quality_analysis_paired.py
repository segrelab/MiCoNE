#!/usr/bin/env python3

import csv
from functools import partial
from warnings import warn

from networkx.algorithms.traversal.edgebfs import REVERSE


def get_score(baseid: int, stat_dict: dict) -> str:
    """
    Calculate whether a given base id is 'good', 'warning' or 'failure'
    A warning will be issued if the lower quartile for any base is less than 10,
    or if the median for any base is less than 25.
    A failure will be issued if the lower quartile for any base is less than 5,
    or if the median for any base is less than 20.

    Parameters
    ---------
    baseid : int
        Base position currently under consideration for scoring
    stat_dict : Dict[str, List[float]]
        A dictionary containing scores for each of the seven statistics

    Returns
    ------
    str
        A string that is either 'good', 'warning' or 'failure'
        good = lambda s25: s25 > 28
    """
    warning = lambda s25, s50: (s25 < 10) or (s50 < 25)
    failure = lambda s25, s50: (s25 < 5) or (s50 < 20)
    stat25, stat50 = stat_dict["25%"][baseid], stat_dict["50%"][baseid]
    if failure(stat25, stat50):
        score = "failure"
    elif warning(stat25, stat50):
        score = "warning"
    else:
        score = "good"
    return score


def trimmer(
    scores: list,
    counts: list,
    direction: int = 0,
    threshold: int = 3,
    frac_retain: float = 0.9,
) -> int:
    """
    Trimmer takes scores and direction as input and returns the position where
    the sequence has to be trimmed in that direction

    Parameters
    ---------
    scores : list
        List of scores for each baseid. Scores are 'good', 'warning' or 'failure'
    counts : list
        Number of sequences used to calculate scores for each baseid
    direction : {0, 1}, optional
        The direction for trimming. 0 is left, 1 is right
        Default value is 0
    threshold : int, optional
        The minimum number of good bases that need to appear in sequence to stop trimming
        Default value is 5
    frac_retain : float, optional
        The minimum fraction of sequences that need to be retained after trimming

    Returns
    ------
    int
        The position where the sequence is to be trimmed in the given direction
    """
    ord_scores = scores if direction == 0 else scores[::-1]
    nseqs = counts[0]
    count_fracs = [c / nseqs for c in counts]
    try:
        retain_fail_pos = next(
            ind for ind, c in enumerate(count_fracs) if c < frac_retain
        )
    except StopIteration:
        retain_fail_pos = len(scores)
    stop_flag = 0
    pos = len(scores)
    for i, score in enumerate(ord_scores):
        if stop_flag <= -threshold:
            stop_flag = 0
        if stop_flag >= threshold:
            pos = i - threshold
            break
        elif score == "good":
            stop_flag += 1
        elif score == "warning":
            stop_flag += 0
        elif score == "failure":
            stop_flag -= 1
    direct_pos = pos if direction == 0 else len(scores) - pos
    return direct_pos if direction == 0 else min(direct_pos, retain_fail_pos)


def analyze_quality(quality_file: str) -> list:
    """
    Takes in quality_file location as input and gives out the scores for each positon

    Parameters
    ---------
    quality_file : str
        The location of the quality file

    Returns
    ------
    list
        List that contains the scores 'good', 'warning', 'failure' for each position
    """
    with open(quality_file, "r") as fid:
        header, count, *stats = csv.reader(fid, delimiter="\\t")
    stat_dict = dict((stat[0], list(map(float, stat[1:]))) for stat in stats)
    if len(set(count[1:])) > 1:
        warn("Sequences are of different lengths")
    base_ids = list(map(int, header[1:]))
    scorer_fun = partial(get_score, stat_dict=stat_dict)
    scores = list(map(scorer_fun, base_ids))
    counts = list(map(float, count[1:]))
    return scores, counts


def quality_analysis(forward_quality: str, fname: str) -> None:
    """
    A program to identify the how many bases needs to be trimmed off from the
    start and end of our sequences

    Parameters
    ----------
    forward_quality : str
        The file containing the seven number quality information for each base of forward read
        (2%, 9%, 25%, 50%, 75%, 91%, 98%)
    """
    with open(fname, "w") as fid:
        scores, counts = analyze_quality(forward_quality)
        left_trim = trimmer(scores, counts)
        length_trim = trimmer(scores, counts, direction=1)
        fid.write("trimLeft,{}\\n".format(left_trim))
        fid.write("truncLen,{}\\n".format(length_trim))


if __name__ == "__main__":
    FORWARD = "${forward_summary}"
    REVERSE = "${reverse_summary}"
    quality_analysis(FORWARD, "forward_trim.txt")
    quality_analysis(REVERSE, "reverse_trim.txt")
