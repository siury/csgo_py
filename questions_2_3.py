# 1838074
# Tyler Sverak and Ryan Siu
# 6/8/2019
# Section AB
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import pycountry


def main():
    '''
    A simple main method that runs the functions that produce
    the desire plots
    '''
    pdata = pd.read_csv('players.csv')
    # uncomment the next line to change the data for the top player test
    # pdata = pdata.iloc[[0, 13, 15, 104, 141, 133, 194]]
    # uncomment the next lines for worldwide stat test data
    '''
    pdata = pdata.iloc[[62595, 3000, 5000, 7000, 15000, 25000, 40000,
                        54321, 60000]]
    temp = pdata[['origin', 'name', 'kills',
                  'kast', 'rating', 'deaths', 'headshots']]
    print(temp)
    '''
    top20 = pd.read_csv('top20.csv')
    geography = gpd.read_file('countries.geojson')
    player_stats(pdata, top20)
    # the following are lists of specific players and teams
    # that we want to look at information for
    top30Teams = ['nitr0', 'NAF', 'EliGE', 'Stewie2K', 'Twistzz',
                  'Xyp9x', 'dupreeh', 'gla1ve', 'device', 'Magisk',
                  'allu', 'Aerial', 'xseveN', 'Aleksib', 'sergej',
                  'NBK-', 'RpK', 'apEX', 'ALEX', 'ZywOo',
                  'NEO', 'olofmeister', 'GuardiaN', 'NiKo', 'rain',
                  'Zeus', 'flamie', 's1mple', 'electronic', 'Boombl4',
                  'Xizt', 'JW', 'twist', 'KRIMZ', 'Brollan',
                  'FalleN', 'fer', 'coldzera', 'TACO', 'felps',
                  'f0rest', 'GeT_RiGhT', 'dennis', 'Lekr0', 'REZ',
                  'daps', 'tarik', 'Brehze', 'Ethan', 'CeRq',
                  'arT', 'yuurih', 'VINI', 'KSCERATO', 'ableJ',
                  'jks', 'AZR', 'jkaem', 'Gratisfaction', 'Liazz',
                  'JaCkz', 'shox', 'kennyS', 'AmaNEk', 'Lucky',
                  'karrigan', 'chrisJ', 'woxic', 'frozen', 'ropz',
                  'aizy', 'Kjaerbye', 'JUGi', 'gade', 'valde',
                  'fitch', 'SANJI', 'buster', 'qikert', 'Jame',
                  'huNter', 'LETN1', 'nexa', 'ottoNd', 'EspiranTo',
                  'Sico', 'dexter', 'erkaSt', 'malta', 'DickStacy',
                  'bubble', 'v1c7oR', 'blocker', 'SHiPZ', 'poizon',
                  'steel', 'freakazoid', 'koosta', 'WARDELL', 'neptune',
                  'Snappi', 'MSL', 'k0nfig', 'niko', 'refrezh',
                  'gob b', 'tabseN', 'tiziaN', 'denis', 'XANTARES',
                  'friberg', 'es3tag', 'NaToSaphiX', 'stavn', 'blameF',
                  'ANGE1', 'oskar', 'loWel', 'ISSAA', 'nukkye',
                  'cajunb', 'RUSH', 'autimatic', 'vice', 'Golden',
                  'SZPERO', 'Furlan', 'GruBy', 'phr', 'kaper',
                  'HUNDEN', 'Bubzkji', 'b0RUP', 'acoR', 'sjuush',
                  'zeff', 'XigN', 'HSK', 'xeta', 'stax',
                  'syrsoN', 'Spiidi', 'mirbit', 'k1to', 'faveN',
                  'facecrack', 'almazer', 'FL1T', 'xsepower', 'Jerry']
    large_tourneys = ["IEM Katowice 2019", "IEM Katowice 2019 Main Qualifier",
                      "FACEIT Major 2018", "FACEIT Major 2018 Main Qualifier",
                      "ELEAGUE Major 2018",
                      "ELEAGUE Major 2018 Main Qualifier"]
    p = pdata.copy()
    p = p[p["name"].isin(top30Teams)]
    big = pdata.copy()
    big = big[big["tournament"].isin(large_tourneys)]
    plot_region_player_distribution(p, geography, 'Top 30 Players')
    plot_region_player_distribution(pdata, geography, 'All Players')
    plot_region_player_distribution(big, geography, 'Big Tournaments')


def player_stats(data, filter):
    '''
    Takes a dataframe of player match data and a dataframe of players to
    be examined and saves an image called top20player_stats.png
    of each player's stats compared to
    the average of the stat of all players in the dataframe of
    examined players. Returns the data used for the graph
    '''
    # data is now filtered to examined players in the filter only, in order
    data = data.groupby('name').mean()
    data = data.reindex(filter['name'])
    data = data.head(len(filter))
    data = data.dropna()
    # data is filtered only to stats we want then
    # averages are calculated for each
    data = data[['kills', 'assists', 'rating',
                 'headshots', 'opening_kills', 'adr']]
    columns = list(data)
    averages = {}
    for i in columns:
        total = 0
        count = 0
        for j in data[i]:
            count += 1
            total += j
        averages[i] = (total / count)
    for col in data:
        data[col] = data[col] / averages[col]
    # data is plotted and saved, then "done" is printed to the console
    final = data
    final.plot.bar(figsize=(22, 10), title='Stats by Ratio to Average ' +
                   'for Top 20 Players')
    plt.savefig('top20player_stats.png')
    return final


def country_stats(data):
    '''
    takes a dataframe of matches by player. Returns a DataFrame with
    stats organized by country
    '''
    data['kast'] = data['kast'].apply(lambda x: float(x.strip('%')))
    data = data.groupby('origin').mean()
    data['country'] = data.index
    return data


def plot_region_player_distribution(pdata, countries, title):
    '''
    Using a dataframe of player match information, country geometry
    in a geodataframe, and a String title, creates a plot of all
    countries with their color being dependant on one of several stats.
    Saves a seperate plot focusing completely
    on Scandanavian countries. Saves the data as Scadanavian30Stats.png and
    WorldTop30Stats.png or ScadanavianPlayerStats.png and
    WorldPlayerStats.png depending on the title passed.
    '''
    # creates a copy of player match data and combines it with
    # the geodataframe with country geometry
    pf = pdata
    pf = pf.drop_duplicates(subset='name', keep='first')
    d = pf.groupby("origin")["name"].count().to_frame()
    d["country"] = d.index
    d["country"] = d["country"].apply(getCodes)
    merged = countries.merge(d, left_on="ISO_A3",
                             right_on="country", how="left")
    # filters out countries we have no data on and calculates average
    # stats for each country using the player data, combines that with
    # the map information and plots it
    merged = merged.dropna()
    stats = country_stats(pdata)
    stats['country'] = stats["country"].apply(getCodes)
    merged = merged.merge(stats, left_on='country',
                          right_on='country', how='left')
    save_graph(merged, False, title)
    save_graph(merged, True, title)


def save_graph(df, scan, title):
    '''
    Saves a picture with four plots, showing off KAST, player population,
    headshots, and deaths on average for each country. Title on the
    graphes depends on title passed
    '''
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, figsize=(20, 10), ncols=2)
    df.plot(column='kast', ax=ax1, legend=True).set_title('KAST')
    df.plot(column='name', ax=ax2, legend=True).set_title('Population of '
                                                          + title)
    df.plot(column='headshots', ax=ax3, legend=True).set_title('Headshots')
    df.plot(column='deaths', ax=ax4, legend=True).set_title('Deaths')
    if not scan:
        if (title == 'All Players'):
            fig.savefig('WorldPlayerStats.png')
        elif (title == 'Big Tournaments'):
            fig.savefig('WorldBigTourneyStats.png')
        else:
            fig.savefig('WorldTop30Stats.png')
    else:
        miny = 40
        minx = 4
        maxx = 35
        maxy = 85
        ax1.set_xlim(minx, maxx)
        ax1.set_ylim(miny, maxy)
        ax2.set_xlim(minx, maxx)
        ax2.set_ylim(miny, maxy)
        ax3.set_xlim(minx, maxx)
        ax3.set_ylim(miny, maxy)
        ax4.set_xlim(minx, maxx)
        ax4.set_ylim(miny, maxy)
        if (title == 'All Players'):
            fig.savefig('ScadanavianPlayerStats.png')
        elif (title == 'Big Tournaments'):
            fig.savefig('ScandanavianTourneys.png')
        else:
            fig.savefig('Scadanavian30Stats.png')


def getCodes(country):
    '''
    returns the corresponding country code in a String
    for the country name passed
    '''
    if country == "Russia":
        return "RUS"
    if country == "Czech Republic":
        return "CZE"
    if country == "Korea":
        return "KOR"
    if country == "Macedonia":
        return "MKD"
    if country == "Vietnam":
        return "VNM"
    if country == "Moldova":
        return "MDA"
    if country == "Syria":
        return "SYR"
    if country == "Taiwan":
        return "TWN"
    return pycountry.countries.get(name=country).alpha_3


if __name__ == '__main__':
    main()
