import requests

def test_conexion(url):
	try:
		response = requests.get(url, timeout=5)
		return response.status_code == 200
	except Exception:
		return False


if __name__ == "__main__":
	print("Running internal test for network.py...")
	test_url = "https://www.google.com"
	if test_conexion(test_url):
		print(f"Success: {test_url} is working.")
	else:
		print(f"Error: I can't connect to {test_url}")
