from flask import Flask, request, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

app = Flask(__name__)

form_html = '''
<form method="post">
  Facebook की पूरी कुकीज़ एक साथ पेस्ट करें:<br>
  <textarea name="cookies" rows="6" cols="60" required></textarea><br><br>
  
  Thread ID:<br>
  <input name="thread_id" type="text" required><br><br>
  
  आपका नाम:<br>
  <input name="name" type="text" required><br><br>
  
  मैसेज भेजने का समयांतराल (सेकंड में):<br>
  <input name="interval" type="number" value="10" required><br><br>
  
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

        send_facebook_messages(cookies_str, thread_id, name, interval)
        return "बोट कुकीज़ के साथ शुरू हो गया है! टर्मिनल या लॉग देखें।"
    return render_template_string(form_html)

def send_facebook_messages(cookies_str, thread_id, name, interval):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Browser GUI नहीं देखना हो तो नीचे वाली लाइन अनकमेंट करें
    # options.add_argument("--headless")

    # Chrome Driver इनिशियलाइजेशन
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://facebook.com")
    time.sleep(3)

    for cookie in parse_cookies(cookies_str):
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print("Cookie सेट करते समय Error:", e)

    driver.refresh()
    time.sleep(5)

    print(f"{name} के लिए थ्रेड {thread_id} पर हर {interval} सेकंड मेसेज भेजने को तैयार।")

    # यहाँ मैसेजिंग लॉजिक डालें

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
