# reading-keeper
## What is it
ReAding KEeper (RAKE) is a reading assistant. 
It is made of a Raspberry Pi and a Camera attached to a reading lamp.

## How it works
The camera is filming the book you read and feeds the video to the Raspberry.

We then use Mediapipe's Hands to detect hands and recognize hand gestures with a Tensorflow model.

## What should it do
  - Take a screenshot of an interesting passage in the book when you want it

- The current gesture to take a photo is the following :
    
![2021-12-20-135159](https://user-images.githubusercontent.com/39133219/146770459-585ea224-f36c-474c-a5f1-ac0ba1aa2fb4.jpg)
    
IMPORTANT : It should be done with the LEFT hand. 
    
The gesture is not recognized on the right hand in order to  minimize the risks of taking a capture when turning a page with your right hand.
    


- Detect when you turn a page to do statistics on your reading like speed.

## What has been done

- [x] Take a screenshot gesture
  - Take a screenshot OK
  - Take a screenshot only of the zone of interest NOT OK
- [ ] Detect page turning
- [x] Setup Raspberry camera
- [x] Deploy code on raspberry
- [x] Attach camera to lamp
- [x] Compile data into a mobile app

## How to run it

The project runs with **Python 3.7 ONLY**

1. (Optional) Setup a Python virtual environment

```bash
python3 -m venv ./venv
source venv/bin/activate
```

2. Install required packages

``` 
pip install --upgrade pip
pip install mediapipe opencv-python tensorflow
```

3. Run the app (main.py)

``` 
python main.py
```

