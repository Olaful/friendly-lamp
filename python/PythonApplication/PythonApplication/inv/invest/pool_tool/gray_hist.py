import matplotlib as mp
import argparse
import matplotlib.pyplot as plt


def gray_histogram(img):
    mp_img = mp.image.imread(img)

    axis = plt.gca()
    axis.hist(mp_img.flatten(), 256)

    plt.show()


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--path',
                            default='',
                            type=str,
                            required=False,
                            help='the path of img')
    args = arg_parser.parse_args()

    if args.path:
        gray_histogram(args.path)


if __name__ == '__main__':
    main()
