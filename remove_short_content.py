import os

def remove_short_content(path, len_character):
	with open(path, "r") as f:
		content = f.readlines()

	f = open(path, "w")
	for c in content:
		if len(c.strip()) > len_character:
			f.write(c)
	f.close()

def main():
	project_dir = os.getcwd()
	train_dir = os.path.join(project_dir, "predata", "Train")
	test_dir = os.path.join(project_dir, "predata", "Test")

	for d in [train_dir, test_dir]:
		list_fn = os.listdir(d)
		for fn in list_fn:
			path = os.path.join(d,fn)
			remove_short_content(path, 100)

if __name__ == '__main__':
	main()