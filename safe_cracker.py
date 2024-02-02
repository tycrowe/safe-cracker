import os
import random
import threading
import time

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

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


def evaluate_code(user_code, time_threshold):
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

    start_time = time.time()
    try:
        exec(user_code)
        elapsed_time = time.time() - start_time
        print(f"Elapsed time: {elapsed_time}")
    except Exception as e:
        return f"Error executing code: {e}"

    # To win, the code must be approximately equal to the time threshold.
    # For example, if the time threshold is 1, the code must be between 0.9 and 1.1
    if time_threshold - 0.1 <= elapsed_time <= time_threshold + 0.1:
        return True
    else:
        return f"Time requirement not met. Expected: {time_threshold}, Got: {elapsed_time}"


def check_files(time_threshold=big_o_notation_time_thresholds(0)):
    while True:
        print("Checking files...")
        for user in user_names:
            file_path = f"./lock_files/{user}.py"
            try:
                with open(file_path, "r") as file:
                    print(f"Checking {user}.py")
                    user_code = file.read()
                    result = evaluate_code(user_code, time_threshold)
                    if result is not True:
                        print(result)
                        # Make a copy of the file and move it to the ./attempts directory
                        with open(f"./lock_files/attempts/{user}_latest_attempt.py", "w") as f:
                            f.write(f"# {result}\n")
                            f.write(user_code)
                    else:
                        print(f"{user} passed the time requirement of {time_threshold}.")
                        # Make a copy of the file and move it to the ./passed directory
                        with open(f"./lock_files/passed/{user}_latest_passed.py", "w") as f:
                            f.write(user_code)
                    # Add the file to the list of files to be deleted
                    flagged_for_deletion_paths.append(file_path)
            except FileNotFoundError:
                pass
        # Delete the files that were flagged for deletion
        for file_path in flagged_for_deletion_paths:
            os.remove(file_path)
            print(f"Deleted {file_path}")
        flagged_for_deletion_paths.clear()
        print("Done checking files.")
        time.sleep(3)


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
