import math
import threading
import time

FILES = [
	"primes-real.txt",
	"primes-fake.txt",
]
COMMENT_CHARACTER = "#"
NUMBER_OF_THREADS = 2

def measureRunningTime(func, *args):
	startTime = time.time()
	func(*args)
	return time.time() - startTime

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
			if line[0] != COMMENT_CHARACTER and int(line) >= 2 * NUMBER_OF_THREADS:
				numbers.append(int(line))
		f.close()
	return numbers

def threadFunc(barrier, name, number, calculator, input):
	print("- Thread " + str(name) + " start")
	remainder = 1
	for i in range(input[0], input[1] + 1):
		remainder = (remainder * i) % number
	calculator.calculateRemainder(remainder)
	print("- Thread " + str(name) + " stop")
	barrier.wait()
	print("- Thread " + str(name) + " end")

class ThuyBarrier:
	def __init__(self, number):
		self.number = number
		self.mutex  = threading.Lock()

	def wait(self):
		self.mutex.acquire()
		self.number = self.number - 1
		self.mutex.release()
		while self.number > 0:
			time.sleep(0.1)

class RemainerCalculator:
	def __init__(self, number, value):
		self.number = number
		self.value  = value
		self.mutex  = threading.Lock()

	def calculateRemainder(self, value):
		self.mutex.acquire()
		self.value = (self.value * value) % self.number
		self.mutex.release()

	def remainder(self):
		return self.value

class ThreadManager:
	def __init__(self, number, threadInputs, remainderCalculator):
		self.threadInputs 			 = threadInputs
		self.remainderCalculator = remainderCalculator
		self.number 						 = number
		self.barrier 						 = ThuyBarrier(NUMBER_OF_THREADS + 1)

	def __run__(self):
		threads = []
		for index, input in enumerate(self.threadInputs):
			thread = threading.Thread(target=threadFunc, name=index, args=(self.barrier, index, self.number, self.remainderCalculator, input))
			threads.append(thread)
			thread.start()
		self.barrier.wait()

	def run(self):
		runningTime = measureRunningTime(self.__run__)
		time.sleep(0.1)
		print("- THREAD RUNNING TIME: %.6f seconds" % runningTime)

class NaiveCheck:
	def __init__(self, number):
		self.number = number
		self.isPrime = False

	def __run__(self):
		result = 1
		for i in range(1, self.number):
			result = (result * i) % self.number
		self.isPrime = result == self.number - 1

	def run(self):
		runningTime = measureRunningTime(self.__run__)
		print("- NAIVE RUNNING TIME: %.6f seconds" % runningTime)
		return self.isPrime

class ThreadCheck:
	def __init__(self, number):
		self.number = number

	def run(self):
		threadInputs = splitUp(NUMBER_OF_THREADS, self.number)
		calculator   = RemainerCalculator(self.number, 1)
		tm           = ThreadManager(self.number, threadInputs, calculator)
		tm.run()

		if calculator.remainder() == self.number - 1:
			return True
		return False

if __name__ == "__main__":
	numbers = getNumbersFromFiles()
	for number in numbers:
		print("Number: " + str(number))
		print("- THREAD RESULT: " + str(ThreadCheck(number).run()))
		print("- NAIVE RESULT: " + str(NaiveCheck(number).run()))
