#!/usr/bin/env python3
"""
Script to write personal information to a file.
"""

def get_user_info():
    """Collect user information via input prompts."""
    info = {}
    
    print("=== Personal Information Writer ===")
    print("Please enter your information (press Enter to skip a field):\n")
    
    info['name'] = input("Name: ")
    info['email'] = input("Email: ")
    info['phone'] = input("Phone: ")
    info['address'] = input("Address: ")
    info['city'] = input("City: ")
    info['state'] = input("State/Province: ")
    info['zip'] = input("ZIP/Postal Code: ")
    info['country'] = input("Country: ")
    info['occupation'] = input("Occupation: ")
    info['notes'] = input("Additional notes: ")
    
    return info

def write_info_to_file(info, filename='user_info.txt'):
    """Write the collected information to a file."""
    with open(filename, 'w') as f:
        f.write("=== Personal Information ===\n")
        f.write(f"Name: {info['name']}\n")
        f.write(f"Email: {info['email']}\n")
        f.write(f"Phone: {info['phone']}\n")
        f.write(f"Address: {info['address']}\n")
        f.write(f"City: {info['city']}\n")
        f.write(f"State/Province: {info['state']}\n")
        f.write(f"ZIP/Postal Code: {info['zip']}\n")
        f.write(f"Country: {info['country']}\n")
        f.write(f"Occupation: {info['occupation']}\n")
        f.write(f"Notes: {info['notes']}\n")
        f.write("=" * 30 + "\n")
    
    print(f"\nInformation successfully written to {filename}")

def main():
    """Main function to run the script."""
    info = get_user_info()
    write_info_to_file(info)

if __name__ == "__main__":
    main()
