from flask import Flask, request, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

html_form = '''
<form method="post">
  Facebook की पूरी Cookies यहाँ पेस्ट करें:<br>
  <textarea name="cookies" rows="6" cols="60" required></textarea><br><br>
  
  Thread ID:<br>
  <input name="thread_id" type="text" required><br><br>
  
  आपका नाम:<br>
  <input name="name" type="text" required><br><br>
  
  Message भेजने का अंतराल (सेकंड में):<br>
  <input name="interval" type="number" value="10" required><br><br>
  
  <input type="submit" value="रन करें">
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
        return "बॉट कूकीज़ के साथ शुरू हो गया है! टर्मिनल देखें।"
    return render_template_string(html_form)

def send_facebook_messages(cookies_str, thread_id, name, interval):
    options = webdriver.ChromeOptions()
    # UI दिखाना चाहते हैं तो नीचे वाली लाइन हटा दें
    # options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get("https://facebook.com")
    time.sleep(3)

    for cookie in parse_cookies(cookies_str):
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print("Cookie सेट में त्रुटि:", e)
    
    driver.refresh()
    time.sleep(5)

    print(f"{name} के लिए थ्रेड {thread_id} पर हर {interval} सेकंड में मैसेज भेजने के लिए लॉगिन हो गया।")

    # यहां अपने Selenium लॉजिक से मैसेज भेजने का कोड डालें

    # Demo के लिए बंद कर रहे हैं, आप बाद में अपनी जरूरत के अनुसार हैंडल करें
    driver.quit()

def parse_cookies(cookies_str):
    cookies = []
    for part in cookies_str.split(';'):
        if '=' in part:
            name, value = part.strip().split('=', 1)
            cookies.append({'name': name, 'value': value, 'domain': '.facebook.com'})
    return cookies

if __name__ == "__main__":
    app.run(debug=True)
