from flask import Flask, request, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

app = Flask(__name__)

form_html = '''
<form method="post" enctype="multipart/form-data">
  Facebook Cookies (एक साथ पेस्ट करें):<br>
  <textarea name="cookies" rows="6" cols="60" required></textarea><br><br>
  
  Thread ID:<br>
  <input name="thread_id" type="text" required><br><br>
  
  आपका नाम:<br>
  <input name="name" type="text" required><br><br>
  
  Message भेजने का समयांतराल (सेकंड में):<br>
  <input name="interval" type="number" value="10" required><br><br>
  
  Message फाइल चुनें (एक लाइन = एक मैसेज):<br>
  <input type="file" name="msgfile"><br><br>
  
  <input type="submit" value="Run करें">
</form>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cookies_str = request.form['cookies']
        thread_id = request.form['thread_id']
        name = request.form['name']
        interval = int(request.form['interval'])
        msgfile = request.files.get('msgfile')

        messages = []
        if msgfile:
            messages = msgfile.read().decode('utf-8').splitlines()

        run_facebook_bot(cookies_str, thread_id, name, interval, messages)
        return f"Bot चल रहा है। {len(messages)} मैसेज फाइल से लिए गए। टर्मिनल देखें।"
    return render_template_string(form_html)

def run_facebook_bot(cookies_str, thread_id, name, interval, messages):
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://facebook.com")
    time.sleep(3)

    # Add cookies from the string
    for cookie in parse_cookies(cookies_str):
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"Cookie setting error: {e}")

    driver.refresh()
    time.sleep(5)

    print(f"Logged in with cookies. Ready to send {len(messages)} messages to thread {thread_id} from {name} every {interval} seconds.")

    # Example: Loop through messages and print (instead of sending)
    for msg in messages:
        print(f"Sending message: {msg}")
        # Selenium logic to send message goes here
        time.sleep(interval)

    driver.quit()

def parse_cookies(cookies_str):
    cookies = []
    for part in cookies_str.split(';'):
        if '=' in part:
            name, value = part.strip().split('=', 1)
            cookies.append({'name': name, 'value': value, 'domain': '.facebook.com'})
    return cookies

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
