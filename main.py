import cfscrape, csv, argparse, json, datetime
from bs4 import BeautifulSoup

#Alterando

class Spotify:
    def __init__(self) -> None:
        pass

    def spotify_top_charts(self, country='global', date='latest', frequency='daily', quantity=200):
        scraper = cfscrape.create_scraper()
        url = f'https://spotifycharts.com/regional/{country}/{frequency}/{date}'
        html = scraper.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', class_='chart-table')
        top_charts = table.find_all('tr')
        for chart in top_charts[1:quantity+1]:
            top_chart = {
                "chart_position":chart.find('td', class_='chart-table-position').text,
                "chart_music_name":chart.select('td > strong')[0].text,
                "chart_author_name":chart.select('td > span')[0].text.strip('by '),
                "total_streams":chart.find('td', class_='chart-table-streams').text
            }
            yield top_chart

    def save_to_csv(self, data):
        with open('top_chart_spotify.csv', 'w',newline='', encoding='utf-8') as file:
            fieldnames = ['chart_position', 'chart_author_name', 'chart_music_name']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow(item)
            print('Saved to csv file!')
            file.close()

    def save_to_json(self, data, output):
        list_to_json = []
        for item in data:
            list_to_json.append(item)
        json_save = {"top_charts":list_to_json}
        with open(f'{output}.json', 'w', encoding='utf-8') as file:
            json.dump(json_save, file)
            file.close()
        print(f'Saved to "{output}.json"')

    def using_argparse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', required=False, action='store', dest='country', default='global', type=str, help='Insert one country to get the Spotify top charts.')
        parser.add_argument('-d', required=False, action='store', dest='date', type=str, default='latest', help='Date to get the Spotify top charts.')
        parser.add_argument('-f', required=False, action='store', dest='frequency', type=str, default='daily', help='"daily" or "weekly" needed.')
        parser.add_argument('-q', required=False, action='store', dest='quantity', default=200, type=int, help='Quantity of musics to get.')
        parser.add_argument('-o', required=True, action='store', dest='output', type=str, help='File name to save.')
        args = parser.parse_args()
        output = self.spotify_top_charts(country=args.country, date=args.date, frequency=args.frequency, quantity=args.quantity)
        self.save_to_json(output, args.output)

if __name__ == '__main__':
    spotify_trends = Spotify()
    spotify_trends.using_argparse()