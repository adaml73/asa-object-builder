import pprint as pprint
import pandas as pd
import jinja2, ipaddress, click




network_object_host_template = """
{% for i in dict %}
object network {{ dict[i]['ObjectName'] }}
description {{ dict[i]['description'] }}
host {{ dict[i]['ip'] }}
{% endfor %}
"""

network_object_group_template = """
object-group network 
description
{% for i in dict -%}
network-object {{ dict[i]['ObjectName'] }}
{% endfor %}
"""

def build_network_objects(records):
	network_object_builder = jinja2.Template(network_object_host_template)
	network_object_output = network_object_builder.render(dict=records)
	print(network_object_output)

def build_network_object_group(records):
	network_object_group_builder = jinja2.Template(network_object_group_template)
	network_object_group_output = network_object_group_builder.render(dict=records)
	print(network_object_group_output)

def format_object_name(records):
	try:
		for i in records:
			if ipaddress.ip_address(records[i]['ip']).is_private:
				records[i]['ObjectName'] = 'ON_' + records[i]['name'] + '_Hst'
			elif ipaddress.ip_address(records[i]['ip']).is_multicast:
				recordsp[i]['ObjectName'] = 'ON_' + records[i]['name'] + '_Mcst'
			elif ipaddress.ip_address(records[i]['ip']).is_global:
				records[i]['ObjectName'] = 'ON_' + records[i]['name'] + 'Pub_Hst'
			else:
				print('IP type unspecified')
				records[i]['ObjectName'] = 'ON_' + records[i]['name'] 
	except e as exception:
		print(e)




@click.command()
@click.argument('csv')
@click.argument('description')


def object_writer(csv,description):
	click.echo(f'importing CSV {csv}')
	df = pd.read_csv(csv)
	records = df.to_dict(orient='index')
	for i in records:
		records[i]['description'] = records[i]['name'] + ' ' + description
	format_object_name(records)
	build_network_objects(records)
	build_network_object_group(records)



if __name__ == '__main__':
	object_writer()