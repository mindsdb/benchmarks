import os

with open('data.csv', 'w') as fp:
	fp.write('emotion,audio_path')
	for emotion in os.listdir('.'):
		if emotion.endswith('.py') or emotion.endswith('.md') or emotion.endswith('.csv'):
			continue
		for fn in os.listdir(emotion):
			audio_path = os.path.join('benchmarks','datasets', 'aesdd',emotion,fn)
			fp.write(f'\n{emotion},{audio_path}')
