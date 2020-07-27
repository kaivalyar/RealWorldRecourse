import numpy as np
import choix

class Feature:

    def __init__(self, featureName=None, itemKey=None, surveyName=None):
        self.featureName = featureName
        self.itemKey = itemKey
        self.surveyName = surveyName
        self.strength = -1
    
    def __str__(self):
        return '{}/{} - {} : {}'.format(self.featureName, self.surveyName, self.itemKey, self.strength)

class FeatureSet:

    def __init__(self, filename, exclude=None):
        if isinstance(filename, list):
            feats = filename
        else:
            with open(filename, 'r') as f:
                feats = f.readline().strip().split(',')
            if exclude is None:
                pass
                #feats = feats[1:]
            elif isinstance(exclude, int):
                feats.remove(feats[exclude])
            elif isinstance(exclude, str):
                feats.remove(exclude)
            elif isinstance(exclude, list):
                for ex in exclude:
                    if isinstance(ex, int):
                        feats.remove(feats[ex])
                    elif isinstance(ex, str):
                        feats.remove(ex)
        self.features = []
        for i, feature in enumerate(feats):
            self.features.append(Feature(feature, i, feature))

    def __str__(self):
        result = '\n'
        for f in self.features:
            result += '\t'
            result += str(f)
            result += '\n'
        return result

    def get_by_featureName(self, featureName):
        for feature in self.features:
            if feature.featureName == featureName:
                return feature

    def get_by_surveyName(self, surveyName):
        for feature in self.features:
            if feature.surveyName == surveyName:
                return feature

    def get_by_itemKey(self, itemKey):
        for feature in self.features:
            if feature.itemKey == itemKey:
                return feature

    def rename(self, featureName, surveyName):
        feature = self.get_by_featureName(featureName)
        feature.surveyName = surveyName

    def fit(self, surveyfile):
        cdata = []
        with open(surveyfile, 'r') as f:
            for line in f:
                line = line.split('>')
                key1 = self.get_by_surveyName(line[0].strip()).itemKey
                key2 = self.get_by_surveyName(line[1].strip()).itemKey
                cdata.append((key1, key2))
        results = choix.opt_pairwise(len(self.features), cdata, alpha=0.0001)
        for i, strength in enumerate(np.exp(results)):
            self.get_by_itemKey(i).strength = strength
        pass

if __name__ == '__main__':
    print('Running dummy test: ')
    data = FeatureSet('./data/adult.csv', exclude=['HasTelephone', 'CheckingAccountBalance_geq_0', 'CheckingAccountBalance_geq_200', 'SavingsAccountBalance_geq_100', 'SavingsAccountBalance_geq_500'])
    data.rename('Age', 'age')
    data.fit('./data/adult-survey.txt')
    print(data)
    pass



