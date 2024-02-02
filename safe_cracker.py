import os
import random
import threading
import time

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class Result:
    def __init__(self, username, user_code, result, passed):
        self.username = username
        self.user_code = user_code
        self.result = result
        self.passed = passed


# Create dictionary with username as key and result as value
attempted_users = {}
passed_users = {}
flagged_for_deletion_paths = []
notations = {
    "O(1)": 0.1,
    "O(log n)": 0.5,
    "O(n)": 1,
    "O(n log n)": 5,
    "O(n^2)": 10,
    "O(2^n)": 15,
    "O(n!)": 20,
    "O(n^n)": 25,
    "O(n^n^n)": 30
}


def big_o_notation_time_thresholds(seed):
    random.seed(seed)
    return random.choice(list(notations.values()))


def evaluate_code_threaded(username, user_code, time_threshold):
    # Sanitize user code
    user_code = user_code.replace("import", "# import")
    user_code = user_code.replace("print", "# print")
    user_code = user_code.replace("input", "# input")
    user_code = user_code.replace("open", "# open")
    user_code = user_code.replace("exec", "# exec")
    user_code = user_code.replace("eval", "# eval")
    user_code = user_code.replace("os", "# os")
    user_code = user_code.replace("sys", "# sys")
    user_code = user_code.replace("subprocess", "# subprocess")
    user_code = user_code.replace("shutil", "# shutil")
    user_code = user_code.replace("tempfile", "# tempfile")
    user_code = user_code.replace("input", "# input")

    # Add more replacements as needed

    # Function to run user code
    def run_user_code():
        try:
            start_time = time.time()
            exec(user_code)
            elapsed_time = time.time() - start_time
            if time_threshold - 0.1 <= elapsed_time <= time_threshold + 0.1:
                attempted_users[username] = Result(username, user_code, f"Passed with {elapsed_time}, needed {time_threshold}", True)
            else:
                attempted_users[username] = Result(username, user_code, f"Time requirement not met. Expected: {time_threshold}, Got: {elapsed_time}", False)
        except Exception as e:
            return f"Error executing code: {e}"

    # Run user code in a separate thread with timeout
    thread = threading.Thread(target=run_user_code)
    thread.start()
    thread.join(time_threshold)


def check_attempts():
    print("Checking attempts...")
    flagged_for_user_deletion = []
    for user in attempted_users:
        print(f"Checking {user}")
        result = attempted_users[user]
        if result.passed:
            passed_dir = f"./lock_files/passed/{user}_latest_passed.py"
            print(f"{user} passed with {result.result}")
            # Override the file in the passed folder, or create a new one if it doesn't exist
            with open(passed_dir, "w") as file:
                file.write(result.user_code)
                file.close()
            passed_users[user] = result
        else:
            attempt_dir = f"./lock_files/attempts/{user}_latest_attempt.py"
            print(f"{user} didn't crack the safe, result: {result.result}")
            # Move the file to the attempts folder
            with open(attempt_dir, "w") as file:
                file.write(result.user_code)
                file.close()
        # Add the file path to the list of files to be deleted
        flagged_for_user_deletion.append(user)
        flagged_for_deletion_paths.append(f"./lock_files/{user}.py")

    for user in flagged_for_user_deletion:
        del attempted_users[user]

    # Delete the files
    for file_path in flagged_for_deletion_paths:
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass

    flagged_for_deletion_paths.clear()

    print("Done checking attempts.")


def check_files(time_threshold=big_o_notation_time_thresholds(0)):
    while True:
        print("Checking files...")
        for user in user_names:
            file_path = f"./lock_files/{user}.py"
            if user in attempted_users and attempted_users[user].passed:
                print(f"{user} already passed, skipping...")
                flagged_for_deletion_paths.append(file_path)
                continue
            try:
                with open(file_path, "r") as file:
                    print(f"Checking {user}.py")
                    user_code = file.read()
                    evaluate_code_threaded(user, user_code, time_threshold)
                    file.close()
            except FileNotFoundError:
                pass
        print("Done checking files.")
        check_attempts()
        time.sleep(5)


# Add the usernames to the list
user_names = [
    "tcrowe",
    "tmerritt",
    # Student name
    # Student name
    # Student name
]


def main():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user with full permissions
    # Iterate the list of usernames and add them to the authorizer
    for user in user_names:
        authorizer.add_user(user, "password", "./lock_files", perm="elradfmw")

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a custom banner (optional)
    handler.banner = "Welcome to the Safe-Cracker FTP server."

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ("0.0.0.0", 2121)
    server = FTPServer(address, handler)

    # Start serving
    server.serve_forever()


if __name__ == "__main__":
    file_checking_thread = threading.Thread(target=check_files(big_o_notation_time_thresholds("test")), daemon=True)
    file_checking_thread.start()
    main()
