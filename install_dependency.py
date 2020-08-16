import os

os.system(
    f"pip install git+https://{os.environ['username']}:{os.environ['secrets_token']}@github.com/callistoteam/iamschool.git"
)
