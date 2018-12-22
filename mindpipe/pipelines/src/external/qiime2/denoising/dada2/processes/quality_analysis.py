#!/usr/bin/env python3

import csv
from functools import partial
from warnings import warn


def get_score(baseid: int, stat_dict: dict) -> str:
    # Calculate whether a given base id is 'good', 'warning' or 'failure'
    # A warning will be issued if the lower quartile for any base is less than 10,
    # or if the median for any base is less than 25.
    # A failure will be issued if the lower quartile for any base is less than 5,
    # or if the median for any base is less than 20.

    # Parameters
    # ---------
    # baseid : int
    #     Base position currently under consideration for scoring
    # stat_dict : Dict[str, List[float]]
    #     A dictionary containing scores for each of the seven statistics

    # Returns
    # ------
    # str
    #     A string that is either 'good', 'warning' or 'failure'
    # good = lambda s25: s25 > 28
    warning = lambda s25, s50: (s25 < 10) or (s50 < 25)
    failure = lambda s25, s50: (s25 < 5) or (s50 < 20)
    stat25, stat50 = stat_dict["25%"][baseid], stat_dict["50%"][baseid]
    score = "good"
    if failure(stat25, stat50):
        score = "failure"
    elif warning(stat25, stat50):
        score = "warning"
    return score


def trimmer(scores: list, direction: int = 0, threshold: int = 3) -> int:
    # Trimmer takes scores and direction as input and returns the position where
    # the sequence has to be trimmed in that direction

    # Parameters
    # ---------
    # scores : list
    #     List of scores for each baseid. Scores are 'good', 'warning' or 'failure'
    # direction : {0, 1}, optional
    #     The direction for trimming. 0 is left, 1 is right
    # threshold : int, optional
    #     The minimum number of good bases that need to appear in sequence to stop trimming

    # Returns
    # ------
    # int
    #     The position where the sequence is to be trimmed in the given direction
    ord_scores = scores if not direction else scores[::-1]
    fail_flag = 0
    for i, score in enumerate(ord_scores):
        if fail_flag >= threshold:
            pos = i - threshold
            break
        elif score == "good":
            fail_flag += 1
        elif score == "warning":
            fail_flag -= 1
        elif score == "failure":
            fail_flag = 0
    direct_pos = pos if not direction else len(scores) - pos
    return direct_pos


def analyze_quality(quality_file: str) -> list:
    # Takes in quality_file location as input and gives out the scores for each positon

    # Parameters
    # ---------
    # quality_file : str
    #     The location of the quality file

    # Returns
    # ------
    # list
    #     List of floats that contatins the scores 'good', 'warning', 'failure'
    #     for each position
    with open(quality_file, "r") as fid:
        header, count, *stats = csv.reader(fid, delimiter=",")
    stat_dict = dict((stat[0], list(map(float, stat[1:]))) for stat in stats)
    if len(set(count[1:])) > 1:
        warn("The counts at each base pair do not match")
    base_ids = list(map(int, header[1:]))
    scorer_fun = partial(get_score, stat_dict=stat_dict)
    scores = list(map(scorer_fun, base_ids))
    return scores


def quality_analysis(forward_quality: str, reverse_quality: str) -> None:
    # A program to identify the how many bases needs to be trimmed off from the
    # start and end of our sequences

    # forward_quality : str
    #     The file containing the seven number quality information for each base
    #     (2%, 9%, 25%, 50%, 75%, 91%, 98%)
    with open("trim.txt", "w") as fid:
        if forward_quality and reverse_quality:
            forward_scores = analyze_quality(forward_quality)
            reverse_scores = analyze_quality(reverse_quality)
            fid.write("--p-trim-left-f {ans} ".format(ans=trimmer(forward_scores)))
            fid.write(
                "--p-trunc-len-f {ans} ".format(
                    ans=trimmer(forward_scores, direction=1)
                )
            )
            fid.write("--p-trim-left-r {ans} ".format(ans=trimmer(reverse_scores)))
            fid.write(
                "--p-trunc-len-r {ans} ".format(
                    ans=trimmer(reverse_scores, direction=1)
                )
            )
        else:
            scores = analyze_quality(forward_quality)
            fid.write("--p-trim-left {ans} ".format(ans=trimmer(scores)))
            fid.write("--p-trunc-len {ans} ".format(ans=trimmer(scores, direction=1)))


if __name__ == "__main__":
    FORWARD = "${forward}"
    REVERSE = "${reverse}"
    quality_analysis(FORWARD, REVERSE)
