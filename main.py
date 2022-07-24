from project1.cut import cut
from project1.proj1 import proj1
from project2.predict_q import predict_q
from project2.predict_eg import predict_eg

import project3.project3 as proj3

import project4.project4 as proj4

def ans():
    cut()
    proj1()
    predict_q()
    predict_eg()

    proj3.main()

    ans = proj4.initial()

    return ans

# if __name__ == '__main__':
#     ans()
print(ans())