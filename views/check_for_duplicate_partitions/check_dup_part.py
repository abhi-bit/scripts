#!/usr/bin/python

import sys


def scan_active_partition(line, f):
    active_block_str = ""
    content = ""
    content = line.split("[")[2]
    active_block_str += content.rstrip()
    if "]" not in content:
        more_line = ""
        for more_line in f:
            if "Passive partition" not in more_line:
                if "]" in more_line:
                    active_block_str += \
                        more_line.split(" ")[-2].split("]")[0].rstrip()
                    break
                else:
                    active_block_str += \
                        more_line.split(" ")[-1].rstrip()
    return active_block_str


def scan_passive_partition(line, f):
    passive_block_str = ""
    content = ""
    content = line.split(" ")[3].split("[")[1].rsplit()[0]
    if "]" in content:
        passive_block_str += content.split("]")[0].rstrip()
    else:
        passive_block_str += content.rstrip()
    if "]" not in content:
        more_line = ""
        for more_line in f:
            if "Cleanup partition" not in more_line:
                if "]" in more_line:
                    passive_block_str += \
                        more_line.split(" ")[-2].split("]")[0].rstrip()
                    break
                else:
                    passive_block_str += \
                        more_line.split(" ")[-1].rstrip()

    return passive_block_str


def scan_cleanup_partition(line, f):
    cleanup_block_str = ""
    content = ""
    content = line.split(" ")[3].rsplit()[0]
    cleanup_block_str += content.split("[")[1].rstrip()
    if "]" not in content:
        more_line = ""
        for more_line in f:
            if "]" in more_line:
                cleanup_block_str += \
                    more_line.split(" ")[-2].split("]")[0].rstrip()
                break
            else:
                cleanup_block_str += \
                    more_line.split(" ")[-1].rstrip()

    return cleanup_block_str


def main():
    with open(sys.argv[1]) as f:
        for line in f:
            active_block_str = ""
            passive_block_str = ""
            cleanup_block_str = ""
            # agg_part_list = ""
            intersection_counter = 0
            if "Active partition" in line:
                active_block_str = scan_active_partition(line, f)

                line = f.next()
                if "Passive partition" in line:
                    passive_block_str = scan_passive_partition(line, f)

                    line = f.next()
                    if "Cleanup partition" in line:
                        cleanup_block_str = scan_cleanup_partition(line, f)

                # TODO: Bug when any of active/passive/cleanup list is
                #       empty - list size is returned as one - so
                #       agg_part_list size can be b/w 1024-1026
                # agg_part_list = active_block_str + ',' + \
                #     passive_block_str + ',' +\
                #     cleanup_block_str
                # print "aggregate len:", len(agg_part_list.split(','))

                # print "active_block_str:", active_block_str, \
                #     "len:", len(active_block_str.split(","))
                # print "passive_block_str:", passive_block_str, \
                #     "len:", len(passive_block_str.split(","))
                # print "cleanup_block_str:", cleanup_block_str, \
                #     "len:", len(cleanup_block_str.split(","))

            if active_block_str != "" \
                    or passive_block_str != "" or cleanup_block_str != "":
                # check for intersection
                if active_block_str != "" and passive_block_str != "":
                    act_pass = list(set(active_block_str.split(",")) &
                                    set(passive_block_str.split(",")))
                    if len(act_pass) > 0:
                        print act_pass
                        intersection_counter += 1
                        print "Overlap bn active and passive partition"

                if active_block_str != "" and cleanup_block_str != "":
                    act_clean = list(set(active_block_str.split(",")) &
                                     set(cleanup_block_str.split(",")))
                    if len(act_clean) > 0:
                        print act_clean
                        intersection_counter += 1
                        print "Overlap bn active and cleanup partition"

                if passive_block_str != "" and cleanup_block_str != "":
                    pass_clean = list(set(passive_block_str.split(",")) &
                                      set(cleanup_block_str.split(",")))
                    if len(pass_clean) > 0:
                        print pass_clean
                        intersection_counter += 1
                        print "Overlap bn passive and cleanup partition"

                if intersection_counter > 0:
                    print "intersection_counter", intersection_counter

                # print "Active:", active_block_str
                # print "Passive:", passive_block_str
                # print "Cleanup:", cleanup_block_str


if __name__ == "__main__":
    main()
