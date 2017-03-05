import json

def format_json(metadata):
	output = dict()
	for data in metadata['output']:
		keys = data['hostname']
		if keys in output:
			output[keys].append(data)
		else:
			output[keys] = [data]
	return output

def data_format_for_bar_chart(data):
	output = []
	osd_item = ['OSD ID','apply_latency_ms','commit_latency_ms']
	output.append(osd_item)
	for item in data['output']['osd_perf_infos']:
		osd_item = []
		osd_item.append(item['id'])
		osd_item.append(item['perf_stats']['apply_latency_ms'])
		osd_item.append(item['perf_stats']['commit_latency_ms'])
		output.append(osd_item)
	return output

def build_tree_from_list(osd_tree):
	tree_nodes = []
	osd_tree_duplicate = osd_tree

	for node in osd_tree_duplicate['output']['nodes']:
		pass


