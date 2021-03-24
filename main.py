import math
import threading

FILES = [
	"primes-real.txt",
	"primes-fake.txt",
]
COMMENT_CHARACTER = "#"
NUMBER_OF_THREADS = 4

def splitUp(numberOfThreads, number):
	if number < 2 * numberOfThreads:
		return [[1, number-1]]

	results = []
	for i in range(0, numberOfThreads):
		start = math.floor(i * (number - 1) / numberOfThreads) + 1
		end   = math.floor((i + 1) * (number - 1) / numberOfThreads)
		results.append([start, end])
	return results

def getNumbersFromFiles():
	numbers = []
	for file in FILES:
		f = open(file, "r")
		for line in f.read().splitlines():
			if line[0] != COMMENT_CHARACTER:
				numbers.append(int(line))
		f.close()
	return numbers

def checkPrime(number):
	if number == 1:
		return False

	threadInputs = splitUp(NUMBER_OF_THREADS, number)
	calculator   = RemainerCalculator(number, 1)
	tm           = ThreadManager(threadInputs, calculator)
	tm.run()

	if calculator.remainder() == number - 1:
		return True
	return False

def threadFunc(calculator, input):
	for i in range(input[0], input[1] + 1):
		calculator.calculateRemainder(i)

class RemainerCalculator:
	def __init__(self, number, value):
		self.number = number
		self.value  = value

	def calculateRemainder(self, value):
		self.value = (self.value * value) % self.number

	def remainder(self):
		return self.value

class ThreadManager:
	def __init__(self, threadInputs, remainderCalculator):
		self.threadInputs = threadInputs
		self.remainderCalculator = remainderCalculator

	def run(self):
		threads = []
		for index, input in enumerate(self.threadInputs):
			thread = threading.Thread(target=threadFunc, name=index, args=(self.remainderCalculator, input))
			threads.append(thread)
			thread.start()
		for thread in threads:
			thread.join()

if __name__ == "__main__":
	numbers = getNumbersFromFiles()
	for number in numbers:
		if checkPrime(number):
			print("RESULT: " + str(number) + " is a prime number")
		else:
			print("RESULT: " + str(number) + " is not a prime number")
