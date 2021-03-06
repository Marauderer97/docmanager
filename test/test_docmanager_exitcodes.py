#!/usr/bin/python3

import pytest
import shlex
from docmanager.cli import parsecli
from docmanager.action import Actions
from docmanager.core import ReturnCodes
from xml.sax._exceptions import SAXParseException

def test_exitcodes_0(tmp_broken_xml):
    """ call docmanager without params """
    try:
        parser = parsecli([])
    except SystemExit as e:
        assert e.code == ReturnCodes.E_CALL_WITHOUT_PARAMS, \
            "Expected exit code {} but got {}.".format(ReturnCodes.E_CALL_WITHOUT_PARAMS,
                                                       e.code)

def test_exitcodes_1(tmp_broken_xml):
    """ parse broken xml file in get """
    try:
        clicmd = "get {}".format(tmp_broken_xml)
        a = Actions(parsecli(shlex.split(clicmd)))
    except SystemExit as e:
        assert e.code == ReturnCodes.E_XML_PARSE_ERROR, \
            "Expected exit code {} but got {}.".format(ReturnCodes.E_XML_PARSE_ERROR,
                                                       e.code)

def test_exitcodes_2(tmp_invalid_db5_file):
    """ check for an invalid DocBook 5 file """
    try:
        clicmd = "get {}".format(tmp_invalid_db5_file)
        a = Actions(parsecli(shlex.split(clicmd)))
    except SystemExit as e:
        assert e.code == ReturnCodes.E_INVALID_XML_DOCUMENT, \
            "Expected exit code {} but got {}.".format(ReturnCodes.E_INVALID_XML_DOCUMENT,
                                                       e.code)

def test_exitcodes_3(tmp_invalid_db5_file):
    """ check for an invalid DocBook 5 file """
    try:
        clicmd = "get invalid_file_name.xml"
        a = Actions(parsecli(shlex.split(clicmd)))
        a.parse()
    except SystemExit as e:
        assert e.code == ReturnCodes.E_FILE_NOT_FOUND, \
            "Expected exit code {} but got {}.".format(ReturnCodes.E_FILE_NOT_FOUND,
                                                       e.code)
