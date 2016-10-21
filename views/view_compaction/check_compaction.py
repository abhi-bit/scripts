#!/usr/bin/python

import sys
import time


def main():
    pattern = "%Y-%m-%dT%H:%M:%S"
    result = dict()
    with open(sys.argv[1]) as f:
        for line in f:
            if "Compacting indexes for" in line:
                data = line.split()
                timestamp = data[0].split(',')[1].split('.')[0]
                epoch = int(time.mktime(time.strptime(timestamp, pattern)))
                ddoc_id = data[3]

                if ddoc_id not in result:
                    result[ddoc_id] = list()
                timing_snapshot = dict()
                timing_snapshot['start_time'] = epoch
                timing_snapshot['ts'] = timestamp
                result[ddoc_id].append(timing_snapshot)

            if "Finished compacting indexes" in line:
                data = line.split()
                timestamp = data[0].split(',')[1].split('.')[0]
                epoch = int(time.mktime(time.strptime(timestamp, pattern)))
                ddoc_id = data[4]

                if ddoc_id not in result:
                    # print ("INFO: ddoc %s start compact missing" % ddoc_id)
                    continue
                else:
                    snapshot_to_update = result[ddoc_id][-1]
                    snapshot_to_update['end_time'] = epoch
                    result[ddoc_id][-1] = snapshot_to_update

    # print avg, min, max compaction time on per ddoc level
    for ddoc in result:
        compaction_entries = result[ddoc]
        entry_count = len(compaction_entries)
        max_val = 0
        min_val = sys.maxint
        sum_val = 0.0
        for entry in compaction_entries:
            if 'end_time' in entry:
                time_elapsed = entry['end_time'] - entry['start_time']
                if time_elapsed > 0:
                    if time_elapsed > max_val:
                        max_val = time_elapsed
                    if time_elapsed < min_val:
                        min_val = time_elapsed
                sum_val = sum_val + time_elapsed
            else:
                print ("WARNING: ddoc %s finish compact missing, compact start timestamp %s "
                       % (ddoc_id, entry['ts']))
        print ("ddoc: %s max_val: %d min_val: %d avg_val: %f" %
               (ddoc, max_val, min_val, sum_val/entry_count))


if __name__ == "__main__":
    main()
