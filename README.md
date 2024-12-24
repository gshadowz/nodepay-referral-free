# Nodepay Referral Free (Termux only)
![nodepay-banner](img/nodepay.png)


# [Register Nodepay Here](https://app.nodepay.ai/register?ref=1XsOOpCNsHejnuP)

# Good Proxy for Nodepay
- [Cherry Proxy](https://center.cherryproxy.com/Login/Register?invite=gshadowz)
- [922 Proxy](https://www.922proxy.com/register?inviter_code=gshadowz)
- [ABC Proxy](https://www.abcproxy.com/?code=605NOU06)

# Features
- Get Token for Existing Nodepay Account
- Fail Safe Mechanisnm, Put Failed Account Credential into File
- Saving Credential and Token into different file
- Better Logging Color

# Requirements
- Git
    ```bash
    pkg install git
    ```

- Python
    ```bash
    pkg install python
    ```

# How to Use
- Clone this Repository and change directory
    ```bash
    git clone https://github.com/gshadowz/nodepay-referral-free.git
    cd nodepay-referral-free
    ```

- Install the requirements
    ```bash
    pip install -r requirements.txt
    ```

- Copy and Paste the JS Script in [Important Step](#important-step) to the [Via Browser](https://www.viayoo.com/en/)
    
- Open Via Browser, go to [Nodepay Login](https://app.nodepay.ai/login) And Run Captcha Solver for get captcha token

- Then in the Termux, run
    ```
    python app.py
    ```

- After that open new session in Termux and run the main script. get-token is for getting nodepay token and auto-referral for auto referral using your referral code.
    ```bash
    python get-token.py
    ```
    or
    ```bash
    python auto-referral.py
    ```

- Wait until complete and enjoy your free auto referral.

### **Note: For tutorial using video, you can visit this [youtube video](https://www.youtube.com/watch?v=4rVVzquI-pU)**

# Important Step
### Captcha Solver JavaScript / use via 

```javascript

// ==UserScript==
// @name         Captcha Token Fetcher, Subscribe YouTube : @nbprg
// @namespace    https://viayoo.com/
// @version      1.0
// @description  Fetch Captcha token, reload page, wait for 5 seconds, and run for 10000 times
// @author       Saifur Rahman Siam / Telegram : @TataCuto
// @match        https://app.nodepay.ai/login
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {
    'use strict';
    let counter = 0;
    const maxIterations = 10000;  // Set maximum iterations to 10000
    let retryCounter = 0;
    const maxRetries = 8;  // Set maximum retries to 5
    // Function to simulate click on the CAPTCHA checkbox
    function clickCaptchaCheckbox() {
        const captchaCheckbox = document.querySelector('input[name="cf-turnstile-response"]');
        if (captchaCheckbox) {
            console.log('Clicking CAPTCHA checkbox...');
            captchaCheckbox.click();
        } else {
            console.log('CAPTCHA checkbox not found.');
        }
    }
    // Function to check for CAPTCHA token and make request
    function checkCaptchaToken() {
        const captchaInput = document.querySelector('input[name="cf-turnstile-response"]');
        if (captchaInput && captchaInput.value) {
            const captchaValue = captchaInput.value;
            console.log('CAPTCHA token fetched:', captchaValue);
            const url = `http://localhost:5000/post?token=${captchaValue}`;
            GM_xmlhttpRequest({
                method: "GET",
                url: url,
                onload: function(response) {
                    console.log('Response from server:', response.responseText);
                },
                onerror: function(error) {
                    console.error('Error fetching server response:', error);
                }
            });
            // Increment the counter
            counter++;
            retryCounter = 0;  // Reset retry counter after a successful fetch
            // Check if the process should stop after 10000 iterations
            if (counter < maxIterations) {
                console.log(`Iteration ${counter} completed.`);
                // Wait for 10 seconds, then reload the page
                setTimeout(() => {
                    location.reload();  // Reload the page
                }, 2000); // 10-second delay before reload
            } else {
                console.log('Completed 10000 iterations, stopping.');
            }
        } else {
            retryCounter++;
            if (retryCounter < maxRetries) {
                console.log(`CAPTCHA token not yet available, retrying... (Attempt ${retryCounter} of ${maxRetries})`);
                clickCaptchaCheckbox();  // Click the CAPTCHA checkbox if available
                setTimeout(checkCaptchaToken, 1000);  // Retry after 1 second if CAPTCHA is not available
            } else {
                console.log(`Failed to fetch CAPTCHA token after ${maxRetries} attempts, reloading page.`);
                location.reload();  // Reload the page if maximum retries reached
            }
        }
    }
    // Start the process by calling checkCaptchaToken
    checkCaptchaToken();
})();

```

# Source 
https://github.com/nbprg/nodepay-referral