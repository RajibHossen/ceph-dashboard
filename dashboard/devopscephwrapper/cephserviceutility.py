"""A service utility modules for ceph rest calls
All the supporting jobs such as formatting json, making bar chart are doing here
"""


def format_json(metadata):
    """
    Change json format data to different json format
    :param metadata:
    :return: formatted json data
    """
    output = dict()
    for data in metadata['output']:
        keys = data['hostname']
        if keys in output:
            output[keys].append(data)
        else:
            output[keys] = [data]
    return output


def data_format_for_bar_chart(data):
    """
    Changing data format to be compatible in bar chart
    :param data:
    :return: formatted data
    """
    output = []
    osd_item = ['OSD ID', 'apply_latency_ms', 'commit_latency_ms']
    output.append(osd_item)
    for item in data['output']['osd_perf_infos']:
        osd_item = [item['id'],
                    item['perf_stats']['apply_latency_ms'],
                    item['perf_stats']['commit_latency_ms']]
        output.append(osd_item)
    return output


def build_tree_from_list(osd_data):
    """
    Build tree structure data from json data
    :param osd_data: json
    :return: tree structured data
    """
    osd_tree = []
    osd_dict = dict((item['id'], item) for item in osd_data['output']['nodes'])

    for node in osd_data['output']['nodes']:
        if 'children' in node and node['type'] == 'root':
            osd_tree.append(node)

    def make_tree(childrens):
        """
        sub module for making tree structures data
        :param childrens:
        :return: child list
        """
        childs = []
        for ids in childrens:
            datas = osd_dict[ids]
            if 'children' in datas and datas['children']:
                datas['children'] = make_tree(datas['children'])
                childs.append(datas)
            else:
                childs.append(datas)
        return childs
    final_tree = dict()
    final_tree['root'] = []
    for item in osd_tree:
        if 'children' in item and item['children']:
            item['children'] = make_tree(item['children'])
            final_tree['root'].append(item)
        else:
            final_tree['root'].append(item)

    return final_tree
