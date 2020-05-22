from subprocess import check_output


# download requirements.txt
check_output(["pip", "install", "-r", "requirements.txt"])

# download driver
check_output(["curl", "-O", "https://chromedriver.storage.googleapis.com/81.0.4044.138/chromedriver_mac64.zip"])
check_output(["unzip", "chromedriver_mac64.zip"])

# download distributions.obj
check_output(["curl", "-O", "https://github.com/nreimers/truecaser/releases/download/v1.0/english_distributions.obj.zip"])
check_output(["unzip", "english_distributions.obj.zip"])

