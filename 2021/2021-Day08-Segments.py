from collections import Counter

test_input = """""".splitlines()

def strsort(x):
    return "".join(sorted(x))

def get_input(filename):
    signals = []
    with open(filename) as f:    
        for line in (x.strip() for x in f):
            parts = line.split(" | ")
            digits = [strsort(x) for x in parts[0].split(" ")]
            display = [strsort(x) for x in parts[1].split(" ")]
            signals.append({"digits": digits, "display": display})
    return signals

def decode_display(signal: dict):
    signal["display_decoded"] = [ signal["digits_decoded"][disp] for disp in signal["display"]]

def decode_easy_digits(signal: dict):
    signal["digits_decoded"] = {}
    digassign = [(2, '1'), (3, '7'), (4, '4'), (7, '8')]
    diglen = {len(d): d for d in signal["digits"]}

    for dlen, digit in digassign:
        signal["digits_decoded"][diglen[dlen]] = digit

def decode_hard_digits(signal: dict):
    # first, deduce how the segments correspond
    signal["digit_codes"] = {v: k for k, v in signal["digits_decoded"].items()}
    signal["segments_mapped"] = {}
    # deduce what "a" is
    seven = signal["digit_codes"]["7"]
    one = signal["digit_codes"]["1"]
    a = list(set(seven) - set(one))[0]
    signal["segments_mapped"]["a"] = a
    # deduce what "b", "e", and "f" are
    signal["segment_counts"] = Counter("".join(signal['digits']))
    segment_counts_reversed = {v: k for k, v in signal["segment_counts"].items()}
    signal["segments_mapped"]["b"] = segment_counts_reversed[6]
    signal["segments_mapped"]["e"] = segment_counts_reversed[4]
    signal["segments_mapped"]["f"] = segment_counts_reversed[9]
    # deduce what "c" is
    c = list(set(one) - set(signal["segments_mapped"]['f']))[0]
    signal["segments_mapped"]["c"] = c
    # deduce what "d" is
    four = signal["digit_codes"]["4"]
    d = list(set(four) - set(signal["segments_mapped"]['b']) - set(signal["segments_mapped"]['c']) - set(signal["segments_mapped"]['f']))[0]
    signal["segments_mapped"]["d"] = d
    # deduce what "g" is
    g = list(set("abcdefg") - set(signal["segments_mapped"].values()))[0]
    signal["segments_mapped"]["g"] = g
    signal["segments_mapped_reversed"] = {v: k for k, v in signal["segments_mapped"].items()}
    # now, deduce the rest of the digits
    sigdig = (('acdeg', '2'), ('acdfg', '3'), ('abdfg', '5'), 
        ('abdefg', '6'), ('abcdfg', '9'), ('abcefg', '0'))
    for d in signal['digits']:
        pre_sorted_d = "".join(sorted(list(d)))
        translated_d = "".join([signal['segments_mapped_reversed'][l] for l in list(d)])
        sorted_d = "".join(sorted(list(translated_d)))
        for seqdig, digit in sigdig:
            if sorted_d == seqdig:
                signal['digit_codes'][digit] = pre_sorted_d
    
    signal["digits_decoded"] = {v: k for k, v in signal["digit_codes"].items()}


def count_easy_digits(signals: list):
    cnt = 0
    for signal in signals:
        decode_easy_digits(signal)
        cnt += sum(1 for x in signal["display"] if x in signal["digits_decoded"].keys())
    return cnt



def sum_decoded_digits(signals: list):
    decoded_sum = 0
    for signal in signals:
        decode_easy_digits(signal)
        decode_hard_digits(signal)
        decode_display(signal)
        final_display = int("".join(signal["display_decoded"]))
        decoded_sum += final_display          
    return decoded_sum

test_signals = get_input("2021-Day08.txt")
print(count_easy_digits(test_signals))
print(sum_decoded_digits(test_signals))