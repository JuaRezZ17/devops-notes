from utils.network import test_conexion

def start_program():
	target_url = "https://www.python.org"
	print(f"Checking the status of {target_url}...")

	if test_conexion(target_url):
		print("¡Everything is fine! We can continue.")
	else:
		print("Error: The service is not available")


if __name__ == "__main__":
	start_program()
