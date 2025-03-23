'''
Напишіть Python-скрипт, який завантажує текст із заданої URL-адреси, аналізує частоту використання слів у тексті за допомогою парадигми MapReduce і візуалізує топ-слова з найвищою частотою використання у тексті.
Імпортуйте необхідні модулі (matplotlib та інші).
Візьміть код реалізації MapReduce з конспекту.
Створіть функцію visualize_top_words для візуалізації результатів.
У головному блоці коду отримайте текст за URL, застосуйте MapReduce та візуалізуйте результати.
'''

import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import requests

def get_text(url):
    response = requests.get(url)
    response.raise_for_status()  
    return response.text

def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


def map_reduce(text, search_words=None):
    text = remove_punctuation(text)
    words = text.split()

    if search_words:
        words = [word for word in words if word in search_words]

    with ThreadPoolExecutor() as executor:
        mapped_values = executor.map(map_function, words)
    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = executor.map(reduce_function, shuffled_values)

    return dict(reduced_values)


def visualize_top_words(result, top_n=10):
    top_words = Counter(result).most_common(top_n)
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title('Top {} Most Frequent Words'.format(top_n))
    plt.gca().invert_yaxis()
    plt.show()

if __name__ == '__main__':

    url = "https://gutenberg.net.au/ebooks01/0100011.txt"
    text = get_text(url)
    result = map_reduce(text)
    visualize_top_words(result)

