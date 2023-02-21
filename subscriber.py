import os
import paho.mqtt.client as mqtt

fileNumber = {"100B": 0, "10KB": 0, "1MB": 0, "10MB": 0}

def createFolderStructure():
    folder_name = "DataReceived"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    filenames = ['100B', '10KB', '1MB', '10MB']
    for subfolder in filenames:
        subfolder_name = os.path.join(folder_name, subfolder)
        if not os.path.exists(subfolder_name):
            os.mkdir(subfolder_name)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("100B", qos=1)
    client.subscribe("10KB", qos=1)
    client.subscribe("1MB", qos=1)
    client.subscribe("10MB", qos=1)



def on_message(client, userdata, msg):
    global fileNumber
    fileNumber[msg.topic] += 1
    fileName = os.path.join("DataReceived", msg.topic, str(fileNumber[msg.topic]))
    with open(fileName, "wb") as file:
        file.write(msg.payload)
    print("File received and written to disk")

createFolderStructure()

client = mqtt.Client(client_id="subscriber",clean_session=True)
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.191", 1883, 60)

client.loop_forever()
