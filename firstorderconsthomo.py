import numpy.linalg as la
import scipy as sp


class System:

    def __init__(self, operator, initial):
        """

        :param operator:
        :param initial:
        """
        self.operator = operator
        self.initial = initial
        self.dimensions = sp.shape(initial)[0]

    @property
    def operator(self):
        return self.__operator

    @operator.setter
    def operator(self, val):
        self.__operator = val
        self.eigenvalues, self.eigenvectors = la.eig(val)
        self.norm_factors = self._generate_norm_factors(self.eigenvectors)
        self.normalized = self._normalize(self.eigenvectors)
        self.coefficients = self._decomp(self.initial, self.eigenvectors)
        return None

    @property
    def initial(self):
        return self.__initial

    @initial.setter
    def initial(self, val):
        self.__initial = val
        self.coefficients = self._decomp(self.initial, self.eigenvectors)



    def _generate_norm_factors(self, vectors):
        """

        :param vectors: NxM array of M N-dimensional vectors (the vectors are column vectors).
        :return: NdArray.  Element i is the normalization factor for vector vectors[:, i].
        """
        norms = sp.zeros(sp.shape(vectors)[1])
        for index, vec in enumerate(vectors):
            norms[index] = 1 / abs(sp.dot(vec.conj(), vec))
        return norms

    def _normalize(self, vectors):
        """
        Normalize the eigenvectors vectors.
        :param vectors:
        :return:
        """
        normalized = sp.zeros(sp.shape(vectors), dtype=complex)
        for index, vector in enumerate(vectors):
            normalized[:, index] = vector * self.norm_factors[index]
        return normalized

    def _decomp(self, decomposee, vectors):
        """

        :param decomposee:
        :param vectors:
        :return:
        """
        coefficients = sp.zeros(sp.shape(vectors)[1], dtype=complex)
        for index, vector in enumerate(vectors):
            coefficients[index] = sp.dot(vector.conj(), decomposee)
        return coefficients

    def time_evolve(self, t):
        """

        :param t:
        :return:
        """
        evolved = sp.zeros(self.dimensions)
        for i in range(self.dimensions):
            evolved = evolved + self.coefficients[i] * self.eigenvectors[:, i] * sp.exp(self.eigenvalues[i] * t)
        return evolved
