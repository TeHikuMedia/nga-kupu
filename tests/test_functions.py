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
    assert hōputu('ngawha') == 'ŋaƒa' and hōputu('Wha') == 'Ƒa' and hōputu(
        'Nga') == 'Ŋa' and hōputu('WHA') == 'ƑA' and hōputu('NGA') == 'ŊA'


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