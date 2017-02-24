import sys

def decodingError(refData,sysData):
	score = 0
	for i,(rSent,sSent) in enumerate(zip(refData,sysData)):
		flag = True
		for (rTok,rTag),(sTok,sTag) in zip(rSent,sSent):
			if rTok != sTok:
				print 'Error on line %d: tokens in output not aligned to reference!'%(i+1)
				flag = False
				break
			elif rTag != sTag:
				print 'Error on line %d: tagging is incorrect!'%(i+1)
				flag = False
				break
		if flag:
			score += 1
	return score
	
if __name__ == '__main__':
	ref = [[i.split('_') for i in l.strip().split()] for l in open(sys.argv[1])]
	sys = [[i.split('_') for i in l.strip().split()] for l in open(sys.argv[2])]

	print decodingError(ref,sys)