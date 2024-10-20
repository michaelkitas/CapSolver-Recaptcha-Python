import capsolver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize capsolver with your API key
capsolver.api_key = "CAP-XXX"

# Solve the reCAPTCHA using capsolver
solution = capsolver.solve({
    "type": "ReCaptchaV3TaskProxyLess",  # Required. This should be 'ReCaptchaV3Task' if using proxies or 'ReCaptchaV3TaskProxyLess' if not.
    "websiteKey": "6LdKlZEpAAAAAAOQjzC2v_d36tWxCl6dWsozdSy9",  # Required. This is the domain's public key, often called the 'site key.'
    "websiteURL": "https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php",  # Required. The URL of the page where the reCaptcha is located.
    "pageAction": "homepage" # Required. The action parameter for reCaptcha v3.

    # Optional Parameters:
    # "proxy": "http://user:password@123.123.123.123:8080",  # Optional. Required only if using 'ReCaptchaV2Task' instead of 'ReCaptchaV2TaskProxyLess'. Include your proxy in the format 'http://user:password@host:port'.

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
    driver.get("https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php")

    # Wait for the reCAPTCHA to load
    # Wait until 'window.verifyRecaptcha' is defined
    # WebDriverWait(driver, 30).until(
    #     lambda d: d.execute_script("return typeof window.verifyRecaptcha === 'function';")
    # )

    # Inject the CAPTCHA token into the page
    # driver.execute_script(f"window.verifyRecaptcha('{token}')")

    # Wait for the reCAPTCHA to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "g-recaptcha-response-100000"))
    )

    # Inject the CAPTCHA token into the page
    driver.execute_script("""
    document.getElementById('g-recaptcha-response-100000').style.display = 'block';
    document.getElementById('g-recaptcha-response-100000').style.visibility = 'visible';
    document.getElementById('g-recaptcha-response-100000').value = arguments[0];
    """, token)

    # Wait until the result text is present in the response element
    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.CSS_SELECTOR, ".response").text.strip() != ""
    )

    # Print the result
    result = driver.find_element(By.CSS_SELECTOR, ".response").text
    print("Result:", result)

finally:
    # Close the browser
    driver.quit()
