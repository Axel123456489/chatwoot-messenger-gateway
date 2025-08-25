import subprocess


def run_black():
    print("Running black...")
    subprocess.run(["black", "."], check=True)


def run_isort():
    print("Running isort...")
    subprocess.run(["isort", "."], check=True)


def run_flake8():
    print("Running flake8...")
    subprocess.run(["flake8", "."], check=True)


def main():
    try:
        run_black()
        run_isort()
        run_flake8()
        print("Linting completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during linting: {e}")
        exit(1)


if __name__ == "__main__":
    main()
