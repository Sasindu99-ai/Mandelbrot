from App import App

controllers = {
    'W': 'move up',
    'S': 'move down',
    'A': 'move left',
    'D': 'move right',
    '↑': 'zoom in',
    '↓': 'zoom out',
    '←': 'decrease max iterations',
    '→': 'increase max iterations',
    'C': 'change texture',
    'R': 'recenter',
    'Z': 'auto zoom out to center'
}

welcomeText = f"""
#############################################
#                                           #
#   Welcome to the Mandelbrot Set Viewer    #
#                                           #
#############################################

Controls: 
---------
{chr(10).join([f'\t{key}: {value.capitalize()}' for key, value in controllers.items()])}

Press 'Enter' to continue..."""

if __name__ == '__main__':
    print(welcomeText)
    input()

    app = App()
    app.run()
