import grpc
import orders_pb2
import orders_pb2_grpc
from orders_pb2 import PersonMessage, LocationMessage

from datetime import datetime

# open a gRPC channel
channel = grpc.insecure_channel('localhost:5003')

# create a stub (client)
stub = orders_pb2_grpc.CallServiceStub(channel)

# create a valid request message
person = PersonMessage(first_name="Ness" , last_name="Pllana", company_name="cuburn")
stub.create_person(person)
print(person)
