#!/usr/bin/python
import argparse
import os
import sys
import configset 
THIS_PATH = os.path.dirname(__file__)
configname = os.path.join(THIS_PATH, 'conf.ini')
EXT = configset.read_config4('DB', 'EXT', configname)[0]
if EXT == None:
	EXT = "dns"

class bind(object):
	def __init__(self):
		super(bind, self)

	def makedomain(self, host, ip, typedns='bind'):
		data = [ip, host, ip, ip, host, ip, ip]
		if typedns == 'bind' or typedns == 'bind9':
			template = """$TTL 10800
@		IN SOA	{0}. root.{1}. (
			  2015080401   ; Serial number
			  10800        ; Refresh
			  3600         ; Retry
			  777600       ; Expire
			  3600       ) ; Minimum TTL
		A	{2}
		NS	{3}.
		MX	10 mail.{4}.
ftp		A	{5}
mail		A	{6}
www		CNAME	@
""".format(*data)
		elif typedns == 'sdnsp' or typedns == 'sdnsplus' or typedns == 'simple' or typedns == 'simple dns plus' or typedns == 'simplednsplus':
			template = """
		$TTL 10800
@		IN SOA	( {0}. ; Primary DNS server
			  root.{1}. ; Responsible person
			  2015080401   ; Serial number
			  10800        ; Refresh
			  3600         ; Retry
			  777600       ; Expire
			  3600       ) ; Minimum TTL
		A	{2}
		NS	{3}.
		MX	10 mail.{4}.
ftp		A	{5}
mail		A	{6}
www		CNAME	@
""".format(*data)

		print "template =", template
		print '-'*94
		print "DB-PATH =", os.path.join(os.path.join(configset.read_config4('DB', 'PATH', configname))[0], str(host) + '.' + EXT)
		print '-'*94
		fi = open(os.path.join(configset.read_config4('DB', 'PATH', configname)[0], str(host) + '.' + EXT), 'w')
		fi.write("\n")
		fi.write(template)
		fi.close()

	def insertdomain(self, host, typehost='master', dbpath=None, configpath=None):
		if dbpath == None:
			dbpath = os.path.join(configset.read_config4('DB', 'PATH', configname)[0], str(host) + "." + EXT)
		else:
			dbpath = os.path.join(dbpath, str(host) + "." + EXT)
		print "HOST   2 =", host
		print "TYPE   2 =", typehost
		print "DBPATH 2 =", dbpath
		# data1 = [host, typehost, dbpath]
		template = """zone "%s" {
        type %s;
        file "%s";
};"""%(host, typehost, dbpath)
		print "template =", template
		if configpath == None:
			fi = open(configset.read_config4('DB', 'CONFIG_PATH', configname)[0], 'a')
		else:
			fi = open(configpath, 'a')
		fi.write("\n")
		fi.write(template)
		fi.close()

	def control(self, host, ip, typehost='master', dbpath=None, configpath=None, typedns='bind'):
		self.makedomain(host, ip, typedns)
		self.insertdomain(host, typehost, dbpath)

	def usage(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('-H', '--host', help='Host Domain Name', action='store')
		parser.add_argument('-i', '--ip', help='IP Host Domain Name', action='store')
		parser.add_argument('-t', '--type', help='Type Host Domain Name [master, slave], default=master', default='master', action='store')
		parser.add_argument('-c', '--config', help='Config file name path, default=path of bind installer', action='store')
		parser.add_argument('-z', '--zone-path', help='Zone Config path, default=path of bind installer', action='store')
		parser.add_argument('-d', '--type-dns', help='Type Dns Server, default=bind', default='bind', action='store')
		if len(sys.argv) == 1:
			parser.print_help()
		else:
			args = parser.parse_args()
			self.control(args.host, args.ip, args.type, args.zone_path, args.config, args.type_dns)


if __name__ == '__main__':
	c = bind()
	# c.makedomain('hacker.net', '192.168.1.4')
	c.usage()
