import os
import sys
import pytest
import xlrd
import tempfile
from pyfas import Tpl

TEST_FLD = os.getcwd() + os.sep + "test_files" + os.sep

def test_not_a_tpl():
    with pytest.raises(ValueError) as exeinfo:
        tpl = Tpl(TEST_FLD+"/FC1_rev01.ppl")
        assert exinfo.value.message == "not a tpl file"

def test_init_same_folder():
    tpl = Tpl("tpl_file.tpl")
    assert tpl.path == ''
    assert tpl.fname == "tpl_file.tpl"

def test_init():
    tpl = Tpl(TEST_FLD+"FC1_rev01.tpl")
    assert tpl.fname == "FC1_rev01.tpl"
    assert tpl.path == TEST_FLD[:-1]

def test_attributes():
    tpl = Tpl(TEST_FLD+"/FC1_rev01.tpl")
    assert tpl._attributes['CATALOG'] == 331
    assert tpl._attributes['data_idx'] == 421
    assert 'VOLGB' in tpl.trends[1]

def test_extraction():
    tpl = Tpl(TEST_FLD+"/FC1_rev01.tpl")
    tpl.extract(3)
    assert tpl.data[3][0] == 9.973410e6
    assert 'Pressure' in tpl.label[3]

def test_filter():
    tpl = Tpl(TEST_FLD+"/FC1_rev01.tpl")
    PTs = tpl.filter_data('PT')
    assert 'PT' in PTs[3]
    assert 'POSITION' in PTs[3]
    assert 'TIEIN' in PTs[3]
    tpl.trends
    assert 'VOLGB' in tpl.trends[1]

def test_to_excel():
    tpl = Tpl(TEST_FLD+"/FC1_rev01.tpl")
    tpl.to_excel()
    assert "FC1_rev01_tpl.xlsx" in os.listdir(TEST_FLD)
    xl = xlrd.open_workbook(TEST_FLD+"/FC1_rev01_tpl.xlsx")
    sh = xl.sheet_by_index(0)
    assert sh.cell_value(3, 4) == 9.973300e+06
    os.remove(TEST_FLD+"/FC1_rev01_tpl.xlsx")
    temp_folder = tempfile.gettempdir()
    tpl.to_excel(temp_folder)
    assert "FC1_rev01_tpl.xlsx" in os.listdir(temp_folder)
    os.remove(temp_folder+"/FC1_rev01_tpl.xlsx")
