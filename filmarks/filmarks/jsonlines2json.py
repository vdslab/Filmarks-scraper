import json


def main():
    data = []
    occupations = set()
    genres = set()
    countries = set()
    with open('./filmarks.jsonlines', mode='r') as f:
        for line in f.readlines():
            obj = json.loads(line)
            for o in obj['production_members'].keys():
                occupations.add(o)
            for g in obj['genres']:
                genres.add(g)
            for c in obj['production_countries']:
                countries.add(c)
            data.append(obj)
    # with open('./filmarks_fix.jsonlines', mode='w') as f:
    #     for d in data:
    #         d['production_members'] = d.pop('production_member')
    #         f.write(json.dumps(d, ensure_ascii=False) + '\n')

    with open('./filmarks.json', mode='w') as f:
        occupations = list(occupations)
        genres = list(genres)
        countries = list(countries)
        print(occupations, genres, countries)
        data = {'occupations': occupations,
                'genres': genres, 'countires': countries, 'movies': data}
        json.dump(data, f, ensure_ascii=False)


if __name__ == '__main__':
    main()
