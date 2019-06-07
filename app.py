import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

primeList = "numbers"


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits') #hits is a key which is stored on/in reddis. 
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

#this is a comment
@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/isPrime/<int:number>')
def isPrimeNumber(number):
	if (number <=1): #get rid of 1s, 0s and anything less than that since they are not prime 
		return 'Please enter a number greater than 1.\n'

	if (number <=3): #catch entries of 2 and 3 before we start checking remainders as 2 and 3 are prime but 2%2 = 0 
		cache.lpush('primeList', number)
		return '{} is a prime number.\n'.format(number)
		
	if(number % 2 == 0 or number % 3 == 0): #if the number isn't <=3, but can be % by 2 or 3 and it equals zero, it's not prime 
		return '{} is not a prime number.\n'.format(number)

	i = 5
	while(i * i <number):
		if (number % i == 0 or number %(i + 2) ==0): 
			return '{} is not a prime number.\n'.format(number)
		#we start from 5 and go up by 6 each iteration, 
		
		i = i + 6
	cache.lpush('primeList', number)
	return '{} is a prime number.\n'.format(number)

			
	
	
@app.route('/primesStored')
def listPrime():	
	#lrange might be the easiest way to return list of everything that goes into primeList 
	return 'length is {}.\n'.format(cache.lrange('primeList', 0, -1)) #this works 



#this clear list method is to obviously clear the list, and reset it for testing purposes 
@app.route('/clearList')
def listClear():
	for i in range (0, cache.llen('primeList')):
		cache.lpop('primeList') 
	return 'List has been cleared.\n'
	