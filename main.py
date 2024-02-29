import requests

cipher_text = "NHKHY;''DKGAC!ZW'MH!.TWSZXTCGAOM,RDSE.HPYU';!HY;X'JB'XXNGNNBLQXNJ!HYUEXE.BER;GNIYTG.'GH.TG.'JNGFHDSDNYF.Q;BYYE.UA;FNTTDSE.GYC'GQHI!RMNHKHY;.JGYY;UVGNNWBO.GKESF.Q;BYYE.BZOUZBOBHNZ?ERX';E!EA;JH!Q!UBZK!TTTS';EHE.;JB?!L;HXOGHXXWGNZHE.;JBOY!VB'QNYUR;GNIYTHVV?NUFTYTN!!DRN'HLYE.UA;FNTTDSDNYLDUVHPHY;DSKIX!O,MOIQO;BZSLTTBMGNNB,URMO'HE.;JBOEYU'FNZBU,BZHZXTUVNH!UBAXGE?M;BCGNHISUUR,O!O;YAMEMD,XG!RB'KCVMOHLQXNJCG!OVYK!RM"

english_frequencies = {'U': 0.037, 'B': 0.016, 'D': 0.034, 'M': 0.022, 'T': 0.079, 'K': 0.012, 'I': 0.061, 'R': 0.054,
                       'O': 0.076, 'L': 0.044, 'V': 0.009, 'H': 0.06, '.': 0.022, "'": 0.01, '?': 0.005,
                       'Y': 0.025, '!': 0.015, 'C': 0.022, 'N': 0.06, 'E': 0.106, 'S': 0.053,
                       ',': 0.021, 'F': 0.014, 'Q': 0.002, 'P': 0.013, 'J': 0.001,
                       'A': 0.075, 'G': 0.027, 'Z': 0.0, ';': 0.0,
                       'W': 0.023, 'X': 0.001}

symbols = "!',.;?ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def char_count(text):
    char_cnt = {}
    for char in text:
        if char in char_cnt:
            char_cnt[char] += 1
        else:
            char_cnt[char] = 1
    return char_cnt

def index_of_coincidence(text):
    n = len(text)
    char_cnt = char_count(text)
    index = 0
    for count in char_cnt.values():
        index += count * (count - 1)

    index = index / (n * (n - 1))
    return index

def decrypt_vigenere_xor(cipher_text, key):
    decrypted_text = ''
    key_length = len(key)
    for i, char in enumerate(cipher_text):
        char_index = symbols.index(char)
        key_index = symbols.index(key[i % key_length])
        decrypted_char_index = (char_index ^ key_index) % 32
        decrypted_char = symbols[decrypted_char_index]
        decrypted_text += decrypted_char
    return decrypted_text

def guess_key_length(cipher_text):
    for key_length in range(1, 30):
        substrings = [''] * key_length
        for i, char in enumerate(cipher_text):
            substrings[i % key_length] += char

        ic_avg = 0
        for substring in substrings:
            ic_avg += index_of_coincidence(substring)
        ic_avg /= key_length
        print(f"Key Length: {key_length}, Index of Coincidence: {ic_avg}")


def decrypt_with_key_length(cipher_text, key_length):
    key = ""
    for i in range(key_length):
        sub_text = cipher_text[i::key_length]
        best_correlation = 0
        best_key_char = None

        for candidate_key_char in english_frequencies.keys():
            decrypted_text = decrypt_vigenere_xor(sub_text, candidate_key_char)
            valid_chars = [char for char in decrypted_text if char in english_frequencies]

            freqs = {}
            for char in set(valid_chars):
                freqs[char] = valid_chars.count(char) / len(valid_chars)

            correlation = sum(freq * english_frequencies[char] for char, freq in freqs.items())

            if correlation > best_correlation:
                best_correlation = correlation
                best_key_char = candidate_key_char
        key += best_key_char
    return key


def decrypt_with_key(cipher_text, key):
    result = ''
    for i in range(len(cipher_text)):
        result += symbols[symbols.index(cipher_text[i]) ^ symbols.index(key[i % len(key)])]
    return result

def decrypt_text(cipher_text):
    guess_key_length(cipher_text)
    assumed_key_length = 7 # from function guess_key_length(cipher_text) we can see that our key_length will be 7
    key = decrypt_with_key_length(cipher_text, assumed_key_length)
    decrypted_text = decrypt_with_key(cipher_text, key)
    return decrypted_text, key

decrypted_text, key = decrypt_text(cipher_text)
print(decrypted_text)

