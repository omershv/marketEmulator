cd C:\marketEmulator

start python producer_consumer.py consumer 0 10 user80
start python producer_consumer.py consumer 1 10 user81
start python producer_consumer.py consumer 2 20 user82

start python producer_consumer.py producer 0 10 user90
start python producer_consumer.py producer 1 20 user91
start python producer_consumer.py producer 2 10 user92