import requests
import time
import os

subscription_key = 'YOUR_SUBSCRIPTION_KEY'
location = "centralindia"
input_file = "sentences.txt"
output_folder = "output_mp3"

if not os.path.exists(output_folder):
	os.makedirs(output_folder)
if subscription_key == 'YOUR_SUBSCRIPTION_KEY':
	print("Kindly modify the subscription key inside this file (line 5). \nExiting...")
	exit()

def get_token():
	token_url = "https://{}.api.cognitive.microsoft.com/sts/v1.0/issueToken".format(location)
	headers = {
		'Ocp-Apim-Subscription-Key' : subscription_key
	}
	response = requests.post(token_url, headers=headers)
	access_token = str(response.text)
	return access_token

def generate_speech(input_text, outfile, token):
	url = "https://{}.tts.speech.microsoft.com/cognitiveservices/v1".format(location)
	header = {
		'Authorization': 'Bearer '+str(token),
		'Content-Type': 'application/ssml+xml',
		'X-Microsoft-OutputFormat': 'audio-24khz-160kbitrate-mono-mp3'
	}

	'''
	You can customise your speech output here
	by changing language, gender and name
	'''
	data = "<speak version='1.0' xml:lang='en-US'>\
				<voice xml:lang='en-US' xml:gender='Female' name='en-US-AriaNeural'>\
					{}\
				</voice>\
		   </speak>".format(input_text)
	try:
		response = requests.post(url, headers=header, data=data)
		response.raise_for_status()
		with open(outfile, "wb") as file:
			file.write(response.content)
		print(response)
		response.close()
	except Exception as e:
		print("ERROR: ", e)

def sleep_and_refresh(i):
	if i>0 and i%7==0: # Extra sleep 
		time.sleep(61)
	return get_token() # Generate new token

if __name__ == "__main__":
	token = get_token() # Each Token is valid for 10 minutes
	with open(input_file, 'r') as infile:
		sentences = infile.readlines()
		for i, sentence in enumerate(sentences):
			print(i, sentence)
			outfile = os.path.join(output_folder, "{}_azure.mp3".format(i))
			generate_speech(sentence, outfile, token)
			time.sleep(1) # Avoiding too many requests
			# token = sleep_and_refresh(i)  # Enable only when input file is large
		print("DONE!")
