def wordSim(P, R):
    if len(R) > len(P):
        P, R = R, P
    common = {}
    count = 1
    for i in P:
        if i in R:
            common.setdefault(i, [])
            common[i].append(count)
            count += 1

    # print common, P
    count = 1
    for i in R:
        if i in common:
            common[i].append(count)
            count += 1
    # print common, P
    sumi = 0.0
    for i in common:
        sumi += abs(common[i][0] - common[i][1])
    # print sumi
    # Calculating Similiarity
    if len(common) == 0:
        return 0, []
    try:
        if len(common) % 2 == 0:
            return 1 - (2 * sumi / float(len(common) ** 2)), common
        elif len(common) % 2 != 0 and len(common) > 1:
            return 1 - (2 * sumi / (float(len(common) ** 2) - 1)), common
        elif len(common) % 2 != 0 and len(common) == 1:
            return 1, common
    except ZeroDivisionError:
        return 0, []
