import re
import os
import sys
from yelp_uri.encoding import recode_uri
from urllib.request import urlopen
from bs4 import BeautifulSoup

oropuare = "aāeēiīoōuū"
orokati = "hkmnprtwŋƒ"
kūare_tohutō = ''.maketrans({'ā': 'a', 'ē': 'e', 'ī': 'i', 'ō': 'o', 'ū': 'u'})
arapū = "AaĀāEeĒēIiĪīOoŌōUuŪūHhKkMmNnPpRrTtWwŊŋƑƒ-"


def nahanaha(tūtira):
    # Takes a list of strings (e.g. output of kōmiri_kupu) and returns the
    # list in Māori alphabetical order
    return sorted(tūtira, key=lambda kupu: [arapū.index(pūriki) if pūriki in arapū else len(arapū) + 1 for pūriki in
                                            hōputu(kupu)])


def hōputu(kupu):
    # Replaces ng and wh, w', w’ with ŋ and ƒ respectively, since Māori
    # consonants are easier to deal with in unicode format. It may be passed
    # A list, dictionary, or string, and uses if statements to determine how
    # To replace the consonants of the constituent words, and wheter to return
    # A string or a list. The Boolean variable determines whether it's encoding
    # Or decoding (set False if decoding)

    return re.sub(r'(w\')|(w’)|(wh)|(ng)|(W\')|(W’)|(Wh)|(Ng)|(WH)|(NG)', whakatakitahi, kupu)


def whakatakitahi(tauriterite):
    # If passed the appropriate letters, return the corresponding symbol
    oro = tauriterite.group(0)
    if oro == 'ng':
        return 'ŋ'
    elif oro == 'w\'' or oro == 'w’' or oro == 'wh':
        return 'ƒ'
    elif oro == 'Ng' or oro == 'NG':
        return 'Ŋ'
    else:
        return 'Ƒ'


# Keys to the kupu_list dictionary:
keys = ['pākehā', 'rangirua', 'pākehā_kūare_tohutō', 'rangirua_kūare_tohutō']
kupu_lists = {}


def kōmiri_kupu(kupu_tōkau, tohutō=True):
    # Removes words that contain any English characters from the string above,
    # returns dictionaries of word counts for three categories of Māori words:
    # Māori, ambiguous, non-Māori (Pākehā)
    # Set tohutō = True to become sensitive to the presence of macrons when making the match

    # Splits the raw text along characters that a
    kupu_hou = re.findall('(?!-)(?!{p}*--{p}*)({p}+)(?<!-)'.format(p='[a-zāēīōū\-’\']'), kupu_tōkau,
                          flags=re.IGNORECASE)

    # Gets the preferred word lists from the preloaded files, depending on
    # The Boolean variable, as macronised and demacronised texts have different
    # Stoplists (files that need to be accessed)
    kupu_rangirua = kupu_lists[keys[1]] if tohutō else kupu_lists[keys[3]]
    kupu_pākehā = kupu_lists[keys[0]] if tohutō else kupu_lists[keys[2]]

    # Setting up the dictionaries in which the words in the text will be placed
    raupapa_māori, raupapa_rangirua, raupapa_pākehā = {}, {}, {}

    # Puts each word through tests to determine which word frequency dictionary
    # it should be referred to. Goes to the ambiguous dictionary if it's in the
    # ambiguous list, goes to the Māori dictionary if it doesn't have consecutive
    # consonants, doesn't end in a consnant, doesn't have any english letters
    # and isn't one of the provided stop words. Otherwise it goes to the non-Māori
    # dictionary. If this word hasn't been added to the dictionary, it does so,
    # and adds a count for every time the corresponding word gets passed to the
    # dictionary.

    for kupu in kupu_hou:
        hōputu_kupu = hōputu(kupu)
        if ((kupu.lower() or kupu.lower().translate(kūare_tohutō)) in kupu_rangirua) or len(kupu) == 1:
            if kupu not in raupapa_rangirua:
                raupapa_rangirua[kupu] = 0
            raupapa_rangirua[kupu] += 1
            continue
        elif not (re.compile("[{o}][{o}]".format(o=orokati)).search(hōputu_kupu.lower()) or (
                hōputu_kupu[-1].lower() in orokati) or any(pūriki not in arapū for pūriki in hōputu_kupu.lower()) or (
                          (kupu.lower() or whakatakitahi_oropuare(kupu)) in kupu_pākehā)):
            if kupu not in raupapa_māori:
                raupapa_māori[kupu] = 0
            raupapa_māori[kupu] += 1
            continue
        else:
            if kupu not in raupapa_pākehā:
                raupapa_pākehā[kupu] = 0
            raupapa_pākehā[kupu] += 1

    return raupapa_māori, raupapa_rangirua, raupapa_pākehā


def whakatakitahi_oropuare(kupu):
    # Replaces doubled vowels with a single vowel. It is passed a string, and returns a string.
    return re.sub(r'uu', 'u', re.sub(r'oo', 'o', re.sub(r'ii', 'i', re.sub(r'ee', 'e', re.sub(r'aa', 'a', kupu)))))


def hihira_raupapa_kupu(kupu_hou, tohutō):
    # Looks up a single word to see if it is defined in maoridictionary.co.nz
    # Set tohutō = False to not ignore macrons when making the match
    # Returns True or False

    kupu_huarua = kupu_hou.lower()
    # If the macrons are not strict, they are removed for the best possibility of finding a match
    if tohutō:
        kupu_huarua = kupu_huarua.translate(no_tohutō)
    # Sets up an iterable of the word, and the word without double vowels to be searched.
    # This is because some texts use double vowels instead of macrons, and they return different search results.
    taurua = [kupu_huarua, whakatakitahi_oropuare(kupu_huarua)]
    # Sets up the variable to be returned, it is changed if a result is found
    wāriutanga = False

    for kupu in taurua:
        taukaea = recode_uri(
            'http://maoridictionary.co.nz/search?idiom=&phrase=&proverb=&loan=&histLoanWords=&keywords=' + kupu)
        hupa = BeautifulSoup(urlopen(taukaea), 'html.parser', from_encoding='utf8')

        tohu = hupa.find_all('h2')

        # The last two entries are not search results, due to the format of the website.
        for taitara in tohu[:-2]:
            taitara = taitara.text.lower()
            # Removes capitals and macrons for the best chance of making a match
            if kupu in (taitara.translate(no_tohutō).split() if tohutō else taitara.split()):
                wāriutanga = True
                break
            else:
                pass

    print("Found " + kupu + ": " + str(wāriutanga))
    return wāriutanga


def hihira_raupapa(kupu_hou, tohutō=False):
    # Looks up a list of words to see if they are defined in maoridictionary.co.nz
    # Set tohutō = False to become sensitive to the presence of macrons when making the match
    # Returns a list of words that are defined, and a list of words that are not defined from the input list.

    # Associates each word with a dictionary check result
    hihira = [hihira_raupapa_kupu(kupu, tohutō) for kupu in kupu_hou]

    # Adds it to the good word list if it passed the check
    kupu_pai = [tokorua[1] for tokorua in zip(hihira, kupu_hou) if tokorua[0]]
    # Adds it to the bad word list if it failed the check
    kupu_kino = [tokorua[1] for tokorua in zip(hihira, kupu_hou) if not tokorua[0]]
    return kupu_pai, kupu_kino


def kupu_ratios(text, tohutō=True):
    map_Māori, map_ambiguous, map_other = kōmiri_kupu(text, tohutō)

    nums = {'reo': sum(map_Māori.values()),
            'ambiguous': sum(map_ambiguous.values()),
            'other': sum(map_other.values()) + len(re.findall('[\d]+([,.][\d]+)*', text))}

    nums['percent'] = get_percentage(**nums)
    save_corpus = nums['percent'] >= 50

    return save_corpus, nums


def get_percentage(reo, ambiguous, other):
    if reo:
        return round(100 * reo / (reo + other), 2)
    elif other:
        return 0
    elif ambiguous:
        return 51
    else:
        return 0


def auaha_raupapa_tū(kupu_tōkau, tohutō=True):
    # This function is used for making stoplists as it does not depend on any stoplists.
    # It finds all words in a string, and adds them to a dictionary depending on
    # Whether they look like Māori words or not, and counts their frequency.
    # Set tohutō = True to become sensitive to the presence of macrons when making the match

    # Splits the raw text along characters that a
    kupu_hou = re.findall('(?!-)(?!{p}*--{p}*)({p}+)(?<!-)'.format(p='[a-zāēīōū\-’\']'), kupu_tōkau,
                          flags=re.IGNORECASE)

    # Setting up the dictionaries in which the words in the text will be placed
    raupapa_māori, raupapa_pākehā = {}, {}

    # Puts each word through tests to determine which word frequency dictionary
    # it should be referred to. Goes to the Māori dictionary if it doesn't have
    # consecutive consonants, doesn't end in a consnant, or doesn't have any
    # English letters. Otherwise it goes to the non-Māori dictionary. If this
    # word hasn't been added to the dictionary, it does so, and adds a count for
    # every time the corresponding word gets passed to the dictionary.

    for kupu in kupu_hou:
        hōputu_kupu = hōputu(kupu)
        if not (re.compile("[{o}][{o}]".format(o=orokati)).search(hōputu_kupu.lower()) or (
                hōputu_kupu[-1].lower() in orokati) or any(pūriki not in arapū for pūriki in hōputu_kupu.lower())):
            if kupu not in raupapa_māori:
                raupapa_māori[kupu] = 0
            raupapa_māori[kupu] += 1
            continue
        else:
            if kupu not in raupapa_pākehā:
                raupapa_pākehā[kupu] = 0
            raupapa_pākehā[kupu] += 1

    return raupapa_māori, raupapa_pākehā


def tiki_ōrau(kōwae):
    # Uses the kōmiri_kupu function from the taumahi module to estimate how
    # Much of the text is Māori. Input is a string of text, output is a percentage string

    # Gets the word frequency dictionaries for the input text
    raupapa_māori, raupapa_rangirua, raupapa_pākehā = kōmiri_kupu(kōwae, False)

    # Calculates how many words of the Māori and English dictionary there are
    tatau_māori = sum(raupapa_māori.values())
    tatau_rangirua = sum(raupapa_rangirua.values())
    tatau_pākehā = sum(raupapa_pākehā.values())
    tatau_kapa = tatau_māori + tatau_pākehā
    tatau_tapeke = tatau_kapa + tatau_rangirua

    # Provided there are some words that are categorised as Māori or English,
    # It calculates how many Māori words there are compared to the sum, and
    # Returns the percentage as a string
    ōrau = 0.00 if (not tatau_kapa != 0) else round((tatau_māori / tatau_kapa) * 100, 2)

    return tatau_māori, tatau_rangirua, tatau_pākehā, tatau_tapeke, ōrau


try:
    root = __file__
    if os.path.islink(root):
        root = os.path.realpath(root)
    dirpath = os.path.dirname(os.path.abspath(root)) + '/taumahi_tūtira'

    # Reads the file lists of English and ambiguous words into list variables
    filenames = ["/kupu_kino.txt", "/kupu_rangirua.txt", "/kupu_kino_kūare_tohutō.txt",
                 "/kupu_rangirua_kūare_tohutō.txt"]
    for pair in zip(keys, filenames):
        with open(dirpath + pair[1], "r") as kōnae:
            kupu_lists[pair[0]] = kōnae.read().split()
except Exception as e:
    print(e)
    print("I'm sorry, but something is wrong.")
    print("There is no __file__ variable. Please contact the author.")
    sys.exit()

# All following script is for cleaning raw text strings:

apostrophes = '‘’\'"“”\s'
sentence_end = ['([.!?:—"“]+[\)\]]*|,\s*[\'"“”])', '[{}]+'.format(apostrophes)]

# Regex for splitting paragraphs, detecting a p end and beginning of another
new_paragraph = re.compile('({}+|-+){}\n'.format(sentence_end[0], sentence_end[1]))
# Version 2:
paragraph_pattern = re.compile('(?<=([.!?]|[\-—:]))[\-—.!? ‘’\'"•]*\n["\']*(?=[A-Z])')

# Regex to detect the end of a sentence
new_sentence = re.compile('{}{}|["“”]—?'.format(sentence_end[0], sentence_end[1]))


def get_paragraph(txt):
    paragraph_end = paragraph_pattern.search(txt)
    if paragraph_end:
        return txt[:paragraph_end.start()], txt[paragraph_end.end():]
    return txt, ''


def clean_whitespace(paragraph):
    return re.sub(r'\s+', ' ', paragraph).strip()


# Regex to replace all ~|[A macron] vowels with macron vowels
vowels = re.compile(r'(A?~|\[A macron\])([aeiouAEIOU])')
vowel_map = {'a': 'ā', 'e': 'ē', 'i': 'ī', 'o': 'ō', 'u': 'ū'}


def sub_vowels(txt):
    return vowels.sub(lambda x: vowel_map[x.group(2).lower()], txt)
