# Function to display settings menu
def display_menu(settings):
    print("Settings Menu:")
    for i, (setting, value) in enumerate(settings.items(), 1):
        print(f"{i}. {setting}: {value}")

# Function to update a setting
def update_setting(settings, setting_name):
    new_value = input(f"Enter new value for {setting_name}: ")
    settings[setting_name] = new_value
    print(f"{setting_name} updated to: {new_value}")

# Main function
def main():
    # Initial settings
    settings = {
        "Option 1": "Value 1",
        "Option 2": "Value 2",
        "Option 3": "Value 3"
    }

    while True:
        display_menu(settings)
        choice = input("Enter the number of the setting to update (or 'q' to quit): ")
        if choice.lower() == 'q':
            break
        try:
            choice = int(choice)
            if 1 <= choice <= len(settings):
                setting_name = list(settings.keys())[choice - 1]
                update_setting(settings, setting_name)
            else:
                print("Invalid choice. Please enter a number between 1 and", len(settings))
        except ValueError:
            print("Invalid input. Please enter a number.")

# Ensure the main function is called when the script is run directly
if __name__ == "__main__":
    main()
