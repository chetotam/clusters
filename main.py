from pprint import pprint
import operator

def update(cluster, service, count):
    new_cluster = dict(cluster)

    # first create array of load distribution between servers
    # as [(<server>, <total_services_running>), ...] sorted in load ascending order
    load_distribution = sorted(
        {server: sum(services.values()) for server, services in new_cluster.items()}.items(),
        key=operator.itemgetter(1)
    )
    servers = [server for server, _ in load_distribution]
    load = [load for _, load in load_distribution]

    # then send service instances one by one to server with lowest load level
    load.append(999999999) # random big number to help us determine which servers are
                           # "lowest load" in case they all have equal amount of services
    for i in range(len(servers)):
        while load[i] < load[i + 1]:
            for j in range(i + 1):
                load[j] += 1
                try:
                    new_cluster[servers[j]][service] += 1
                except KeyError:
                    new_cluster[servers[j]][service] = 1
                count -= 1
                if count == 0:
                    return new_cluster

def main():
    example_data = {
        'ginger': {
            'django': 2,
            'flask': 3,
        },
        'cucumber': {
            'flask': 1,
        },
        'potato': {
            'flask': 6,
        },
        'carrot': {
            'pylons': 3,
        },

    }

    print("Configuration before:")
    pprint(example_data)

    update(example_data, 'pylons', 12)

    print("Configuration after:")
    pprint(example_data)


if __name__ == '__main__':
    main()