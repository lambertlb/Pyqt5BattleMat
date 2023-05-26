

class BitTest:
	def __init__(self):
		self.bitsPerColumn = 27
		self.bits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	def setBit(self, column, row, value):
		bitIndex = (row * self.bitsPerColumn) + column
		arrayIndex = bitIndex // 32
		bitShift = bitIndex % 32
		bitMask = 1 << bitShift
		word = self.bits[arrayIndex] & 0xffffffff
		if value:
			word |= bitMask
		else:
			word &= ~bitMask
		self.bits[arrayIndex] = word
		print(f'index {arrayIndex} {word:#x}')


# test = BitTest()
# for row in range(10):
# 	for column in range(27):
# 		test.setBit(column, row, True)

zz = 4227923967
print(f'{zz:#x}')
print(test.bits)