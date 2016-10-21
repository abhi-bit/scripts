#!/usr/bin/python

import json
import requests
import sys
import urllib


def main():
    host_cluster_ip = sys.argv[1]
    bucket_name = sys.argv[2]
    user_name = sys.argv[3]
    password = sys.argv[4]
    compaction_threshold = int(sys.argv[5])

    stats_url = "http://" + host_cluster_ip + ":8091/pools/default/buckets/" + \
        bucket_name + "/stats"
    stats_dump = requests.get(stats_url, auth=(user_name, password),
                              data={'zoom': 'minute'})
    stats_result = json.loads(stats_dump.text)
    if max(stats_result["op"]["samples"]["couch_views_fragmentation"]) > \
            compaction_threshold:

        # get the list of design docs
        ddocs_url = "http://" + host_cluster_ip + ":8091/pools/default/buckets/" + \
            bucket_name + "/ddocs"
        ddocs_dump = requests.get(ddocs_url)
        ddocs_result = json.loads(ddocs_dump.text)
        ddocs = list()
        for entry in ddocs_result["rows"]:
            item = entry["doc"]["meta"]["id"]
            ddocs.append(urllib.quote(item, safe=''))

        # compact the ddocs one by one:
        for ddoc in ddocs:
            ddoc_compact_url = "http://" + host_cluster_ip + \
                ":8091/pools/default/buckets/" + bucket_name + \
                "/ddocs/" + ddoc + "/controller/compactView"
            r = requests.post(ddoc_compact_url, auth=(user_name, password))
            print ("ddoc: %s, compact call status code: %d" %
                   (ddoc, r.status_code))

if __name__ == "__main__":
    main()
