# easy-simple-email-reporting

easy-simple-email-reporting.py is a tool that helps you create simple, easy-to-read reports for email phishing events and incidents. You provide the tool with an .eml file, and it extracts relevant information from the email from a reporting perspective. It then generates a report template and saves it using the naming convention report-filename.eml.txt.

The generated report can be further expanded with additional details, such as a description of the overall situation, investigation findings, or actions taken during the incident response process.

### Usage
``` python3 easy-simple-email-reporting.py <eml_file_path> ```

Example:
```
$ python3 easy-simple-email-reporting.py sample1.eml
$ cat report-sample1.eml.txt
Headers
======================================
Date: 14 Jan 2020 00:06:05 -0800
Subject: FW: Due Invoice Payment - protonmail.com - Wire Transfer Document

To: wpx@protonmail.com
From: Paolo Reggiani <Paol.Reggiani@moss.it>

Reply-To: 
Return-Path: <Paol.Reggiani@moss.it>

Sender IP: 
Resolve Host: 

Message-ID: 


URLs
======================================
http://www[.]w3[.]org/TR/html4/loose[.]dtd


Attachments
======================================
Attachment Name: quotation.iso
MD5: 6aef1d7f88e8aa450a0c604b4caee5ba
SHA1: 3fe45f8cd20cd7c63e55e3918dac1d3a0d7fb05a
SHA256: 75fdb848eac332b4ca7d88f497e7ba7ebbb9a798d825b28cf1f87b9d7149e87f


Description
======================================



Artifact Analysis
======================================
Sender Analysis:


URL Analysis:


Attachment Analysis:



Verdict
======================================



Defense Actions
======================================
```
