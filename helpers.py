#!/usr/bin/python3
__author__ = 'NeptunDK'
import unittest
from collections import namedtuple

Order = namedtuple('Order', 'price vol player order_type')
Share = namedtuple('Share', 'stockname vol buyprice')
