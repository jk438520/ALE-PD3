def weighted_sum_of_lists(lst: [float, [bool]]):
    summed_lst = [0] * len(lst[0][1])
    for prob, strat in lst:
        for i, num_batt in enumerate(strat):
            summed_lst[i] += num_batt * prob
    return summed_lst


def generete_perfect_asserts(num_batt: int,
                             att_res: int,
                             def_res: int,
                             prof: [(float, [bool])]):
    assert 0 < att_res
    assert att_res < def_res
    assert def_res < num_batt
    assert sum(prob for prob, _ in prof) == 1


def generate_perfect_defender(num_batt: int,
                              att_res: int,
                              def_res: int,
                              att_prof: [(float, [bool])]):
    generete_perfect_asserts(num_batt, att_res, def_res, att_prof)

    summed_att_prof = weighted_sum_of_lists(att_prof)

    indexed_summed_att_prof = [(batt, i) for i, batt in enumerate(summed_att_prof)]

    indexed_summed_att_prof.sort(reverse=True)

    def_prof = [False] * num_batt
    for _, i in indexed_summed_att_prof[:def_res]:
        def_prof[i] = True

    return def_prof


def generate_perfect_attacker(num_batt: int,
                              att_res: int,
                              def_res: int,
                              def_prof: [bool]):
    generete_perfect_asserts(num_batt, att_res, def_res, def_prof)

    summed_att_prof = weighted_sum_of_lists(def_prof)

    indexed_summed_att_prof = [(batt, i) for i, batt in enumerate(summed_att_prof)]

    indexed_summed_att_prof.sort()

    att_prof = [False] * num_batt
    for _, i in indexed_summed_att_prof[:att_res]:
        att_prof[i] = True

    return att_prof


generate_perfect_attacker(3, 1, 2, [(1, [False, True, True])])
