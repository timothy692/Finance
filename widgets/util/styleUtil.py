def load_stylesheet(file_path: str) -> str:
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Stylesheet file '{file_path}' not found")
        return ""
    except Exception as e:
        print(f"Could not load stylesheet '{file_path}': {e}")
        return ""