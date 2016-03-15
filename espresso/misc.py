###############################
#  This file is part of PyLaDa.
#
#  Copyright (C) 2013 National Renewable Energy Lab
#
#  PyLaDa is a high throughput computational platform for Physics. It aims to make it easier to
#  submit large numbers of jobs on supercomputers. It provides a python interface to physical input,
#  such as crystal structures, as well as to a number of DFT (VASP, CRYSTAL) and atomic potential
#  programs. It is able to organise and launch computational jobs on PBS and SLURM.
#
#  PyLaDa is free software: you can redistribute it and/or modify it under the terms of the GNU
#  General Public License as published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  PyLaDa is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
#  the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with PyLaDa.  If not, see
#  <http://www.gnu.org/licenses/>.
###############################

# -*- coding: utf-8 -*-
__docformat__ = "restructuredtext en"
__all__ = ['write_f90namelist', 'write_pwscf_input']
from ..espresso import logger

def write_f90namelist(f90namelist, stream=None):
    """ Writes namelist to file or string, or stream

        - if stream is None (default), then returns a string containing namelist in fortran
            format
        - if stream is a string, then it should a path to a file
        - otherwise, stream is assumed to be a stream of some sort, with a `write` method

        Keywords are passed on to :py:method:`Namelist.namelist`
    """
    from f90nml import Namelist as F90Namelist
    from os.path import expanduser, expandvars, abspath
    from io import StringIO
    if stream is None:
        result = StringIO()
        write_f90namelist(f90namelist, result)
        result.seek(0)
        return result.read()

    if isinstance(stream, str):
        path = abspath(expanduser(expandvars(stream)))
        logger.log(10, "Writing fortran namelist to %s" % path)
        with open(path, 'w') as file:
            write_f90namelist(f90namelist, file)
        return

    for key, value in f90namelist.items():
        if isinstance(value, list):
            for g_vars in value:
                f90namelist.write_nmlgrp(key, g_vars, stream)
        elif isinstance(value, F90Namelist):
            f90namelist.write_nmlgrp(key, value, stream)
        else:
            raise RuntimeError("Can only write namelists that consist of namelists")


def write_pwscf_input(f90namelist, cards, stream=None):
    """ Writes input to stream

        - if strean is None (default), then returns a string containing namelist in fortran
            format
        - if strean is a string, then it should a path to a file
        - otherwise, strean is assumed to be a stream of some sort, with a `write` method
    """
    from f90nml import Namelist as F90Namelist
    from os.path import expanduser, expandvars, abspath
    from copy import copy
    from io import StringIO

    if stream is None:
        result = StringIO()
        write_pwscf_input(f90namelist, cards, result)
        result.seek(0)
        return result

    if isinstance(stream, str):
        path = abspath(expanduser(expandvars(stream)))
        logger.info("Writing Pwscf input to file %s", path)
        with open(path, 'w') as file:
            write_pwscf_input(f90namelist, cards, file)
        return

    write_f90namelist(f90namelist, stream=stream)
    for value in cards:
        stream.write(str(value) + "\n")
