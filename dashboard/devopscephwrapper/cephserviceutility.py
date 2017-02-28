import json

def format_json(metadata):
	output = dict()
	outputlist = []
	for data in metadata['output']:
		keys = data['hostname']
		if keys in output:
			output[keys].append(data)
		else:
			output[keys] = [data]
	outputlist.append(output)
	return outputlist

