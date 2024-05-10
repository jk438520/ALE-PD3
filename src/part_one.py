import timeit


def weighted_sum_of_lists(lst: [float, [bool]]):
    summed_lst = [0] * len(lst[0][1])
    for prob, strat in lst:
        for i, batt in enumerate(strat):
            summed_lst[i] += prob * batt
    return summed_lst


def asserts(num_batt: int,
            att_res: int,
            def_res: int,
            prof: [(float, [bool])],
            batt_val: [int]):
    assert 0 < att_res
    assert att_res < def_res
    assert def_res < num_batt

    eps = 1e-6

    assert abs(sum(prob for prob, _ in prof) - 1) <= eps
    assert len(batt_val) == num_batt


def generate_perfect_defender(num_batt: int,
                              att_res: int,
                              def_res: int,
                              att_prof: [(float, [bool])],
                              batt_val: [int]):
    asserts(num_batt, att_res, def_res, att_prof, batt_val)

    summed_att_prof = weighted_sum_of_lists(att_prof)

    expected_loss = [bv * p for bv, p in zip(batt_val, summed_att_prof)]

    indexed_summed_att_prof = [(batt_prob, i) for i, batt_prob in enumerate(expected_loss)]

    indexed_summed_att_prof.sort(reverse=True)

    def_prof = [False] * num_batt
    for _, i in indexed_summed_att_prof[:def_res]:
        def_prof[i] = True

    return def_prof


def generate_perfect_attacker(num_batt: int,
                              att_res: int,
                              def_res: int,
                              def_prof: [(float, [bool])],
                              batt_val: [int]):
    asserts(num_batt, att_res, def_res, def_prof, batt_val)

    summed_def_prof = weighted_sum_of_lists(def_prof)

    prob_of_score = [1 - p for p in summed_def_prof]

    expected_score = [bv * p for bv, p in zip(batt_val, prob_of_score)]

    indexed_expected_score = [(score, i) for i, score in enumerate(expected_score)]

    indexed_expected_score.sort(reverse=True)

    att_prof = [False] * num_batt

    for _, i in indexed_expected_score[:att_res]:
        att_prof[i] = True

    return att_prof


def calculate_score(att_prof: [(float, [bool])],
                    def_prof: [(float, [bool])],
                    batt_val: [int]):
    for _, att_strat in att_prof:
        assert len(att_strat) == len(batt_val)
    for _, def_strat in def_prof:
        assert len(def_strat) == len(batt_val)
    att_score = 0
    def_score = 0

    summed_att_prof = weighted_sum_of_lists(att_prof)
    summed_def_prof = weighted_sum_of_lists(def_prof)

    for att_prob, def_prob, bv in zip(summed_att_prof, summed_def_prof, batt_val):
        expected_score  = att_prob * (1 - def_prob) * bv
        att_score += expected_score
        def_score -= expected_score

    return att_score, def_score




span_a = 0
span_b = 0
span_c = 0
span_d = 0
span_e = 0


def epsilons(num_batt: int,
             att_res: int,
             def_res: int,
             att_prof: [(float, [bool])],
             def_prof: [(float, [bool])],
             batt_val: [int]):
    global span_a
    global span_b
    global span_c
    global span_d
    global span_e

    asserts(num_batt, att_res, def_res, att_prof, batt_val)
    asserts(num_batt, att_res, def_res, def_prof, batt_val)
    for _, att_strat in att_prof:
        assert len(att_strat) == num_batt
        assert sum(att_strat) == att_res
    for _, def_strat in def_prof:
        assert len(def_strat) == num_batt
        assert sum(def_strat) == def_res

    tm1 = timeit.default_timer()
    att_score, def_score = calculate_score(att_prof, def_prof, batt_val)
    tm2 = timeit.default_timer()
    att_counter = [(1, generate_perfect_attacker(num_batt, att_res, def_res, def_prof, batt_val))]
    tm3 = timeit.default_timer()
    att_counter_score, _ = calculate_score(att_counter, def_prof, batt_val)
    tm4 = timeit.default_timer()
    def_counter = [(1, generate_perfect_defender(num_batt, att_res, def_res, att_prof, batt_val))]
    tm5 = timeit.default_timer()
    _, def_counter_score = calculate_score(att_prof, def_counter, batt_val)
    tm6 = timeit.default_timer()

    span_a += tm2 - tm1
    span_b += tm3 - tm2
    span_c += tm4 - tm3
    span_d += tm5 - tm4
    span_e += tm6 - tm5

    return att_counter_score - att_score, def_counter_score - def_score


def get_times():
    global span_a
    global span_b
    global span_c
    global span_d
    global span_e
    return span_a, span_b, span_c, span_d, span_e

def epsilon_for_attacker(num_batt: int,
                         att_res: int,
                         def_res: int,
                         att_prof: [(float, [bool])],
                         def_prof: [(float, [bool])],
                         batt_val: [int]):
    return epsilons(num_batt, att_res, def_res, att_prof, def_prof, batt_val)[0]


def stratToInt(strat: [bool]):
    return sum(2 ** i for i, b in enumerate(strat) if b)


def intToStrat(num_batt: int, strat: int):
    ret = []
    for i in range(num_batt):
        ret.append(strat % 2 == 1)
        strat = strat // 2
    return ret


def epsilon_for_defender(num_batt: int,
                         att_res: int,
                         def_res: int,
                         att_prof: [(float, [bool])],
                         def_prof: [(float, [bool])],
                         batt_val: [int]):
    return epsilons(num_batt, att_res, def_res, att_prof, def_prof, batt_val)[1]


if __name__ == '__main__':
    # print(generate_perfect_attacker(3, 1, 2, [(1, [False, True, True])], [1, 1, 1]))
    # print(epsilon_for_attacker(3, 1, 2, [(0.5, [False, True, False]), (0.5, [True, False, False])], [1, 1, 1]))
    #
    # print(generate_perfect_attacker(4, 1, 2, [(1, [False, False, True, True])], [2, 1, 1, 1]))
    # print(generate_perfect_attacker(4, 1, 2, [(1, [False, False, True, True])], [2, 1, 6, 6]))
    def_prof = [(1, [0, 1, 1])]
    generate_perfect_attacker(3, 1, 2, def_prof, [1, 2, 3])
