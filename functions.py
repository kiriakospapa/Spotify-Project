import matplotlib.pyplot as plt


def plot_artists_with_most_songs(singers, n=10):
    singers_unique = set(singers)
    names = []
    times = []
    for singer in singers_unique:
        print(singers.count(singer))
        names.append(singer)
        times.append(singers.count(singer))

    singers_unique = [x for _,x in sorted(zip(times,singers_unique))]

    times = sorted(times)

    plt.pie(times[-n:], labels=singers_unique[-n:], shadow=True)
    plt.show() 
 

if __name__ =='__main__':
    pass