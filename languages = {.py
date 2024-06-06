languages = {
    'english': {"greeting": "Hello"},
    'malay': {"greeting": "Selamat Datang" }
}

def select_language():
    print("Select a language:")
    for i, lang in enumerate(languages):
        print(f"{i + 1}. {lang}")

    selection = input("Enter the number of your preferred language: ")
    try:
        selection = int(selection)
        if 1 <= selection <= len(languages):
            return list(languages.keys())[selection - 1]
        else:
            print("Invalid selection. Please enter a number between 1 and", len(languages))
            return select_language()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return select_language()

def get_message(language, key):
    return languages[language].get(key, f"Message '{key}' not found in {language}.")

def main():
    selected_language = select_language()
    print(get_message(selected_language, "greeting"))
    print(get_message(selected_language, "farewell"))

if __name__ == "__main__":
    main()