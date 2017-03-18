# marketEmulator

MarketRequest.py - Contains the data structures for authentication and requests, also the code for parsing them
RequestOperations.py - contains the extra code for request logic
MarketState.py - Contains the current state of the market, including the users and their resources. Automatically loads the state on init and saves when asked to
server.py - The main server code that receives data
make_keys.py - Generates public/private keys, not needed unless we want to recreate them
producer.py - Test client, will be upgraded to become a producer once the server is completed
marketTester.py - Test client

keys_private.txt - Contains private keys, each group will receive one of these (not commited to git)
keys_public.pkl - Pickle file containing the public keys, this is available for everyone
user_holdings.pkl - Contains the current market state and user inventory
request_ids.pkl - Contains the most recent request id created, used for generating unique request IDs
active_queries.pkl - Contains the active queries in the system