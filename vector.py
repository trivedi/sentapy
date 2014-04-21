# Vector object is essentially a dictionary with a few basic methods
# - normalize()
# - min()
# - max()
# - total()


class Vector(dict):

    def __init__(self, *args, **kwargs):
        """
        Uses dictionary constructor
        """
        dict.__init__(self, *args, **kwargs)



    def __getitem__(self, key):
        """
        Lets us index Vector object dictionary style
        Calls inhereited dict __get__() item method

        v = Vector
        v["positive"]

        @param {object} key
        @return {object}
        """
        if key in self:
            return dict.__getitem__(self, key)
        else:
            return 0


    def __repr__(self):
        """
        Representation of {Vector}

        @return {string}
        """
        return dict.__repr__(self)


    def size(self):
        """
        Returns size of the {Vector}

        @return {int}
        """
        return len(self)

    def min(self):
        """
        Returns key with min value

        @return {object}
        """
        # Vector is empty, return no value
        if not self:
            return None

        sorted_vector =  sorted(self.items(), key=lambda x : x[1])
        return sorted_vector[0][0]


    def max(self):
        """
        Returns key with max value

        @return {object}
        """
        # Vector is empty, return no value
        if not self:
            return None

        sorted_vector = sorted(self.items(), key=lambda x : x[1], reverse=True)
        return sorted_vector[0][0]


    def total(self):
        """
        Computes sum of all values

        @return {int||float}
        """
        return sum(self.values())


    def normalize(self):
        """
        Normalize {Vector} by dividing each value by the sum of all values

        @return {Vector}
        """
        total = self.total()*1.0
        normalized_vector = Vector()

        for element in self:
            normalized_vector[element] = self[element] / total

        return normalized_vector

