import functools


def no_recursion(f):
	busy = False
	@functools.wraps(f)
	def g(*args, **kwargs):
		nonlocal busy
		if busy: return 
		busy = True
		try:
			f(*args, **kwargs)
		finally:
			busy = False
	return g
