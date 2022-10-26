# coding=utf-8
"""Contains methods for command line interaction"""
import argparse


def parse_args():
    """
    Creates the argument parser for the command line
    :return: the args that were parsed from the command line
    """
    # This file contains the commandline tools for the current tool
    parser = argparse.ArgumentParser(prog='cc_dcr.py', usage='cc_dcr.py [options]')
    parser.add_argument('--eventLog', nargs='?', default='Resources/Hospital_Billing_Event_Log.xes',
                        help='The path pulling the event log')
    parser.add_argument('--XmlDcr', nargs="?", default='Resources/Hospital_BIlling.xml',
                        help='The input path for the DCR Graph xml')
    parser.add_argument('--useCelonis', nargs="?", help="Link to the Celonis instance")

    return parser.parse_args()
