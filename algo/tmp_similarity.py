def normalise_dict(word_count):
    """Normalises a dict which stores words and their counts"""
    E_X = 0
    E_X_2 = 0
    n = 0
    for key in word_count:
        freq = word_count[key]
        E_X = E_X + freq
        E_X_2 = E_X_2 + (freq * freq)
        n = n + 1

    E_X = E_X / n
    E_X_2 = E_X_2 / n
    variance = E_X_2 - E_X
    sigma = (variance) ** (0.5)

    normalised_dict = {}
    for key in word_count:
        normalised_dict[key] = (word_count[key] - E_X) / sigma

    return normalised_dict

def appropriate_margin(word_count_dict,M):
    """Returns the maximum value of word_count_dict divided by M"""

    maximum = -100
    for key in word_count_dict:
        maximum = max(word_count_dict[key],maximum)

    return (maximum/M)

def correlation_coefficient(word_dict_1,word_dict_2,margin):
    """Computes the correlation coefficient between two dicts.
        margin is a paramater (0 <= margin <= 1) above which if there exists a word whose value is at least margin in at least one of the dicts, it will get its own separate dimension, else it will be counted in others/miscellaneous."""
    list_1 = []
    list_2 = []
    others_1 = 0
    others_2 = 0

    for key in word_dict_1:
        if (key in word_dict_2):
            if ( (word_dict_1[key] >= margin) or (word_dict_2[key] >= margin) ):
                list_1.append(word_dict_1[key])
                list_2.append(word_dict_2[key])
            else:
                others_1 = others_1 + word_dict_1[key]
                others_2 = others_2 + word_dict_2[key]
        else:
            if (word_dict_1[key] >= margin):
                list_1.append(word_dict_1[key])
                list_2.append(0)
            else:
                others_1 = others_1 + word_dict_1[key]


    for key in word_dict_2:
        if (key not in word_dict_1):
            if( word_dict_2[key] >= margin):
                list_1.append(0)
                list_2.append(word_dict_2[key])
            else:
                others_2 = others_2 + word_dict_2[key]


    list_1.append(others_1)
    list_2.append(others_2)

    vec_1 = numpy.array(list_1)
    vec_2 = numpy.array(list_2)

    C = numpy.cov(vec_1,vec_2)
    return C

