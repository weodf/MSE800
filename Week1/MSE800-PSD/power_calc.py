def calculate_power(base, exponent):
        return base ** exponent
    

if __name__ == "__main__":
    print("WEEK1 MSE800-PSD")
    
    try:
        x = int(input("Please enter base x: "))
        y = int(input("please enter exponent y: "))
        
        result = calculate_power(x, y)
        
        print(f"Result: {x} raised to the power of {y} is {result}")
        
    except ValueError:
        print("Invalid input. Please enter numeric values.")