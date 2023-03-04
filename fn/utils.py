def remove_comma(n):
	val = n.strip().split(',')
	return int(val[0]) if len(val) <= 1 else int(val[0]+val[1])