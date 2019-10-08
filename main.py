import objects


def main():
    try:
        while True:
            objects.Window().run()
            if "y" not in input("Do you want to play again?[y/n]"):
                break
    except:
        pass

if __name__ == '__main__':
    main()
