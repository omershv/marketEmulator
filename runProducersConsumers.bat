cd C:\marketEmulator

start python producer_consumer.py producer 4 10 user90
start python producer_consumer.py producer 5 20 user91
start python producer_consumer.py producer 6 10 user92
start python producer_consumer.py producer 7 20 user93
start python producer_consumer.py producer 8 30 user94
start python producer_consumer.py producer 9 10 user95

timeout 20

start python producer_consumer.py consumer 4 10 user80
start python producer_consumer.py consumer 5 10 user81
start python producer_consumer.py consumer 6 20 user82
start python producer_consumer.py consumer 7 20 user83
start python producer_consumer.py consumer 8 10 user84
start python producer_consumer.py consumer 9 30 user85

