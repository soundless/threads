#!/usr/bin/python
#
# Copyright (c) Andrea Micheloni 2011
#
# Part of the tutorial available at http://www.tankmiche.com/
#
#       This program is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program.  If not, see <http://www.gnu.org/licenses/>.

from event_queue import EventQueue
import time, threading

def noparams():
	print "*** noparams() executed"
	return "noparams() result"

def param(one, two="something else"):
	print "*** param("+str(one)+") executed"
	return "param("+str(one)+") result"

def raiseexceptionnoparams():
	print "*** raiseexceptionnoparams() executed"
	raise ValueError("raiseexceptionnoparams() exception")

def raiseexceptionparam(one):
	print "*** raiseexceptionparam("+str(one)+") executed"
	raise ValueError("raiseexceptionparam("+str(one)+") exception")

eq = EventQueue()

results = [eq.enqueue(param,[1, 2]),
	eq.enqueue(param,kwargs={'one':2, 'two':2}),
	eq.enqueue(noparams,highPriority=True),
	eq.enqueue(raiseexceptionnoparams),
	eq.enqueue(raiseexceptionparam,[-1]),eq.stop(),
	eq.enqueue(param,["Over 9000"])]

for func in results:
	try:
		print str("Result: " + str(func()))
	except ValueError, e:
		print str("Result exception: " + str(e))
	except Exception, e:
		print str("Result exception: " + str(e))

try:
	lastHope=eq.enqueue(param,[1])
	print lastHope()
except Exception, e:
	print str("Last hope exception: " + str(e))
