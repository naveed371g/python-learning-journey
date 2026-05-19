#!/usr/bin/env python3

def getinfo ():
	info = {}
	info['name'] = input("name")
	info['address'] = input("address")

	return info

def write_to_file (info, filename='userinfo'):
	with open(filename, 'w') as file:
		file.write(f"Name : {info['name']}\n")
		file.write(f"Address : {info['address']}\n")

def main():
	info = getinfo()
	write_to_file(info)
"""
if __name__ == "__main__":
    main()
"""
main()
