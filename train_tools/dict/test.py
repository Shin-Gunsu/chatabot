def read_corpus_data(filename):
    with open(filename, 'r',encoding='utf-8') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
    return data

corpus_data = read_corpus_data('corpus.txt')

print(corpus_data)