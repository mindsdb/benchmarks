import os

with open('data.csv', 'w') as fp:
	fp.write('class,superclass,image_path')
	for set_dir in ('test', 'train'):
		for dn in os.listdir(set_dir):
			for fn in os.listdir(os.path.join(set_dir, dn)):
				for img_name in os.listdir(os.path.join(set_dir, dn, fn)):
					img_path = os.path.join('benchmarks','datasets', 'cifar100',set_dir, dn, fn, img_name)
					fp.write(f'\n{fn},{dn},{img_path}')
