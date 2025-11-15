import pandas as pd
import matplotlib.pyplot as plt

class preprocesser:
    def __init__(self, pathToCSV):
        df = pd.read_csv(pathToCSV)
        self.df = df

    # finds titles like Mr. and Miss and Dr. and puts them into a "Title" column
    def extractTitles(self):
        self.df["Title"] = self.df["Name"].str.extract(r",\s*([^\.]+)\.")
        return self.df
    
    # Some ticket numbers are the same, so this counts them and puts them into "TicketGroupSize"
    def findTicketGroups(self):
        self.df["TicketGroupSize"] = self.df.groupby("Ticket")["Ticket"].transform("count")

    def makeUnknownEmbarkCategory(self):
        self.df["Embarked"] = self.df["Embarked"].fillna("Unknown")

    def binAges(self):
        self.df["AgeGroup"] = pd.cut(
            self.df["Age"],
            bins=[0, 12, 18, 35, 50, 80, 200],
            labels=["Child", "Teen", "YoungAdult", "Adult", "Senior", "WiseOne"]
        )

        # Imputation
        self.df["AgeGroup"] = self.df["AgeGroup"].cat.add_categories("Unknown")
        self.df["AgeGroup"] = self.df["AgeGroup"].fillna("Unknown")
        
    def removeColumns(self, columnNames):
        self.df = self.df.drop(columnNames, axis=1)

    def produceCSV(self, fileName):
        self.df.to_csv(fileName)


if __name__ == "__main__":
    thingy = preprocesser("train.csv")
    
    # Feature Generation
    thingy.extractTitles()
    thingy.findTicketGroups()
    thingy.makeUnknownEmbarkCategory()
    thingy.binAges()

    # Removing the stuff that I don't want
    thingy.removeColumns(["Name", "Age", "Ticket", "Cabin"])

    # plt.hexbin(thingy.df['SibSp'], thingy.df['Parch'], gridsize=10, cmap='viridis')
    # plt.colorbar(label='Density')
    # plt.xlabel('SibSp')
    # plt.ylabel('Parch')
    # plt.show()
    print(thingy.df.head())
    thingy.produceCSV("out.csv")
