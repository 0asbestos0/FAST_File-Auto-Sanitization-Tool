# File Auto Sanitization Tool

Simple overview of use/purpose.

## Description

Max Automated analysis of various Files (Different files added with time).
File Types Supported:
1. OLE files (.doc .xls .ppt)
2. PDF files (.pdf)
3. Image files (.jpg/.jpeg .png)
4. OOXML files (.docx .xlsx .pptx)

## Getting Started

### Dependencies

1. Windows system (Tested on Windows 10)
2. Python and pip installed (Tested on python 3.10 and above)
3. VCRUNTIME140.dll must be present (Download and install from official miscrosoft website at: https://aka.ms/vs/16/release/vc_redist.x64.exe)

### Installing

To install the tool, use the following commands:

```shell
git clone https://github.com/0asbestos0/FAST_File-Auto-Sanitization-Tool.git
```
or
Download Zip file and unzip it.
********************************************************
********************************************************
CAUTION: THIS REPOSITORY CONTAINS A FEW MALWARE SAMPLES IN THE "Test" DIRECTORY WHICH IS EASILY FLAGGED BY ANY AV SOFTWARE.
********************************************************
********************************************************
Then,
```shell
cd FAST_File-Auto-Sanitization-Tool-main
pip install -r requirements.txt
```

Now you can do a demo run of the tool.
```shell 
The "Test" Directory will contains default samples for testing purposes.
```

### Executing program

Use the following basic commands to get started with the tool:
```shell
cd FAST_File-Auto-Sanitization-Tool-main
python maintool.py -h
```
This command will show the help for tool.
```shell
python maintool.py -f "Absolute_path_to_a_file" --manual --report
```
or,
```shell
python maintool.py -d "Absolute_path_to_a_directory" --report
```
## Disclaimer
This project contains code from some other's repositories like by Didier Stevens and YARA. Kindly note that since this project is in development, these dependencies on other's repositories will be eliminated with due course of time.
