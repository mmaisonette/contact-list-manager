"""
This program is a 'Contact List' app running only on CLI!
It has available a clear description of each function on this
code through the use of docstrings.

You can reach out to me at https://github.com/mmaisonette for any inquirement regarding to this app.
"""

import re
import phonenumbers
from tabulate import tabulate


# Functions
def new_contact(
    contact_list, contact_name, contact_raw_phone, contact_email, contact_favorite
):
    """
    Summary:
        Adds a new contact to the provided contact list.

    Parameters:
        contact_list (list): The list to which the new contact will be appended.
        contact_name (str): The name of the contact.
        contact_phone (str): The phone number of the contact.
        contact_email (str): The email address of the contact.
        contact_favorite (str): Indicates if the contact is a favorite ("Yes" or "No").

    Returns:
        None

    Side Effects:
        Appends a new contact dictionary to contact_list and prints a confirmation message.
    """
    contact_phone = format_phone_number(contact_raw_phone)

    contact = {
        "Name": contact_name.title(),
        "Phone Number": contact_phone,
        "Email": contact_email,
        "Favorite (Yes/No)": contact_favorite.title(),
    }
    contact_list.append(contact)
    print(
        f"\n✅ The contact '{contact_name.title()}' was successfully added to the contact list!"
    )


def format_phone_number(raw_number):
    """
    Summary:
        Formats a raw phone number string by adding parentheses around the first two characters (prefix)
        and a space before the remaining digits.

    Args:
        raw_number (str): The raw phone number string to format.

    Returns:
        str: The formatted phone number in the form "(XX) XXXXXX...".
    """
    prefix = raw_number[:2]
    number = raw_number[2:]
    return f"({prefix}) {number}"


def is_valid_phone(number, region="BR"):
    """
    Summary:
        Validates a phone number for a given region using the phonenumbers library.

    Args:
        number (str): The phone number to validate.
        region (str, optional): The region code to use for parsing the number. Defaults to "BR".

    Returns:
        bool: True if the phone number is valid for the specified region, False otherwise.
    """
    try:
        parsed = phonenumbers.parse(number, region)
        return phonenumbers.is_valid_number(parsed)
    except phonenumbers.NumberParseException:
        return False


def is_valid_email(email):
    """
    Summary:
        Validates whether the provided email address matches a standard email format.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    # A common regex pattern for email validation.
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,7}$"
    if re.fullmatch(regex, email):
        return True
    return False


def view_contacts(contact_list):
    """
    Summary:
        Displays the list of contacts in a formatted table.

        If the contact list is empty, prints a warning message.
        Otherwise, prints the contacts using a fancy grid format with indexed rows
        using the tabulate library.

    Args:
        contact_list (list of dict): The list of contacts to display. Each contact should be represented as a dictionary.

    Returns:
        None
    """
    if not contact_list:
        print("\n⚠️  No contacts found!")
        return

    table = tabulate(
        contact_list,
        headers="keys",
        tablefmt="fancy_grid",
        showindex=range(1, len(contact_list) + 1),
    )
    print(table)
    return


def list_favorites(contact_list):
    """
    Summary:
            Displays a list of favorite contacts from the provided contact list.

            Iterates through the contact_list and filters contacts marked as favorites
            (i.e., where the "Favorite (Yes/No)" field is set to "Yes", case-insensitive).
            If favorite contacts are found, prints them in a formatted table using the tabulate library.
            If no favorites are found, prints a warning message.

    Args:
        contact_list (list of dict): The list of contact dictionaries to search for favorites.

    Returns:
        None
    """
    favorites = [
        contact
        for contact in contact_list
        if str(contact.get("Favorite (Yes/No)", "")).lower() in ("yes")
    ]
    if not favorites:
        print("\n⚠️ No favorite contacts found!")
        return
    print("\n⭐ Favorite Contacts:")
    print()
    table = tabulate(
        favorites,
        headers="keys",
        tablefmt="fancy_grid",
        showindex=range(1, len(favorites) + 1),
    )
    print(table)
    return


def edit_contact(contact_list):
    """
    Summary:
        Allows the user to select and edit an existing contact from the contact list.

        Displays the current list of contacts and prompts the user to choose a contact by its number.
        For the selected contact, prompts the user to edit each field (Name, Phone Number, Email, Favorite),
        showing the current value and allowing the user to keep it by pressing Enter.
        Updates the contact with any new values entered by the user.

    Args:
        contact_list (list): A list of contact dictionaries to be edited.

    Returns:
        None
    """
    if not contact_list:
        print("\n⚠️ There are no contacts to edit yet!")
        return

    # Show current contact list.
    view_contacts(contact_list)

    # Ask which contact to edit.
    while True:
        choice = input(
            "\nEnter the number of the contact to edit (or 'b' to go back): "
        ).strip()
        if choice.lower() == "b":
            print("Edit canceled! Returning to main menu!")
            return
        if not choice.isdigit():
            print("⚠️ Please enter a valid number!")
            continue

        # Adjusting the index to the right position.
        index = int(choice) - 1
        if 0 <= index < len(contact_list):
            break
        print(f"Please enter a number between 1 and {len(contact_list)}.")

    contact = contact_list[index]
    print(
        f"\nEditing contact #{index+1} — current values in [brackets]. Press Enter to keep them.\n"
    )

    # Prompt with current values; keep old if user hits Enter.
    new_name = input(f"Name [{contact.get('Name','')}]: ").strip()
    new_phone = input(f"Phone [{contact.get('Phone Number','')}]: ").strip()
    new_email = input(f"Email [{contact.get('Email','')}]: ").strip()
    new_favorite = input(f"Favorite? [{contact.get('Favorite (Yes/No)','')}]: ").strip()

    if new_name:
        contact["Name"] = new_name
    if new_phone:
        contact["Phone Number"] = format_phone_number(new_phone)
    if new_email:
        contact["Email"] = new_email
    if new_favorite:
        contact["Favorite (Yes/No)"] = new_favorite

    print("\n✅ Contact updated successfully!")
    # Just return — control goes back to the main loop (main menu).
    return


def delete_contact(contact_list):
    """
    Summary:
        Removes a contact from the provided contact list based on user input.

        Displays the current list of contacts and prompts the user to enter the contact number to remove.
        Validates the input and removes the selected contact if the input is valid.
        Prints a confirmation message upon successful removal or an error message if the input is invalid.

    Args:
        contact_list (list): A list of contact dictionaries, each containing contact details.

    Returns:
        None
    """
    print("\nWhich contact would you like to remove?")

    # Show current contact list.
    view_contacts(contact_list)

    choice = input("\nPlease, type the contact number: ").strip()
    if not choice.isdigit():
        print("\n⚠️ Invalid contact number!")
        return

    # Adjusting the index to the right position.
    index = int(choice) - 1
    if 0 <= index < len(contact_list):
        removed = contact_list.pop(index)
        print(f"\n✅ Contact '{removed['Name']}' was removed successfully!")
    else:
        print("\n⚠️ Invalid contact number!")


# An empty list to start. That is a list of dictionaries.
contact_list = []

# Menu
while True:
    print("\n📇 CONTACT LIST")
    print("\nThese are the options available:\n")
    print("1. Add a new contact")
    print("2. View the contact list")
    print("3. List the favorite contacts")
    print("4. Edit a contact")
    print("5. Delete a contact")
    print("6. Exit")

    # Calling functions.
    selected_option = input("\nPlease, choose an option: ")
    print()

    if selected_option == "1":
        # Running the name input and validation.
        while True:
            contact_name = input(
                "Inform the name and last name of the new contact (the last one or most used): "
            )
            parts = contact_name.strip().split()
            if len(parts) >= 2 and all(len(part) >= 2 for part in parts[:2]):
                break
            retry = print("\n⚠️ It is necessary to enter the name of the new contact!")

        # Running the phone number input and validation.
        while True:
            contact_phone = input(
                "Inform the phone number with the prefix (e.g., 51, 54, etc.): "
            )
            if is_valid_phone(contact_phone):
                break
            retry = (
                input(
                    "\n⚠️ Press 'Enter' to try again or 'q' to continue without adding a phone number. "
                )
                .strip()
                .lower()
            )
            if retry == "q":
                break

        # Running an email address validation.
        while True:
            contact_email = input("Provide a valid email address: ")
            if is_valid_email(contact_email):
                break
            retry = (
                input(
                    "\n⚠️ Invalid email address! Press 'Enter' to try again or 'q' to continue without adding an email. "
                )
                .strip()
                .lower()
            )
            if retry == "q":
                contact_email = ""
                break

        # Checking if the favorite is set or not.
        while True:
            contact_favorite = input("Is it a favorite contact? Yes/No: ")
            if len(contact_favorite) == 3:
                break
            contact_favorite = "No"
            break

        new_contact(
            contact_list, contact_name, contact_phone, contact_email, contact_favorite
        )
    elif selected_option == "2":
        view_contacts(contact_list)
    elif selected_option == "3":
        list_favorites(contact_list)
    elif selected_option == "4":
        edit_contact(contact_list)
    elif selected_option == "5":
        delete_contact(contact_list)
    elif selected_option == "6":
        print("\nAll tasks completed. Goodbye!")
        break
