import requests
import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# 환경변수 로드
load_dotenv()

# Image Analyze function
def analyze_image(image_path):
    ENDPOINT_URL = os.getenv("ENDPOINT") + "vision/v3.2/analyze"

    params = {"visualFeatures":"Categories,Description,Color"}
    headers = {
        "Ocp-Apim-Subscription-Key":os.getenv("SUBSCRIPTION_KEY"),
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

# Object Detection function
def object_detection(image_path):
    ENDPOINT_URL = os.getenv("ENDPOINT") + "vision/v3.2/detect"

    headers = {
        "Ocp-Apim-Subscription-Key":os.getenv("SUBSCRIPTION_KEY"),
        "Content-Type":"application/octet-stream"
    }

    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
    except Exception as e:
        print(f"Error reading image file: {e}")
        return None
    
    response = requests.post(ENDPOINT_URL, headers=headers, data=image_data)
    if response.status_code == 200 :
        analysis = response.json()
        return analysis
    else:
        print(f"Error : {response.status_code} - {response.text}")
        return None     

    
# create bounding box function
def create_bounding_box(image_path, detection_data):
    try:
        image = Image.open(image_path) # 이미지 읽어오기
    except Exception as e:
        print(f"Error opening image file: {e}")
        return None
    
    draw = ImageDraw.Draw(image) # 비트맵으로 형변환

    for obj in detection_data.get("objects", []): # detection data 에서 objects 를 리스트로 가져와서 개수만큼 반복
        rect = obj["rectangle"]
        x, y, w, h = rect["x"], rect["y"], rect["w"], rect["h"]
        draw.rectangle((x, y, x + w, y + h), outline="red", width=2) # 사각형 그리기 굵기 2

        label = obj["object"] # 객체 이름
        draw.text((x, y), label, fill="red") # 객체 이름 텍스트로 그리기

    
    # save and modified image
    parts = image_path.rsplit('.',1)

    if len(parts) ==2:
        output_path = f"{parts[0]}_annotated.{parts[1]}"
    else:
        output_path = f"{image_path}_annotated"

    image.save(output_path) # 이미지 저장
    print(f"Annotated image saved to {output_path}")
    image.show() # 이미지 보여주기

def main():
    image_path = input("Enter the path to the image file: ")

    print("1. Analyzing image.")
    print("2. Detecting objects in image.")
    choice = input("Choose an option (1 or 2): ")

    if choice == '1':
        print("Analysis Result: ")
        result = analyze_image(image_path)        
    elif choice == '2':
        print("Object Detection Result: ")
        result = object_detection(image_path)
        if result:
            create_bounding_box(image_path, result)
        else:
            print("No objects detected or an error occurred.")
            return
    else:   
        print("Invalid choice. Please select 1 or 2.")
        return
    
    if result:
        print(result)

if __name__ == "__main__" :
    main()