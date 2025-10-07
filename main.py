"""
This program is a 'Contact List' app running only on CLI!
We have available a clear description of each function on this
code through the use of docstrings.

Any inquirement can be send to marciomaisonette@gmail.com.
"""

import re
import phonenumbers
from tabulate import tabulate


# Functions
def new_contact(
    contact_list, contact_name, contact_phone, contact_email, contact_favorite=False
):
    """
    The goal of this function is to add a new contact.

    The parameters in use in this function are to add:
    - name
    - phone
    - email
    - set to favorite or not

    Through this function the dict will be created.
    """
    contact = {
        "Name": contact_name.title(),
        "Phone Number": contact_phone,
        "Email": contact_email,
        "Favorite [Yes/No]": contact_favorite.title(),
    }
    contact_list.append(contact)
    print(
        f"\nThe contact '{contact_name.title()}' was successfully added to the contact list!"
    )
    return


def is_valid_phone(number, region="BR"):
    """
    This functional was create to perform a validation of the
    phone provided. The goal is guarantee that the phone is
    right and consice with the region.

    This funcition is using the third party module 'phonenumber'.
    """
    try:
        parsed = phonenumbers.parse(number, region)
        return phonenumbers.is_valid_number(parsed)
    except phonenumbers.NumberParseException:
        return False


def is_valid_email(email):
    """
    This function is responsible for validate the email
    informed by the user.
    """
    # A common regex pattern for email validation
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,7}$"
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def view_contacts(contact_list):
    """
    This function should be used to show the contact list.

    That will show all contacts in a table formated by the tabulate().
    Now includes an index column for easy reference.
    """
    if not contact_list:
        print("\n⚠️ No contacts found!")
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
    This function displays only the contacts marked as favorite.
    """
    favorites = [
        contact
        for contact in contact_list
        if str(contact.get("Favorite [Yes/No]", "")).lower() in ("yes")
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
    """Let the user choose a contact by number and edit its fields."""
    if not contact_list:
        print("\nThere are no contacts to edit yet.")
        return

    # Show current contact list
    view_contacts(contact_list)

    # Ask which contact to edit
    while True:
        choice = input(
            "\nEnter the number of the contact to edit (or 'b' to go back): "
        ).strip()
        if choice.lower() == "b":
            print("Edit canceled. Returning to main menu.")
            return
        if not choice.isdigit():
            print("Please enter a valid number.")
            continue

        index = int(choice) - 1
        if 0 <= index < len(contact_list):
            break
        else:
            print(f"Please enter a number between 1 and {len(contact_list)}.")

    contact = contact_list[index]
    print(
        f"\nEditing contact #{index+1} — current values in [brackets]. Press Enter to keep them.\n"
    )

    # Prompt with current values; keep old if user hits Enter
    new_name = input(f"Name [{contact.get('Name','')}]: ").strip()
    new_phone = input(f"Phone [{contact.get('Phone Number','')}]: ").strip()
    new_email = input(f"Email [{contact.get('Email','')}]: ").strip()
    new_favorite = input(f"Favorite? [{contact.get('Favorite [Yes/No]','')}]: ").strip()

    if new_name:
        contact["name"] = new_name
    if new_phone:
        contact["phone"] = new_phone
    if new_email:
        contact["email"] = new_email
    if new_favorite:
        contact["favorite"] = new_favorite

    print("\n✅ Contact updated successfully!")
    # Just return — control goes back to the main loop (main menu)
    return


def delete_contact(contact_list):
    """This function should be used to delete a contact from the contact list."""
    print("\nWhich contact would you like to remove?")

    # Show current contact list
    view_contacts(contact_list)

    choice = input("\nPlease, type the contact number: ").strip()
    if not choice.isdigit():
        print("\n⚠️ Invalid contact number.")
        return

    index = int(choice) - 1
    if 0 <= index < len(contact_list):
        removed = contact_list.pop(index)
        print(f"\n✅ Contact '{removed['name']}' was removed successfully!")
    else:
        print("\n⚠️ Invalid contact number.")


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

    # Calling functions
    selected_option = input("\nPlease, choose an option: ")
    print()  # Adds a blank line after the input prompt

    if selected_option == "1":
        # Running the name input and validation
        while True:
            contact_name = input(
                "Inform the name and last name (the last one or most used): "
            )
            parts = contact_name.strip().split()
            if len(parts) >= 2 and all(len(part) >= 2 for part in parts[:2]):
                break
            else:
                retry = print("\n⚠️ Please enter both a first name and a last name!")
        # Running the phone number input and validation
        while True:
            contact_phone = input(
                "Inform the phone number with the prefix (e.g. 51, 54, etc.): "
            )
            if is_valid_phone(contact_phone):
                break
            else:
                retry = (
                    input(
                        "\n⚠️ Press Enter to try again or 'q' to continue without adding a phone number: "
                    )
                    .strip()
                    .lower()
                )
                if retry == "q":
                    break
        # Running an email address validation
        while True:
            contact_email = input("Inform a valid email address: ")
            if is_valid_email(contact_email):
                break
            else:
                retry = (
                    input(
                        "\n⚠️ Invalid email address. Press Enter to try again or 'q' to continue without adding an email: "
                    )
                    .strip()
                    .lower()
                )
            if retry == "q":
                contact_email = ""
                break

        # Checking if the favorite is set or not
        while True:
            contact_favorite = input("Is it favorite? Yes/No: ")
            if len(contact_favorite) == 3:
                break
            else:
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
        print("\nThe program is finishing!")
        break
