SWEET BACKEND PROJECT

Utilizes Flask to easily create API routes and handle URL requests in Python.

How to Run:
Install Flask through this command:
 python -m pip install -r requirements.txt

Run using this command:
python main.py

To call API endpoints:

Generate a shorten URL using this command in Powershell:
- Invoke-RestMethod ` -Uri "http://127.0.0.1:5000/shorten" ` -Method POST ` -ContentType "application/json" ` -Body '{"url":"input_url"}'

Get visiting stats for the link using this command:
- Replace the code with the one given by API when calling previous command
Invoke-RestMethod "http://127.0.0.1:5000/input_random_code/stats"