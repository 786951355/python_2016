from pyzabbix import ZabbixAPI, ZabbixAPIException

ZABBIX_SERVER = 'your zabbix url'
zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.session.auth = ("basic auth user", "basic auth pass")
zapi.login('user', 'pass')

