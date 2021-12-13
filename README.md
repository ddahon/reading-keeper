# reading-keeper
## What is it
ReAding KEeper (RAKE) is a reading assistant. 
It is made of a Raspberry Pi and a Camera attached to a reading lamp.

## How it works
The camera is filming the book you read and feeds the video to the Raspberry.

We then use Mediapipe's Hands to detect hands and recognize hands gestures.

## What should it do
  - Take a screenshot of an interesting passage in the book when you want it
  - Detect when you turn a page to do statistics on your reading like speed.

## What has been done

- [x] Take a screenshot gesture
- [ ] Detect page turning
- [ ] Setup Raspberry camera
- [ ] Deploy code on raspberry
- [ ] Attach camera to lamp
- [ ] Compile data into a mobile app

## How to run it

1. (Optional) Setup a Python virtual environment

```bash
python3 -m venv ./venv
source venv/bin/activate
```

2. Install required packages

``` 
pip install mediapipe opencv-python tensorflow
```

3. Run the app

``` 
python main.py
```

