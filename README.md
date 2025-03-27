# fuel-siphonage-detector

- Name: Nicky Chepteck Chemos
- Email: nickyhemos@gmail.com
- Phone Number: 0700517934

# Task Description
The aim of this project is to build a Python pipeline to detect fuel siphonage events based on telemetry logs. Siphonage is defined as a *significant drop* in fuel level while *the vehicle engine is off* and *the vehicle is stationary*.

# How to install and run the code locally

*Prerequisites*
a) Python 3.7+ installed on your system.
b) A command-line interface (Terminal on macOS/Linux or Command Prompt/PowerShell on Windows).

*Steps to take*
1. Clone the Repository
Open windows powershell and cd to your preferred project location
- eg. Desktop--> 'cd Desktop'
Once in the Desktop, clone the repository using:
- git clone https://github.com/Nickychemos/fuel-siphonage-detector.git
You can now open the project in your local computer using a code editor such as VS Code

2. Once in your code editor, open a new terminal and set up a virtual environment and activate it using
- python -m venv env
- env\Scripts\activate

3. Install Dependencies
Ensure that you have pip updated, then install the required packages using the provided requirements.txt file:
- pip install --upgrade pip
- pip install -r requirements.txt
These are the specific files: pandas, streamlit, geopy, pytest, numpy

4. Run the Streamlit UI
The main application file is main.py. To start the Streamlit app, run:
- streamlit run app/main.py
- This will open your default web browser where you can interact with the Fuel Siphonage Detection System. You will be able to:
  1. Upload CSV or Excel files containing vehicle telemetry data.
  2.  See a preview of the uploaded data (first 5 rows).
  3. View detected siphonage events based on the rule-based logic after uploading a file.
  4. Download the processed results.

5. Testing the Code
- To ensure that the detection logic works as expected, you can run the unit tests located in the test_detector.py file on your terminal using: *pytest test_detector.py*
- This will run basic test cases to validate the rule-based detection in detector.py
- If an output of 100% is acheved, it means that all test cases collected passed successfully.

6. Example Output
- When you run the Streamlit UI and upload a properly formatted *CSV* file, you might see such an output:
![image](https://github.com/user-attachments/assets/6959ab4a-d69c-4e1b-830f-d62895e06471)

- Here, only the rows where siphonage is detected will be shown as seen in the siponage column where all outputs are 'Yes'

7. Project Files Overview
- *app.py*:
The Streamlit app that provides a UI for data upload, processing, and result display.
- *detector.py*:
Contains the logic to calculate fuel drop percentage, check if the engine is off, verify minimal location change (using geopy), and flag siphonage rows.
- *utils.py*:
Provides utility functions, including data preprocessing and encoding (e.g., converting engine status to a numeric flag).
- *test_detector.py*:
Unit tests to validate the detection logic using pytest.
- *requirements.txt*:
Lists all external dependencies needed for the project.
- *Fuel_Siphonage_Detection_Task.ipynb*
Notebook containing the Exploratory Data Analysis and Visualization done as well as the initial creation of the siphonage column as a guide
