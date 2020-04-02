# test output


with open('output30.txt', 'r') as f:
    i = 0
    j = 0
    for line in f:
        j += 1
        (truth, pred1) = line.split()
        truth = truth.split('-')
        print(truth[0])
        pred1 = pred1.split('.')
        pred1 = pred1[0] + '.' + pred1[1]
        print(pred1)
        if truth[0] == pred1:
            i += 1
            print('Match!')

    print('Guessed', i, '/', j)
