import h5py


def iterate_nxs(nxs: h5py.File):
    q = []
    q.extend([(None, nxs[group_key]) for group_key in nxs.keys()])
    # q = [(file, "entry")]
    while len(q) > 0:
        parent, current_group = q.pop(0)
        # current_group_reference = parent_group[key]
        # print("Value:", group)

        next_groups = getattr(current_group, "keys")() if hasattr(current_group, "keys") else []

        # extend with the next group references
        q.extend([(current_group, current_group[next_group_name]) for next_group_name in next_groups])
        # q.extend([(current_group_reference, next_group_name) for next_group_name in next_groups])
        # print("Queue state  :", q)

        yield parent, current_group


if __name__ == "__main__":
    with h5py.File("testfile.nxs") as file:
        for group, next in iterate_nxs(file):
            print("Parent grp", group, "Next groups", next)
