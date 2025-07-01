import requests

#response = requests.get("https://th.bing.com/th/id/OIP.P3UcCoQSC6G9foq0rpCfMAHaEJ?w=309&h=180&c=7&r=0&o=7&pid=1.7&rm=3")
#print(response.content)

SUBSCRIPTION_KEY = "7Xzkvw2JddYlTvQjGzGzHEw5FmYcIZAODXFtqyxXp8Sj1WvfUcCGJQQJ99BGACYeBjFXJ3w3AAAFACOG28nn"
ENDPOINT = "https://labuser15-computervision-001.cognitiveservices.azure.com/"

def analyze_image(image_path):
    ENDPOINT_URL = ENDPOINT + "vision/v3.2/analyze"

    params = {"visualFeatures":"Categories,Description,Color"}
    headers = {
        "Ocp-Apim-Subscription-Key":SUBSCRIPTION_KEY,
        "Content-Type":"application/octet-stream"
    }

    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
    except Exception as e:
        print(f"Error reading image file: {e}")
        return None
    
    response = requests.post(ENDPOINT_URL, params=params, headers=headers, data=image_data)
    if response.status_code == 200 :
        analysis = response.json()
        return analysis
    else:
        print(f"Error : {response.status_code} - {response.text}")
        return None
    

def main():
    image_path = input("Enter the path to the image file: ")
    
    result = analyze_image(image_path)
    if result:
        print("Analysis_Result: ")
        print(result)


if __name__ == "__main__" :
    main()