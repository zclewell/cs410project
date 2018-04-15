import metapy

def get_results(cfg_file):
    idx = metapy.index.make_inverted_index(cfg_file)

    results = []
    return results

def main():
    print(get_results('config.toml'))

if __name__ == '__main__':
    main()
