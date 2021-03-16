import oauth
import os

def main():
    print("hello world.")
    print(os.getcwd() + "..\credential\credentials.json")
    oauth.test()


if __name__ == "__main__":
    main()
