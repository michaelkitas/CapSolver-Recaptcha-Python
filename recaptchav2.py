import capsolver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize capsolver with your API key
capsolver.api_key = "CAP-XXX"

# Solve the reCAPTCHA using capsolver
solution = capsolver.solve({
    "type": "ReCaptchaV2TaskProxyLess",  # Required. This should be 'ReCaptchaV2Task' if using proxies or 'ReCaptchaV2TaskProxyLess' if not.
    "websiteKey": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",  # Required. This is the domain's public key, often called the 'site key.'
    "websiteURL": "https://www.google.com/recaptcha/api2/demo",  # Required. The URL of the page where the reCaptcha is located.
    
    # Optional Parameters:
    # "proxy": "http://user:password@123.123.123.123:8080",  # Optional. Required only if using 'ReCaptchaV2Task' instead of 'ReCaptchaV2TaskProxyLess'. Include your proxy in the format 'http://user:password@host:port'.
    # "isInvisible": False,  # Optional. Set this to True if the reCaptcha is invisible and doesn't have a 'pageAction'. Default is False.
    # "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",  # Optional. Include the User-Agent string if you need to emulate a specific browser.
    # "cookies": "name=value; name2=value2",  # Optional. Include cookies if necessary for solving the captcha, formatted as 'name=value; name2=value2
})

print("CAPSolver Solution:", solution)

# Extract the CAPTCHA token from the solution
token = solution.get('gRecaptchaResponse')

if not token:
    print("Failed to get CAPTCHA token from capsolver.")
    exit()

# Set up Selenium WebDriver (you may need to specify the path to your chromedriver)
driver = webdriver.Chrome()

try:
    # Navigate to the target website
    driver.get("https://www.google.com/recaptcha/api2/demo")

    # Wait for the reCAPTCHA to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "g-recaptcha"))
    )

    # Inject the CAPTCHA token into the page
    driver.execute_script("""
    document.getElementById('g-recaptcha-response').style.display = 'block';
    document.getElementById('g-recaptcha-response').value = arguments[0];
    """, token)

    # Submit the form
    submit_button = driver.find_element(By.ID, "recaptcha-demo-submit")
    submit_button.click()

    # Wait for the result page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".recaptcha-success"))
    )

    # Print the result
    result = driver.find_element(By.CSS_SELECTOR, ".recaptcha-success").text
    print("Result:", result)

finally:
    # Close the browser
    driver.quit()
