"""
take in csv data of trump tweet and extract only the text, save to csv
"""
import pandas as pd


def main():
    f1 = pd.read_csv('data/realDonaldTrump_bf_office.csv')
    f2 = pd.read_csv('data/realDonaldTrump_in_office.csv')

    f['text'].to_csv('data/tweets.csv', index=False)


if __name__=="__main__":
    main()
