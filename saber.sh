#!/bin/sh
if [ $# = 1 ]
then
  python cli.py
else
  python cli.py $*
fi
