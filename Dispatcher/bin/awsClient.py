from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

class awsSender():

	client = None
	host = "a9pmbvndre08y.iot.us-east-1.amazonaws.com"
	
	def __init__(self, auth):

		# Client init
		self.client = AWSIoTMQTTClient(auth['tabId'])
		self.client.configureEndpoint(self.host, 8883)
		
		
		self.client.configureCredentials(auth['rootcapath'], auth['privatekeypath'], auth['certificatepath'])
		
		# connection configuration
		self.client.configureAutoReconnectBackoffTime(1, 32, 20)
		# Infinite offline Publish queueing
		self.client.configureOfflinePublishQueueing(-1)  
		# Draining: 2 Hz
		self.client.configureDrainingFrequency(2)  
		# 10 sec
		self.client.configureConnectDisconnectTimeout(10)  
		# 5 sec
		self.client.configureMQTTOperationTimeout(5)
	
	def connect(self):
		self.client.connect()
		time.sleep(2)
		
	def sendMsg(self, dest, msg):
		print("awsSender.sendMsg - Sending message: %s" %(msg))
		self.client.publish(topic, msg, 1)
		pass
	
	def disconnect(self):
		pass
	
