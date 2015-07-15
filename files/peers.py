#!/usr/bin/env python

import boto.ec2
import boto.ec2.autoscale
import json

def autoscaling_peers():
    metadata = boto.utils.get_instance_identity()['document']

    autoscaling = boto.ec2.autoscale.connect_to_region(metadata['region'])
    ec2 = boto.ec2.connect_to_region(metadata['region'])

    for group in autoscaling.get_all_groups():
        for instance in group.instances:
            if instance.instance_id == metadata['instanceId']:
                group.instances.remove(instance)

                instance_ids = [i.instance_id for i in group.instances]
                for status in ec2.get_all_instance_status(instance_ids):
                    if status.instance_status.status != 'ok':
                        instance_ids.remove(status.id)

                if not instance_ids:
                    return []

                return ec2.get_only_instances(instance_ids)

if __name__ == '__main__':
    config = {}
    config['start_join'] = [p.private_dns_name for p in autoscaling_peers()]
    print json.dumps(config)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

