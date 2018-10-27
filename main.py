
from feature_extract import extract
from collusion_attack import collude, diff
from train_and_test import train_and_test
import dct_stego as dct
if __name__ == "__main__":
    w_len = 1

    dct.main()

    # Collusion attack and difference between collude frame and stego frame
    collude("images/", "stego/", w_len)
    diff("images/", "stego/", w_len)

    # Collusion attack and difference between collude frame and cover frame
    collude("images/", "cover/", w_len)
    diff("images/", "cover/", w_len)

    # Extract feature
    extract("images/diff/stego/", "images/diff/cover/")

    # Trainning and Test
    train_and_test(data_file="feature.csv")





