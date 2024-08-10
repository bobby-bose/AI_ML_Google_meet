import cv2
from django.http import JsonResponse
from django.shortcuts import render,redirect
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def detect_eyes(request):
    if request.method == 'POST':
        # Open the default camera (usually the first camera available)
        cap = cv2.VideoCapture(0)

        # Check if the camera is opened successfully
        if not cap.isOpened():
            return JsonResponse({'status': 'error', 'message': 'Failed to open camera.'}, status=500)

        while True:
            # Read a frame from the camera
            ret, frame = cap.read()

            # Convert the frame to grayscale for eye detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect eyes
            eyes = eye_cascade.detectMultiScale(gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(frame, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

            # Display the frame with eye detection
            cv2.imshow('Eye Detection', frame)
            key = cv2.waitKey(1)
            if key == 27:
                break

        # Release the camera and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

        return JsonResponse({'status': 'success', 'message': 'Eye detection window closed.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
    


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(request):
    if request.method == 'POST':
        # Open the default camera (usually the first camera available)
        cap = cv2.VideoCapture(0)

        # Check if the camera is opened successfully
        if not cap.isOpened():
            return JsonResponse({'status': 'error', 'message': 'Failed to open camera.'}, status=500)

        while True:
            # Read a frame from the camera
            ret, frame = cap.read()

            # Convert the frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Display the frame with face detection
            cv2.imshow('Face Detection', frame)
            key = cv2.waitKey(1)
            if key == 27:
                break

        # Release the camera and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

        return JsonResponse({'status': 'success', 'message': 'Face detection window closed.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
 
    
def index(request):
    return render(request,"index.html")




from django.http import JsonResponse
import speech_recognition as sr
from django.shortcuts import render
from django.http import JsonResponse
import speech_recognition as sr

def voice_detection(request):
    if request.method == 'POST':
        try:
            # Initialize recognizer
            recognizer = sr.Recognizer()

            # Use default microphone as source
            with sr.Microphone() as source:
                print("Speak something...")
                # Adjust ambient noise for better recognition
                recognizer.adjust_for_ambient_noise(source)

                # Listen to microphone input
                audio = recognizer.listen(source)

            print("Recognizing...")
            # Use Google Web Speech API for speech recognition
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            
            # Render results.html template with recognized text
            return render(request, 'results.html', {'text': text})
        except sr.UnknownValueError:
            return JsonResponse({'status': 'error', 'message': 'Sorry, could not understand audio.'}, status=400)
        except sr.RequestError as e:
            return JsonResponse({'status': 'error', 'message': f'Error fetching results: {e}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)




from django.shortcuts import render
from django.http import HttpResponse
def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    elif request.method == 'POST':
        try:
            recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                print("Speak something...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print("You said:", text)

            # Redirect to the results page with the recognized text as a parameter
            return redirect('results', text=text)
        except sr.UnknownValueError:
            return JsonResponse({'status': 'error', 'message': 'Sorry, could not understand audio.'}, status=400)
        except sr.RequestError as e:
            return JsonResponse({'status': 'error', 'message': f'Error fetching results: {e}'}, status=500)
def results(request, text):
    return render(request, 'results.html', {'text': text})


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def camera(request):
    if request.method == 'POST':
        camera_state = request.POST.get('camera')
        if camera_state == 'true':
            # Code to handle camera ON state
            print('Camera is now ON')

            # Open camera capture stream
            cap = cv2.VideoCapture(0)

            # Check if the camera is opened successfully
            if not cap.isOpened():
                return JsonResponse({'status': 'error', 'message': 'Failed to open camera.'}, status=500)

            while True:
                # Read a frame from the camera
                ret, frame = cap.read()

                # Convert the frame to grayscale for face and eye detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect faces
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                    # Extract the region of interest (ROI) for eye detection
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = frame[y:y+h, x:x+w]

                    # Detect eyes within the face ROI
                    eyes = eye_cascade.detectMultiScale(roi_gray)
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

                # Display the frame with face and eye detection
                cv2.imshow('Camera Stream', frame)
                key = cv2.waitKey(1)
                if key == 27:
                    break

            # Release the camera and close all OpenCV windows
            cap.release()
            cv2.destroyAllWindows()
        else:
            # Code to handle camera OFF state
            print('Camera is now OFF')

        return JsonResponse({'message': 'Camera state received'}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
def schedule_meeting(request):
    return render(request, 'schedule_meeting.html')

