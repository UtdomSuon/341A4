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
#need to make sure that the datatype parameters are also within the def so that it's defined. 
	#check if the number entered is a prime 
	if number > 1:
		for i in range(2, number//2):
			if(number % i) ==0:
				return '{} is not a prime number.\n'.format(number)
				break
			else:
				cache.lpush('primeList', number)
				return '{} is a prime number.\n'.format(number)

	else:
		return 'Please enter a number greater than 1.\n'


@app.route('/primesStored')
def listPrime():	
	#lrange might be the easiest way to return list of everything that goes into primeList 
	return 'length is {}.\n'.format(cache.lrange('primeList', 0, -1)) #this works 
	