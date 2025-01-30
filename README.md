# ReCAPTCHASolver: Automate reCAPTCHA Audio Challenges with Python  

ReCAPTCHASolver is a Python package that automates the process of solving Google's reCAPTCHA using audio challenges. It utilizes Selenium for web automation, requests for downloading audio files, and Google Speech Recognition for transcription.  

## Features  
- Automates solving of Google reCAPTCHA challenges
- Uses speech-to-text to decode audio challenges
- Handles reCAPTCHA v2 (audio challenges)
- Verifies the installation of FFmpeg and configures it automatically
- Works with Selenium and requires the driver with the reCAPTCHA iframe to be provided



## Demo  
![ReCAPTCHA Solver in Action](https://github.com/lucassoares-eng/my_website/blob/main/app/static/recaptcha-solver.gif?raw=true)


## Installation  
```bash
pip install recaptchav2solver
```

## Usage
```python
from selenium import webdriver
from recaptchav2solver import ReCAPTCHASolver

# Selenium driver setup
driver = webdriver.Chrome()  # or webdriver.Firefox(), depending on the browser you use

# Access the URL containing the reCAPTCHA
url = 'https://example.com'
driver.get(url)

# Solve the reCAPTCHA
solver = ReCAPTCHASolver()
solver.solve_recaptcha(driver)
```

### Notes
To use the solve_recaptcha function, make sure to send the driver (Selenium WebDriver instance) in which the reCAPTCHA iframe is present.

## Dependencies

```plaintext
requests==2.31.0
selenium==4.27.1
speechrecognition==3.14.0
pydub==0.25.1
```
