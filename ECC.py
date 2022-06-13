import random
from math import inf


# a point on the elliptic curve
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __neg__(self):
        return Point(self.x,-self.y)


class EllipticCurveCryptography:

    def __init__(self, a, b, p):
        # (y^2)%p = (x^3 + ax + b)%p
        self.a = a
        self.b = b
        self.p = p

    def field_mod(self, x):
        return x % self.p

    def inverse(self, x):
        for inv in range(self.p):
            if (x * inv) % self.p == 1:
                return inv
        return 0

    def point_addition(self, P, Q):
        if (P == Point(inf, inf)) or (P==Point(inf,-inf)) or (P==Point(-inf,inf)) or (P==Point(-inf,-inf)):
            return Point(Q.x, Q.y)
        elif (Q == Point(inf, inf)) or (Q==Point(inf,-inf)) or (Q==Point(-inf,inf)) or (Q==Point(-inf,-inf)):
            return Point(P.x, P.y)
        elif ((P == Point(inf, inf)) or (P==Point(inf,-inf)) or (P==Point(-inf,inf)) or (P==Point(-inf,-inf))) and (Q == Point(inf, inf)) or (Q==Point(inf,-inf)) or (Q==Point(-inf,inf)) or (Q==Point(-inf,-inf)):
            return Point(inf, inf)

        x1, y1 = P.x, P.y
        x2, y2 = Q.x, Q.y

        if x1 % self.p == x2 % self.p and y1 % self.p == -y2 % self.p:
            return Point(inf, inf)
        # sometimes we have to make a point addition (P!=Q)
        # and sometimes a point doubling (P=Q)
        if x1 == x2 and y1 == y2:
            # point doubling operation (P=Q)
            m = self.field_mod((3 * x1 * x1 + self.a) * self.inverse(2 * y1))
        else:
            # point addition operation (P!=Q)
            m = self.field_mod((y2 - y1) * self.inverse(x2 - x1))

        # we have updated x3 and y3 coordinates
        x3 = self.field_mod(m * m - x1 - x2)
        y3 = self.field_mod(m * (x1 - x3) - y1)

        return Point(x3, y3)

    # it has O(m) linear running time complexity
    def double_and_add(self, n, P):

        temp_point = Point(P.x, P.y)
        binary = bin(n)[3:]

        for binary_char in binary:
            # point doubling operation
            temp_point = self.point_addition(temp_point, temp_point)

            if binary_char == '1':
                # point addition operation
                temp_point = self.point_addition(temp_point, P)

        return temp_point


if __name__ == '__main__':
    # Alphabets used for storing the data
    Alphabets = 'abcdefghijklmnopqrstuvwxyz0123456789#.+-'

    # the E(a,b,p) finite elliptic curve
    a, b, p = 1, 6, 37
    ecc = EllipticCurveCryptography(a, b, p)

    # Generating points of the elliptic curve over field Fp
    Points = []
    for i in range(p):
        for j in range(p):
            if pow(j, 2) % p == (pow(i, 3) + a * i + b) % p:
                Points.append(Point(i, j))
    # Including Point of infinity
    Points.append(Point(inf, inf))

    # Defining Public Keys
    G = Point(2, 4)  # Generator Point
    H = ecc.double_and_add(5, G)  # d=5 is the private key

    Assign = {}
    for i in range(len(Alphabets)):
        Assign[Alphabets[i]] = Points[i]
    print(Assign)
    Plain_Text = "arvind#kumar#rakesh#kumar#sanjanadevi#123456789#b-45#ajay#tenament#maninagar#ahmedabad#gujarat"


    def get_key(val):
        for key, value in Assign.items():
            if val == value:
                return key
        return "key doesn't exist"


    def ecc_encoding(plain_text, e1, e2):
        cipher_text = ''
        for i in plain_text:
            r = random.randint(2, len(Assign)+1)
            C1 = ecc.double_and_add(r, e1)
            C2 = ecc.point_addition(Assign[i], ecc.double_and_add(r, e2))
            T1 = get_key(C1)
            T2 = get_key(C2)
            cipher_text = cipher_text + T1 + T2
        return cipher_text


    def ecc_decoding(cipher_text, private_key):
        plain_text = ''
        for i in range(0, len(cipher_text), 2):
            C1 = Assign[cipher_text[i]]
            C2 = Assign[cipher_text[i + 1]]
            M = ecc.point_addition(C2, -ecc.double_and_add(private_key, C1))
            M.x %= p
            M.y %= p
            plain_text = plain_text + get_key(M)
        return plain_text

    cipher_text = 'fmqhx5efws-anv13.1l0s7fla-xz16f#+5#6eccxjh6utozwn0o#ztb51fsqa3xhtot4hv9b3wpak#0l6p3pto0ae2#4jlwfqa#4v593g0hunob5-dtoe#k1.nayv4oasm3ltmcl2+7qwkv#oroamw'

    # print(ecc_encoding(Plain_Text, G, H))

    # print(ecc_decoding(cipher_text, 5))



    # # Alice random number (a)
    # alice_random = random.randint(2, len(Points) + 1)
    # # Bob's random number (b)
    # bob_random = random.randint(2, len(Points) + 1)
    #
    # # public key with double and add algorithm
    # # THESE ARE POINTS ON THE ELLIPTIC CURVE
    # alice_public = ecc.double_and_add(alice_random, generator_point)
    # bob_public = ecc.double_and_add(bob_random, generator_point)
    #
    # # they can generate the private key (which will be the same)
    # alice_secret_key = ecc.double_and_add(alice_random, bob_public)
    # bob_secret_key = ecc.double_and_add(bob_random, alice_public)
    #
    # print(alice_random)
    # print(bob_random)
    # print(alice_secret_key)
    # print(bob_secret_key)
    # print(alice_public)
    # print(bob_public)
    # print(Points)
    # print(len(Points))
