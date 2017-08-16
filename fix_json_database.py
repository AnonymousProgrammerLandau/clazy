#!/usr/bin/env python2


# This file is part of the clazy static checker.

# Copyright (C) 2017 Sergio Martins <smartins@kde.org>

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.

# You should have received a copy of the GNU Library General Public License
# along with this library; see the file COPYING.LIB.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.

# This script is useful for fixing the json database, in case there's compiler flags
# you want to remove or add. One such example is when you're required to build your
# project with Apple clang, which will then generate pch errors when running
# clazy.

import json, sys, string

#-------------------------------------------------------------------------------
# Filters. Configure here.

# Removes arguments starting with -include
def filter_no_pch(str):
    return not str.startswith("-include")

def remove_pch(c_splitted):
    return filter(filter_no_pch, c_splitted)

def fix_command(c):
    c_splitted = c.split()
    c_splitted = remove_pch(c_splitted)
    return string.join(c_splitted)
#-------------------------------------------------------------------------------
# Main:

f = open(sys.argv[1], 'r')
contents = f.read()
f.close()

decoded = json.loads(contents)
new_decoded = []

for cmd in decoded:
    if 'command' not in cmd:
        continue

    cmd['command'] = fix_command(cmd['command'])
    new_decoded.append(cmd)

new_contents = json.dumps(new_decoded)
print new_contents
