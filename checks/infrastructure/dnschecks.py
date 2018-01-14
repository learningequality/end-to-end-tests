#!/usr/bin/env python
#
# This script checks if the current DNS records for Learning Equality domains and
# subdomains return the expected values.

from collections import namedtuple
import dns.resolver
import socket


DOMAIN = 'learningequality.org'
DNSRecord = namedtuple('DNSRecord', ['name', 'type', 'value', 'comment'])
LE_DOMAINS = """
## Main domain
|@|A|104.18.36.151|Main website|
#
## Supporting infrastrucuture domains
|sushibar|A|35.185.105.222|Suschibar host on GCP|
|pantry|A|162.209.63.41|File server for KA Lite|
|mail|CNAME|ghs.googlehosted.com|Email hosted on Google Apps|
"""

def dns_records_from_table(markdown_table):
    dns_records = []
    for line in markdown_table.splitlines():
        entries = line.split('|')
        if len(entries) == 6:
            name = entries[1].strip()
            record_type = entries[2].strip()
            value = entries[3].strip()
            value = value.replace('@', DOMAIN)
            comment = entries[4].strip()
            dns_record = DNSRecord(name, record_type, value, comment)
            dns_records.append(dns_record)
        elif len(entries) <= 1:
            pass
        else:
            print("Unparsable table row:", line)
    return dns_records



def check_dns_record(dns_record, nameserver=None):
    """
    Checks if dns_record.value matches DNS response returned from the network.
    """
    # 1. Setup
    results = []
    fullname = dns_record.name + '.'
    if '@' in fullname:
        fullname = fullname.replace('@', DOMAIN)
    else:
        fullname += DOMAIN
    #
    # 2. Handle special case of ALIASA record (resolve to ALIAS name to IP)
    if dns_record.type == 'ALIASA':
        resolved_ip = dns.resolver.query(fullname,'A')[0].to_text()
        dns_record = DNSRecord(fullname, 'A', resolved_ip, 'ALIASA-resolved '+dns_record.comment)
    #
    # 3. Do check
    if nameserver:                                     # Use specific DNS Server
        resolver = dns.resolver.Resolver()
        resolver.nameservers=[socket.gethostbyname(nameserver)]
        for rdata in resolver.query(fullname, dns_record.type):
            results.append(rdata)
    else:                                                          # Basic query
        for rdata in dns.resolver.query(fullname, dns_record.type):
            results.append(rdata)
    results_text = [r.to_text().rstrip('.') for r in results]
    #
    if dns_record.value in results_text:
        return True
    else:
        print('DNS error for', dns_record.name, 'Expected:', dns_record.value, 'Got:', results_text)
        return False


if __name__ == "__main__":
    #
    # Load LE doamins
    all_records = dns_records_from_table(LE_DOMAINS)
    #
    # do checks
    for record in all_records:
        check_dns_record(record)  # nameserver='major.ns.cloudflare.com')
    #
    print('DNS checks done.')
