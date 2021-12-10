from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
msg1=dict({'first_name':'xxxx','last_name':'yyyy','company_name':'zzz.'})
producer.send('test', bytes(str(msg1), 'utf-8'))
producer.flush()

{'person_id':8, 'creation_time':'2020-01-05 10:37:06.000000', 'latitude' : '-122.290883','longitude':'37.55363'}