class Range:
    def __init__(self, start, size):
        end = start + size
        self.start = start
        self.end   = end

    def __len__(self):
        return self.end - self.start

    def __repr__(self):
        return "(start: " + str(self.start) + " range: " + len(self) + ")"

    def __hash__(self) -> int:
        return (self.start + self.end).__hash__()

    def __eq__(self, other: object):
        if isinstance(other, Range):
            return self.start == other.start and self.end == other.end
        if object == None: # this enables neat if conditions, making Range(0, 0) == None
            return self.__eq__(Range(0, 0))
        return False

    def __sub__(self, other: object) -> []:
        assert isinstance(other, Range)
        difference = []
        if self.start < other.start:
            # self start lies outside other
            difference.append(Range(self.start, other.start-self.start))

        if self.end > other.end:
            # self end lies outside other
            difference.append(Range(other.end, self.end - other.end))

        return difference

    def __and__(self, other: object):
        assert isinstance(other, Range)
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        length = end - start
        if length > 0:
            return Range(start, length)
        return Range(0, 0)


def main():
    seeds = []
    maps_collection = []  # [src -> Range]
    with open("input.txt") as f:
        # parse seeds
        str_seeds = f.readline().strip().split(" ")[1:]
        for seed in str_seeds:
            seeds.append(int(seed))
        seeds = unwrap_to_range(seeds)
        # parse the maps
        for line in f:
            if line == '\n': # expect next set of maps
                maps_collection.append({})
            elif line[0].isalpha(): # maps header
                continue
            else:
                [dest, src, length] = line.strip().split(" ")
                maps_collection[-1][int(src)] = Range(int(dest), int(length))

    values = seeds
    for maps in maps_collection:
        new_values = []
        for value in values:
            # value represents the numbers in a certain range
            # maps represents all mappings for the given stage of translation
            new_values.extend(translate(value, maps))
        values = new_values

    print('lowest thing:', min(map(lambda v: v.start, values)))


def unwrap_to_range(seeds: [int]) -> [Range]:
    res = []
    for i in range(int(len(seeds)/2)):
        start = seeds[i*2]
        count = seeds[i*2+1]
        res.append(Range(start, count))
    return res


def translate(numbers: Range, mappings: map) -> [Range]:
    mapped_numbers = []
    for start in mappings:
        destination = mappings[start]
        source = Range(start, len(destination))
        # lies within map
        overlap = numbers & source
        if overlap:
            offcuts = numbers - source

            # translate the overlap
            translated = Range(overlap.start - source.start + destination.start, len(overlap))
            mapped_numbers.append(translated)

            for piece in offcuts:
                mapped_numbers.extend(translate(piece, mappings))
            return mapped_numbers

    return [numbers]  # no mapping found, thus keeping it the same


if __name__ == "__main__":
    main()
