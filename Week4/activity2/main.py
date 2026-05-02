from land import RectangularLand


def main():
    print("Rectangular Land Calculator")

    length = float(input("Please enter the length of the land: "))
    width = float(input("Please enter the width of the land: "))

    land = RectangularLand(length, width)

    land.print_dimensions()

    area = land.calculate_area()
    perimeter = land.calculate_perimeter()

    print(f"Area: {area}")
    print(f"Perimeter: {perimeter}")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()