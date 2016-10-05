#!/usr/bin/python
###############################################################################
#
# File Name         : ease.py
# Created By        : Thomas Aurel
# Creation Date     : April  1th, 2016
# Version           : 0.1
# Last Change       : June 27th, 2016 at 10:37:11 AM
# Last Changed By   : Thomas Aurel
# Purpose           : Ease main function
#
###############################################################################
from core.econtroller import EController

# from ihm.interface import Interface
# from core.environment import Environment
# import argparse


# parser = argparse.ArgumentParser()
# group_mode = parser.add_mutually_exclusive_group()
# group_mode.add_argument(
#         '-d', '--demo',
#         help='pass the application into demonstration mode',
#         action='store_true')
# group_mode.add_argument(
#         '-D', '--debug',
#         help='pass the application into debug mode',
#         action='store_true')
# parser.add_argument(
#         '-i', '--ip',
#         help='configure a default global IP for all exploits and scenarios',
#         )
# args = parser.parse_args()
# _d = ''
# _i = ''
#
# env = Environment()
#
# if args.demo:
#     env.setMode('DEMO')
# elif args.debug:
#     env.setMode('DEBUG')
#
# if args.ip:
#     env.setGlobal('HOST', args.ip)

c = EController()
c.execute(_o=None)
