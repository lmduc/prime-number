FILES = [
  "primes-fake.txt",
  "primes-real.txt",
]
COMMENT_CHARACTER = "#"

if __name__ == "__main__":
  numbers = []
  for file in FILES:
    f = open(file, "r")
    for line in f.read().splitlines():
      if line[0] != COMMENT_CHARACTER:
        numbers.append(int(line))
    f.close()
