import pandas as pd
import pickle

if __name__ == '__main__':

    f = open('./dataset/final_dataset.pickle', 'rb')
    dataset = pickle.load(f)
    f.close()
    print("dataset loaded.....")
    print('==========>')


    binary_class_dataset = []
    for index in range(len(dataset)):
        task = []
        task.append(dataset[index][0])
        if str(dataset[index][1][0]).strip() == 'none':
            ref = 0
        else:
            ref = 1
        task.append(ref)

        binary_class_dataset.append(task)

    f = open('./dataset/binary_class_dataset.pickle', 'wb')
    pickle.dump(binary_class_dataset,f)
    f.close()
    print("dataset saved.....")
    print('==========>')

    print(binary_class_dataset[0])
