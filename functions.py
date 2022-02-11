from unicodedata import name
import matplotlib.pyplot as plt
import numpy
import plotly.express as px


def make_autopct(values):
    """Returns the values as labels for a pie char and not the percentages"""
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return f'{val} songs'
    return my_autopct

def plot_artists_with_most_songs(singers, n=10):
    """Plots the top N singers with the most liked songs"""
    singers_unique = set(singers)
    names = []
    times = []
    for singer in singers_unique:
        print(singers.count(singer))
        names.append(singer)
        times.append(singers.count(singer))

    singers_unique = [x for _,x in sorted(zip(times,singers_unique))]

    times = sorted(times)

    plt.pie(times[-n:], labels=singers_unique[-n:], autopct=make_autopct(times[-n:]), shadow=True)
    plt.title(label=f"Top {n} Artists With Most Liked Songs")
    plt.show() 
    

if __name__ =='__main__':
    pass