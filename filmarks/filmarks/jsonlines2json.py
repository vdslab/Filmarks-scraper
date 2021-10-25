import json


def main():
    data = []
    with open('./filmarks.jsonlines', mode='r') as f:
        for line in f.readlines():
            obj = json.loads(line)

            data.append(obj)

    with open('./filmarks.json', mode='w') as f:
        json.dump(data, f, ensure_ascii=False)


if __name__ == '__main__':
    main()
