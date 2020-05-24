from random import randint

AMOUNT_OF_MIX = 300
START_CODON = 'atg'
stop_codons = ['taa', 'tag', 'tga']
translated_protein_map = {'ttt': 'phe', 'ttc': 'phe', 'tta': 'leu',
                          'ttg': 'leu', 'ctt': 'leu', 'ctc': 'leu',
                          'cta': 'leu', 'ctg': 'leu', 'att': 'ile',
                          'atc': 'ile', 'ata': 'ile', 'atg': 'met',
                          'gtt': 'val', 'gtc': 'val', 'gta': 'val',
                          'gtg': 'val', 'tct': 'ser', 'tcc': 'ser',
                          'tca': 'ser', 'tcg': 'ser', 'cct': 'pro',
                          'ccc': 'pro', 'cca': 'pro', 'ccg': 'pro',
                          'act': 'thr', 'acc': 'thr', 'aca': 'thr',
                          'acg': 'thr', 'gct': 'ala', 'gcc': 'ala',
                          'gca': 'ala', 'gcg': 'ala', 'tat': 'tyr',
                          'tac': 'tyr', 'cat': 'his', 'cac': 'his',
                          'caa': 'gln', 'cag': 'gln', 'aat': 'asn',
                          'aac': 'asn', 'aaa': 'lys', 'aag': 'lys',
                          'gat': 'asp', 'gac': 'asp', 'gaa': 'glu',
                          'gag': 'glu', 'tgt': 'cys', 'tgc': 'cys',
                          'tgg': 'trp', 'cgt': 'arg', 'cgc': 'arg',
                          'cga': 'arg', 'cgg': 'arg', 'agt': 'ser',
                          'agc': 'ser', 'aga': 'arg', 'agg': 'arg',
                          'ggt': 'gly', 'ggc': 'gly', 'gga': 'gly',
                          'ggg': 'gly', 'taa': 'STOP', 'tag': 'STOP',
                          'tga': 'STOP'
                          }


def search_max_orf(dna, is_straight):
    max_orf_1 = search_orf(dna, is_straight)
    max_orf_2 = search_orf(dna[1:], is_straight)
    max_orf_3 = search_orf(dna[2:], is_straight)
    max_orf = None
    if max_orf_1 is not None:
        max_orf = max_orf_1
    if max_orf_2 is not None:
        if max_orf is not None:
            if max_orf_2.end - max_orf_2.start > max_orf.end - max_orf.start:
                max_orf = max_orf_2
        else:
            max_orf = max_orf_2
    if max_orf_3 is not None:
        if max_orf is not None:
            if max_orf_3.end - max_orf_3.start > max_orf.end - max_orf.start:
                max_orf = max_orf_3
        else:
            max_orf = max_orf_3
    return max_orf


def search_orf(dna, is_straight):
    max_len = 0
    max_orf_start = -1
    max_orf_end = -1
    max_orf = ''
    orf_start = -1
    for i in range(0, len(dna), 3):
        if dna[i:i + 3] == START_CODON and orf_start == -1:
            orf_start = i
        if orf_start != -1 and stop_codons.__contains__(dna[i:i + 3]):
            if i - orf_start > max_len:
                max_len = i + 3 - orf_start
                max_orf_start = orf_start
                max_orf_end = i + 3
                max_orf = dna[orf_start:i + 3]
            orf_start = -1
    translated_orf = translate_orf(max_orf)
    if max_orf_start != -1 and max_orf_end != -1:
        return ORF(max_orf, translated_orf, max_orf_start, max_orf_end, is_straight)
    return None


def main():
    print('Please, enter DNA`s length')
    dna_length = int(input())
    check_dna_length(dna_length)
    print('Please, GC percent')
    gc_percent = int(input())
    check_gc(gc_percent)
    dna = generate_random_dna(dna_length, gc_percent)
    print('Generated DNA is {}'.format(dna))
    reversed_dna = dna[::-1]
    max_orf = search_max_orf(dna, True)
    max_reversed_orf = search_max_orf(reversed_dna, False)
    if max_orf is None:
        if max_reversed_orf is None:
            print("DNA doesn't have ORF")
            return
        else:
            max_orf = max_reversed_orf
    elif max_reversed_orf is not None and max_reversed_orf.end - max_reversed_orf.start > max_orf.end - max_orf.start:
        max_orf = max_reversed_orf

    if max_orf.end - max_orf.start < 30:
        print('The ORF`s length is so short')
    else:
        print('The max ORF is', end=' ')
        for i in range(0, len(max_orf.orf) - 3, 3):
            print(max_orf.orf[i:i+3], end=' ')
        print()
        print('Translated protein is {}'.format(max_orf.translated_orf))

        print('ORF range is [{},{}]'.format(max_orf.start + 1, max_orf.end + 1))
        if max_orf.is_straight:
            print('DNA direction is straight')
        else:
            print('DNA direction is reverse')


def check_dna_length(dna_length):
    if dna_length < 100 or dna_length > 1000:
        raise Exception('String length should be in the range from 100 to 1000')


def check_gc(gc_percent):
    if gc_percent < 20 or gc_percent > 80:
        raise Exception('GC structure should be in the range from 20 to 80')


def generate_random_dna(dna_length, gc_percent):
    g_sum = int(gc_percent * dna_length / 200)
    c_sum = g_sum
    a_sum = int((dna_length - g_sum * 2) / 2)
    t_sum = a_sum
    dna = ''
    dna = append_chars(dna, g_sum, 'g')
    dna = append_chars(dna, c_sum, 'c')
    dna = append_chars(dna, a_sum, 'a')
    dna = append_chars(dna, t_sum, 't')
    dna_list = list(dna)
    for i in range(AMOUNT_OF_MIX):
        first_char = randint(0, len(dna_list) - 1)
        second_char = randint(0, len(dna_list) - 1)
        temp = dna_list[first_char]
        dna_list[first_char] = dna_list[second_char]
        dna_list[second_char] = temp
    return ''.join(dna_list)


def append_chars(dna, quantity, chr):
    for i in range(quantity):
        dna = dna + chr
    return dna


def search_start_orf(dna):
    start = 0
    dna_start = -1
    while start <= len(dna) - 3:
        if dna[start:start+3] == START_CODON:
            dna_start = start
            break
        else:
            start += 3
    return dna_start


def search_end_orf(dna):
    dna_end = -1
    end = 0
    while end <= len(dna) - 3:
        if stop_codons.__contains__(dna[end:end+3]):
            dna_end = end
        end += 3
    return dna_end


def translate_orf(max_orf):
    translated_orf = ''
    for i in range(0, len(max_orf), 3):
        translated_orf += translated_protein_map.get(max_orf[i:i+3]) + ' '
    return translated_orf


class ORF:
    def __init__(self, orf, translated_orf, start, end, is_straight):
        self.orf = orf
        self.translated_orf = translated_orf
        self.start = start
        self.end = end
        self.is_straight = is_straight


main()