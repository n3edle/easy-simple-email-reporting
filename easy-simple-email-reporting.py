import re
import sys
import hashlib
import email
import os
from email.parser import BytesParser

def read_file(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    parser = email.parser.BytesParser()
    msg = parser.parsebytes(content)
    return msg

def extract_headers(email_message):
    headers_to_extract = [
        "Date",
        "Subject",
        "To",
        "From",
        "Reply-To",
        "Return-Path",
        "Message-ID",
        "X-Originating-IP",
        "X-Sender-IP",
        "Authentication-Results"
    ]
    headers = {}
    for key in email_message.keys():
        if key in headers_to_extract:
            headers[key] = email_message[key]
    return headers

def defang_url(url):
    url = url.replace('https://', 'hxxps[://]')
    url = url.replace('.', '[.]')
    return url

def extract_attachments(email_message):
    attachments = []
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if filename:
            attachments.append({
                'filename': filename,
                'md5': hashlib.md5(part.get_payload(decode=True)).hexdigest(),
                'sha1': hashlib.sha1(part.get_payload(decode=True)).hexdigest(),
                'sha256': hashlib.sha256(part.get_payload(decode=True)).hexdigest()
            })
    return attachments

def extract_urls(email_message):
    urls = set()
    for part in email_message.walk():
        content_type = part.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            payload = part.get_payload(decode=True)
            if isinstance(payload, bytes):
                payload = payload.decode('utf-8', errors='ignore')
            urls.update(re.findall(r'https?:\/\/(?:[\w\-]+\.)+[a-z]{2,}(?:\/[\w\-\.\/?%&=]*)?', payload))
    return list(urls)

def main(file_path):
    email_message = read_file(file_path)

    Date = ""
    Subject = ""
    To = ""
    From = ""
    ReplyTo = ""
    ReturnPath = ""
    SenderIP = ""
    ResolveHost = ""
    MessageID = ""

    headers = extract_headers(email_message)
    urls = extract_urls(email_message)
    attachments = extract_attachments(email_message)
    for key, value in headers.items():
        if key == "Date":
            Date = value
        elif key == "Subject":
            Subject = value
        elif key == "To":
            To = value
        elif key == "From":
            From = value
        elif key == "Reply-To":
            ReplyTo = value
        elif key == "Return-Path":
            ReturnPath = value
        elif key == "Sender IP":
            SenderIP = value
        elif key == "ResolveHost":
            ResolveHost = value
        elif key == "MessageID":
            MessageID = value
        else:
            continue
    filename = "report-" + file_name + ".txt"

    with open(filename, "w") as f:
        print("""\nHeaders
======================================
Date: """+Date+"""
Subject: """+Subject+"""

To: """+To+"""
From: """+From+"""

Reply-To: """+ReplyTo+"""
Return-Path: """+ReturnPath+"""

Sender IP: """+SenderIP+"""
Resolve Host: """+ResolveHost+"""

Message-ID: """+MessageID+"""


URLs
======================================""", file=f)
        for url in urls:
            print(defang_url(url), file=f)
        print("""

Attachments
======================================""", file=f)
        for attachment in attachments:
            print(f"Attachment Name: {attachment['filename']}", file=f)
            print(f"MD5: {attachment['md5']}", file=f)
            print(f"SHA1: {attachment['sha1']}", file=f)
            print(f"SHA256: {attachment['sha256']}", file=f)
        print("""

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
======================================""", file=f)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <email_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    file_name = os.path.basename(file_path)
    main(file_path)