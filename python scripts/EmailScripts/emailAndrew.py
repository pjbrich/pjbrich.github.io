import os
from urllib.parse import quote

recipient = "andrew.niemczyk@exlterra.com"
subject = "Automated Email from Python"
body = "Hello Andrew,\n\nThis is an automated email sent using Python and Thunderbird.\n\nBest regards,\nPython Script"

# Encode the subject and body for use in the command
encoded_subject = quote(subject)
encoded_body = quote(body)

# Construct the Thunderbird command
command = f'thunderbird -compose "to=\'{recipient}\',subject=\'{encoded_subject}\',body=\'{encoded_body}\'"'

# Execute the command
os.system(command)
