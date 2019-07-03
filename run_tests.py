import nose


if __name__ == "__main__":
    # Writes 1 to load proper config file
    with open('testing', 'w') as file_handler:
        file_handler.write('1')
    nose.run()
    with open('testing', 'w') as file_handler:
        file_handler.write('0')