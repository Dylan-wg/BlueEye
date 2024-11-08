#
# Group Project of Group 7, Global Challenge I, Hong Kong Baptist University
# Project Name: Blue Eye
#
# Co-developers: Dylan, Tim
#
# Group Leader: Dylan
# Group Members: Carson, Kyra, Thomas, Tim, Violet
#
# Repository: https://github.com/Dylan-wg/GarbageRecognition
#
from Windows.Camera_window import Camera_window
from Windows.Main_Window import Main_Window


def main():
    # main_window = Main_Window()
    # main_window.render()
    # main_window.root.mainloop()
    window = Camera_window()
    window.render()
    window.root.mainloop()


if __name__ == "__main__":
    main()
