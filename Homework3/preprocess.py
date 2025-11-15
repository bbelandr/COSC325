import pandas as pd

# ONE_HOT_ENCODE = ["Sex", "Embarked"]

class preprocesser:
    def __init__(self, pathToCSV):
        df = pd.read_csv(pathToCSV)
        self.df = df

    """
    oneHotEncode(columnNames)
    newDf = df
    for each name in columnNames:
        set uniqueData
        for each data in df[name]: 
            uniqueData.add(data)
            This will give us unique entries for every different input in the column
        remove one of the entries from uniqueData
            This will ensure that we don't over-encode
        for data in uniqueData
            newDf.addColumn(data)
                Make sure this is initialized to 0
        for row in df:
            if row[name] in data:
                newDf[row[name]] = 1
        delete column newDf[name]
        df = newDf
    return newDf
    """
    def oneHotEncode(self, columnNames):
        newDf = self.df
        for name in columnNames:
            # get unique categories (preserve stable order), skip NaN
            cats = list(pd.Series(self.df[name].dropna().unique()))
            if not cats:
                continue
            encodedCats = cats[1:]  # drop the first category to avoid perfect multicollinearity
            for cat in encodedCats:
                colName = f"{name}.{cat}"
                newDf[colName] = 0  # initialize column to 0
                newDf.loc[self.df[name] == cat, colName] = 1    # set 1 where the original column equals this category

            newDf.drop(columns=[name], inplace=True)
        self.df = newDf
        return newDf

    # Returns the modified dataframe and also modifies the dataframe that it holds internally. 
    def minMaxScale(self, columnNames):
        newDf = self.df.copy()

        for name in columnNames:
            # Normalize
            col = self.df[name]
            newDf[name] = (col - col.min()) / (col.max() - col.min())
        self.df = newDf
        return newDf
    
    def standardize(self, columnNames):
        

    def produceCSV(self, fileName):
        self.df.to_csv(fileName)

if __name__ == "__main__":
    thingy = preprocesser("train.csv")
    thingy.minMaxScale(["Age", "Fare"])
    thingy.produceCSV("out.csv")
