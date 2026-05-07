from controllers.system_controller import SystemController
from controllers.menu_controller import MenuController
from views.console_view import ConsoleView


def main():
    sistema = SystemController()
    vista   = ConsoleView()
    menu    = MenuController(sistema, vista)
    menu.run()


if __name__ == "__main__":
    main()
