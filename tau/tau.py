# -*- coding: utf-8 -*-
from taumahi import *
import re
import csv


def hōputu_kupu(tau):
    # Converts numerals into Māori words for numbers up to 100 billion.
    # The input is a string of numerals, periods and commas
    # The output is a string of Māori words

    # Dictionary for each numeral and its associated number, aside from 0 which is usually omitted except for when it is the only numeral
    tau_kupu = {'1': 'kotahi', '2': 'rua', '3': 'toru', '4': 'whā',
                '5': 'rima', '6': 'ono', '7': 'whitu', '8': 'waru',
                '9': 'iwa', '10': 'tekau', '100': 'rau'}

    # Sets up the string where the numerals' text will be stored
    reo = ""
    # Sets up the 10s carryover variable
    mā = False

    # Removes any commas or periods, with the intention of being left with a string of numbers
    kupu = re.sub(r',', '', re.sub(r'\.', '', tau))

    # If there are any other characters in the string apart from those mentioned in the function's beginning,
    if re.search(r'[^0-9]', kupu):
        # the function will break.
        return

    # Retrieves the length of the string, which is important in determining which 'place' (100s, 10s or 1s) each digit is in.
    hauroa = len(kupu)
    # Loops through each index in the numeral string
    for i in range(hauroa):
        # The numeral '0' is never written, and is treated very differently from other digits. The tests for the digit 0 are hence separated.
        if kupu[i] == '0':
            # If there was a non-zero digit in the previous position, which would be a 10s position if this test is activated,
            if mā:
                # then nothing needs to be written, as the current digit is 0. So it is reverted back to False.
                mā = False
            # If the last thing written was in the number dictionary (i.e. not an order of magnitude from kaha_kaituhituhi), and it is in the 1s position,
            if reo and reo.split()[-1] in tau_kupu.values() and (hauroa - i) % 3 == 1:
                # then an order of magnitude needs to be written
                reo += kaha_kaituhituhi(hauroa, i)
        # If the digit is non-zero,
        else:
            # This will be activated when the current digit is in the 1s position, after a non-zero 10s digit.
            if mā:
                # Since there is also a non-zero digit in the 1s position, it will write "mā", which is used to connect 10s and 1s.
                reo += "mā "
                # The variable is then reverted to False, so that it is only activated in the 1s position after it has been set to True.
                mā = False

            # If there is a 1 in the 10s position, nothing will be written
            if kupu[i] == '1' and (hauroa - i) % 3 == 2:
                pass
            # If there is a 1 in the last position, 'tahi' will be written. Otherwise, 1 is 'kotahi' as in the dictionary.
            elif kupu[i] == '1' and i == (hauroa - 1):
                reo += "tahi"
            # If the previous conditions are not satisfied, then the corresponding word for the digit (stored in the dictionary) is written
            else:
                reo += tau_kupu[kupu[i]]

            # The 100s, 10s and 1s positions loop in cycles of 3.
            # The function determines which position it is by taking the modulo of the difference between the index and string length upon division by 3.
            # 0 = 100s, 1 = 10s, 2 = 1s.

            # If there is a non-zero digit in the 100s position, the word for 'hundred' is written.
            if (hauroa - i) % 3 == 0:
                reo += " rau "
            # If there is a non-zero digit in the 10s position, the word for 'ten' is written. Multiples of 10 are written as the digit multiplier followed by 10.
            elif (hauroa - i) % 3 == 2:
                reo += " tekau "
                # The 10 carryover variable is activated if a 10 is written
                mā = True
            # If there is a non-zero digit in the 1s position, it is passed to the order of magnitude function to determine whether a placeholder needs to be written
            elif (hauroa - i) % 3 == 1:
                reo += kaha_kaituhituhi(hauroa, i)

    # If all the digits were 0, nothing would be written, and the empty string would evaluate as False.
    if reo:
        # Fixes excess whitespace and commas on the end, returns the number's words.
        return clean_whitespace(reo).strip(',')
    else:
        # If all digits were 0, it returns the word for 0.
        return 'kore'


def kaha_kaituhituhi(hauroa, i):
    if (hauroa - i) // 3 == 1:
        kupu = " mano, "
    elif (hauroa - i) // 3 == 2:
        kupu = " miriona, "
    elif (hauroa - i) // 3 == 3:
        kupu = " piriona, "
    else:
        kupu = ""

    return kupu


def pakaru_moni(tau):
    moni = False
    pāuna, herengi, pene = "", "", ""

    if tau[0] == '£':
        moni = True
        tau = tau[1:]

    tau_pakaru = tau.split(',,')

    pāuna = hōputu_kupu(tau_pakaru[0])
    pāuna = pāuna if pāuna != 'kore' else ''
    if len(tau_pakaru) > 1 and tau_pakaru[1]:
        herengi = hōputu_kupu(tau_pakaru[1])
        herengi = herengi if herengi != 'kore' else ''
    if len(tau_pakaru) > 2 and tau_pakaru[2]:
        pene = hōputu_kupu(tau_pakaru[2])
        pene = pene if pene != 'kore' else ''

    if pāuna:
        if moni:
            pāuna = "pāuna moni " + pāuna
        if (herengi or pene):
            pāuna += ", "

    if herengi:
        if pāuna:
            if herengi != 'tahi':
                herengi = "ngā " + herengi
            else:
                herengi = "te " + herengi
            herengi = "me " + herengi
        herengi += " herengi "

    if pene:
        if (pāuna or herengi):
            if pene != 'tahi':
                pene = "ngā " + pene
            else:
                pene = "te " + pene
            pene = "me " + pene
        pene += " pene"

    return clean_whitespace(pāuna + herengi + pene)


def tāima_kupu(tau):
    āpānoa = False

    ngā_tau = tau.split('.')
    pakaru = tau.split(' ')
    if len(pakaru) == 1:
        rā = None
    else:
        rā = True if ('a' in tau.split(' ')[1]) else False

    hāora = ngā_tau[1]
    miniti = ngā_tau[2].split(' ')[0]

    if eval(miniti) > 30:
        miniti = str(60 - eval(miniti))
        āpānoa = True

    if āpānoa and hāora == '12':
        hāora = 'tahi'
    elif āpānoa:
        if hāora == '11' and rā != None:
            rā = not rā
        hāora = hōputu_kupu(str(eval(hāora) + 1))
    else:
        hāora = hōputu_kupu(hāora)
    miniti = hōputu_kupu(miniti)

    return miniti + (" ki" if āpānoa else " mai i") + " te " + hāora + " te wā" + (" i te " + ("ata" if rā else "ahiahitanga") if rā != None else "")


def rā_kupu(tau):
    rā = {'1': 'Hānuere', '2': 'Pēpuere', '3': 'Māehe', '4': 'Āpereira', '5': 'Mei', '6': 'Hune',
          '7': 'Hūrae', '8': 'Ākuhata', '9': 'Hepetema', '10': 'Oketopa', '11': 'Noema', '12': 'Tīhema'}

    ngā_tau = tau.split('/')
    reo = "ā "
    if len(ngā_tau[0]) == 1:
        reo += "tua"
    reo += hōputu_kupu(ngā_tau[0]) + " o ngā rā o " + rā[ngā_tau[1]]

    if len(ngā_tau) <= 2:
        return reo

    reo += " i te tau o tō tātou Ariki kotahi mano "

    if eval(ngā_tau[2]) < 35:
        reo += hōputu_kupu('9')
    else:
        reo += hōputu_kupu('8')

    reo += " rau " + hōputu_kupu(ngā_tau[2])
    return reo


def search(file):
    frequency_dictionary = {}
    file.seek(0)
    reader = csv.reader(file)
    for row in reader:
        list1 = row[9].split()
        for word in list1:
            if all(letters in "0123456789.,pd£/:" for letters in word):
                if word not in frequency_dictionary:
                    frequency_dictionary[word] = 0
                frequency_dictionary[word] += 1
    list1 = list(frequency_dictionary.keys())
    list1.sort()
    return list1


def seek(file, kupu):
    file.seek(0)
    reader = csv.reader(file)
    for row in reader:
        if kupu in row[9]:
            print(row[10])
