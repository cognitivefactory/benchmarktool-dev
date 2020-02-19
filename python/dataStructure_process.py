'''
    TRAIN TEST SPLIT
    Split the dataset in two according to a specified proportion
    output : 
        train, test : two datasets
'''
def train_test_split(data, training_proportion):
    l_data = len(data)
    train_proportion = int(training_proportion * l_data)
    #0.6 => 60% of the data will be used for the training
    
    return data[:train_proportion], data[train_proportion:]