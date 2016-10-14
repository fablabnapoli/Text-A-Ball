
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt

host = "a9pmbvndre08y.iot.us-east-1.amazonaws.com"

#tabid = "TaB_01"
#rootCAPath = "/home/root/certs/root-CA.crt"
#certificatePath = "/home/root/certs/e0c16ebcd7-certificate.pem.crt"
#privateKeyPath = "/home/root/certs/e0c16ebcd7-private.pem.key"

tabid = "TaB_02"
rootCAPath = "/home/root/certs/root-CA.crt"
certificatePath = "/home/root/certs/4cc693a981-certificate.pem.crt"
privateKeyPath = "/home/root/certs/4cc693a981-private.pem.key"

#tabid = "TaB_03"
#rootCAPath = "/home/root/certs/root-CA.crt"
#certificatePath = "/home/root/certs/09bc0ffc96-certificate.pem.crt"
#privateKeyPath = "/home/root/certs/09bc0ffc96-private.pem.key"

# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

# Usage
usageInfo = """Usage:

python TaB_AWS.py -t <topic> -m <message>
"""

try:
	opts, args = getopt.getopt(sys.argv[1:], "t:m:", ["topic=", "message="])
	if len(opts) == 0:
		raise getopt.GetoptError("No input parameters!")
	for opt, arg in opts:
		if opt in ("-t", "--topic"):
                    topic = arg
		if opt in ("-m", "--message"):
                    message = arg
except getopt.GetoptError:
	print(usageInfo)
	exit(1)

# Missing configuration notification
missingConfiguration = False
if not topic:
	print("Missing '-t' or '--topic'")
	missingConfiguration = True
if not message:
	print("Missing '-m' or '--message'")
	missingConfiguration = True

if missingConfiguration:
	exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")  # Python 2
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(tabid)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
time.sleep(2)

# Publish to the same topic
print("Sending message: "+message)
myAWSIoTMQTTClient.publish(topic, message, 1)
