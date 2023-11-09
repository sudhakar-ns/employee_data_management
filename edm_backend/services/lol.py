import time, subprocess
from services.web_automation import WebAutomation
from config import *


def is_website_up(website_url: str) -> bool:
    try:
        # For Windows
        response = subprocess.run(["ping", "-n", "1", website_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # For Linux/Mac, uncomment the line below and comment the above line
        # response = subprocess.run(["ping", "-c", "1", website_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return response.returncode == 1  # Return code 0 indicates a successful ping (website is up)
    except Exception as e:
        print(e)
        return False  # Exception occurred, website is considered down


def perform_web_automation() -> str:
    try:
        bot = WebAutomation()
        bot.set_creds(user_name=USER_NAME, password=PASSWORD, login_page=WEBSITE_LOGIN_PAGE, download_url=REDIRECT_DOWNLOAD_PAGE)
        bot.set_chrome_options()
        bot.set_experimental_option()
        bot.google_bot()
        return 'Success'
    except Exception as err:
        print(err)


def poc() -> (str or None):
    # website_url = "https://st.humana.com/"  # Replace with your website URL
    website_url = "https://www.google.com/" 
    max_retries = 5
    retry_interval_seconds = 60
    response = None
    for retry_count in range(1, max_retries + 1):
        print(f"Retry attempt #{retry_count}")

        if is_website_up(website_url):
            try:
                # Perform web automation
                response = perform_web_automation()
                break
            except Exception as e:
                print(f"Error during web automation: {str(e)}")
        else:
            print(f"Website is down. Waiting for {retry_interval_seconds} seconds before retrying...")

        if retry_count < max_retries:
            time.sleep(retry_interval_seconds)
        else:
            print("Maximum retries reached. Exiting.")
            
        # Upload the downloaded file to S3
        # upload_to_s3('local-file-path', 'your-s3-bucket', 's3-key-for-file')
        print("Checked")
    return response