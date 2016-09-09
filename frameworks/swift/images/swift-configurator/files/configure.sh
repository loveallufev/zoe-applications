#!/bin/bash

set -x

PART_POWER=${PART_POWER:-10}
ZONE_COUNT=${ZONE_COUNT:-3}

NODES=$(python /usr/local/bin/list_storage_nodes.py)

if [ ! -f /etc/swift/account.ring.gz ]; then
	kind=account
	port=6002
	BUILDER_FILE=/etc/swift/${kind}.builder

	swift-ring-builder $BUILDER_FILE create $PART_POWER 3 24

	for node in $NODES; do
		zone=$RANDOM
		let "zone %= $ZONE_COUNT"
		let "zone += 1"
		swift-ring-builder $BUILDER_FILE add --region 1 --zone $zone --ip $(getent hosts $node | awk '{ print $1 }' | head -n1) --port $port --device volume --weight 100
	done

	swift-ring-builder $BUILDER_FILE rebalance

	kind=container
	port=6001
	BUILDER_FILE=/etc/swift/${kind}.builder

	swift-ring-builder $BUILDER_FILE create $PART_POWER 3 24

	for node in $NODES; do
		zone=$RANDOM
		let "zone %= $ZONE_COUNT"
		let "zone += 1"
		swift-ring-builder $BUILDER_FILE add --region 1 --zone $zone --ip $(getent hosts $node | awk '{ print $1 }' | head -n1) --port $port --device volume --weight 100
	done

	swift-ring-builder $BUILDER_FILE rebalance

	kind=object
	port=6000
	BUILDER_FILE=/etc/swift/${kind}.builder

	swift-ring-builder $BUILDER_FILE create $PART_POWER 3 24

	for node in $NODES; do
		zone=$RANDOM
		let "zone %= $ZONE_COUNT"
		let "zone += 1"
		swift-ring-builder $BUILDER_FILE add --region 1 --zone $zone --ip $(getent hosts $node | awk '{ print $1 }' | head -n1) --port $port --device volume --weight 100
	done

	swift-ring-builder $BUILDER_FILE rebalance

fi

