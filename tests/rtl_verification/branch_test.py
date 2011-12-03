from testcase import TestCase

class BranchTests(TestCase):
	def test_goto():
		return ({ 'u1' : 1 }, '''		
					goto label1
					u0 = u0 + 5
					goto ___done
		label1 		u0 = u0 + 12
					goto ___done
		''', { 'u0' : 12 }, None, None, None)

	
	def test_pcDest():
		return ({}, '''		
						u0 = &label
						pc = u0
						goto ___done
						u1 = u1 + 13
						goto ___done
			label		u1 = u1 + 17
						goto ___done
						u1 = u1 + 57
						goto ___done
			''',
			{ 'u0' : None, 'u1' : 17 }, None, None, None)

	def test_bzeroTaken():
		return ({ 'u1' : 0 }, '''		
						if !u1 goto label1
						u0 = u0 + 5
						goto ___done
			label1 		u0 = u0 + 12
						goto ___done
			''', { 'u0' : 12 }, None, None, None)
		
	def test_bzeroNotTaken():
		return ({ 'u1' : 1 }, '''		
						if !u1 goto label1
						u0 = u0 + 5
						goto ___done
			label1 		u0 = u0 + 12
						goto ___done
			''', { 'u0' : 5 }, None, None, None)
		
	def test_bnzeroNotTaken():
		return ({ 'u1' : 0 }, '''		
						if u1 goto label1
						u0 = u0 + 5
						goto ___done
			label1 		u0 = u0 + 12
						goto ___done
			''', { 'u0' : 5 }, None, None, None)

	def test_bnzeroTaken():		
		return ({ 'u1' : 1 }, '''			
						if u1 goto label1
						u0 = u0 + 5
						goto ___done
			label1 		u0 = u0 + 12
						goto ___done
			''', { 'u0' : 12 }, None, None, None)

	def test_ballNotTakenSomeBits():
		return ({ 'u1' : 1 }, '''		
						if all(u1) goto label1
						u0 = u0 + 5
						goto ___done		
			label1 		u0 = u0 + 12
						goto ___done		
			''', { 'u0' : 5 }, None, None, None)

	def test_ballNotTakenNoBits():
		return ({ 'u1' : 0 }, '''		
						if all(u1) goto label1
						u0 = u0 + 5
						goto ___done
			label1 		u0 = u0 + 12
						goto ___done
			''', { 'u0' : 5 }, None, None, None)

	def test_ballTaken():
		return ({ 'u1' : 0xffff }, '''		
						if all(u1) goto label1
						u0 = u0 + 5
						goto ___done
			label1 		u0 = u0 + 12
						goto ___done
			''', { 'u0' : 12 }, None, None, None)
	
	def test_ballTakenSomeBits():
		return ({ 'u1' : 0x20ffff }, '''		
						if all(u1) goto label1
						u0 = u0 + 5
						goto ___done
			label1 		u0 = u0 + 12
						goto ___done
			''', { 'u0' : 12 }, None, None, None)

	def test_rollback():
		return ({},'''
				goto label1
				u0 = u0 + 234
				u1 = u1 + 456
				u2 = u2 + 37
				u3 = u3 + 114
		label3	u4 = u4 + 9
				goto ___done
				u5 = u5 + 12
		label1	goto label3
				u4 = u4 + 99
		''', { 'u4' : 9 }, None, None, None)
		
	def test_call():
		return ({}, '''		
						call label1
						u0 = u0 + 7
						goto ___done
			label1 		u0 = u0 + 12
						goto ___done
			''', { 'u0' : 12, 'u30' : 8 }, None, None, None)
		
		
	def test_pcload():
		return ({}, '''
		
					s0 = &pc_ptr
					pc = mem_l[s0]
					goto ___done
					s1 = s1 + 12
					goto ___done
			target	s1 = s1 + 17
					goto ___done
					s1 = s1 + 29
					
			pc_ptr	.word target
			''', { 'u0' : None, 'u1' : 17 }, None, None, None)
			
	# TODO: add some tests that do control register transfer, 
	# and memory accesses before a rollback.  Make sure side
	# effects do not occur