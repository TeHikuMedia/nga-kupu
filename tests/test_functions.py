import context
from taumahi import *


def test_māori_word():
    assert hihira_raupapa_kupu('kupu', True)


def test_māori_uppercase():
    assert hihira_raupapa_kupu('KUPU', True)


def test_english_word():
    assert not hihira_raupapa_kupu('mittens', True)


def test_tohutō():
    assert hihira_raupapa_kupu('rōpū', True)


def test_ignore_tohutō():
    assert not hihira_raupapa_kupu('ropu', False)


def test_check_list():
    assert hihira_raupapa(['kupu', 'cheese']) == (['kupu'], ['cheese'])


def test_waitangi():
    assert hihira_raupapa_kupu('Waitangi', True)


def test_hihira_raupapa_kupu():
    assert not hihira_raupapa_kupu('ae', False)


def test_hōputu():
    assert hōputu('ngawha') == 'ŋaƒa'
    assert hōputu('Wha') == 'Ƒa'
    assert hōputu('Nga') == 'Ŋa'
    assert hōputu('WHA') == 'ƑA'
    assert hōputu('NGA') == 'ŊA'

def test_hōputu_whakahou():
    assert hōputu_whakahou('ŋaƒa') == 'ngawha'
    assert hōputu_whakahou('Ƒa') == 'Wha'
    assert hōputu_whakahou('Ŋa') == 'Nga'
    assert hōputu_whakahou('ƑA') == 'WHA'
    assert hōputu_whakahou('ŊA') == 'NGA'

def test_nahanaha():
    assert nahanaha(['WHENUA', 'TANGATA']) == ['TANGATA', 'WHENUA']


def test_kōmiri_kupu():
    assert list(kōmiri_kupu('tangata he ball')) == [
        {'tangata': 1}, {'he': 1}, {'ball': 1}]


def test_auaha_raupapa_tū():
    assert list(auaha_raupapa_tū('tangata ball')) == [
        {'tangata': 1}, {'ball': 1}]

def test_kupu_māori():
    assert kupu_māori("tangata he ball") == set(["tangata"])

def test_kupu_pākehā():
    assert kupu_pākehā("tangata he ball") == set(["ball"])
    assert kupu_pākehā('r') == set('r')

def test_punctuation():
    assert kupu_pākehā('kaipupuri’’') == set()
    assert kupu_māori('kaipupuri’’') == set(["kaipupuri’’"])
    assert list(kōmiri_kupu("tangata he ball ’’")) == [{'tangata': 1}, {'he': 1, '’’': 1}, {'ball': 1}]